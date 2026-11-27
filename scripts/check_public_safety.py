#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公开发布安全门禁 / Public Release Safety Gate

在推送公开仓库前检查：敏感信息、私有资产、超大文件、禁止文件类型、私有算法关键词。

用法：
    python scripts/check_public_safety.py            # 检查当前目录
    python scripts/check_public_safety.py --root .   # 指定根目录

退出码：
    0 = 通过
    1 = 发现阻断项（禁止发布）
    2 = 发现告警项（需人工复核）

License: PolyForm Noncommercial 1.0.0
"""

import argparse
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 规则
# ---------------------------------------------------------------------------

# 禁止出现的文件扩展名（可能是私有资产或构建产物）
FORBIDDEN_EXT = {
    ".db", ".sqlite", ".sqlite3",      # 数据库
    ".exe", ".dll", ".msi", ".dmg",    # 安装包/二进制
    ".zip", ".rar", ".7z", ".tar", ".gz",  # 压缩包（可用 Base64 藏内容）
    ".pem", ".key", ".p12", ".pfx",    # 密钥
    ".pyc", ".pyo",                     # 编译产物
    ".map",                             # source map（可能泄露源码结构）
    ".onnx", ".pt", ".safetensors", ".bin",  # 模型权重
    ".db-shm", ".db-wal",
}

# 禁止出现的路径片段
FORBIDDEN_PATH_PARTS = {
    "_internal",
    "PRIVATE_EVIDENCE",
    ".git",   # 由 git 自身管理，不扫描
}

# 私有资产关键词 —— 出现即需人工判断
PRIVATE_ASSET_KEYWORDS = [
    "tiaowen.db",
    "Reference Oracle",
    "Golden Case",
    "Holdout Case",
    "私有Core",
    "私有核心",
    "完整条文库",
    "12000条完整",
    "本命基数",
    "刻干数",
    "考刻定分完整规则",
    "商业客户端源码",
    "安装包下载",
]

# 疑似 Secret 的正则
SECRET_PATTERNS = [
    (r"gh[pousr]_[A-Za-z0-9]{20,}", "GitHub Token"),
    (r"github_pat_[A-Za-z0-9_]{20,}", "GitHub Fine-grained PAT"),
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI 风格 API Key"),
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
    (r"AIza[0-9A-Za-z_\-]{35}", "Google API Key"),
    (r"-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----", "私钥"),
    (r"xox[baprs]-[A-Za-z0-9\-]{10,}", "Slack Token"),
    (r"(?i)(password|passwd|pwd)\s*[=:]\s*['\"][^'\"]{8,}['\"]", "明文密码"),
    (r"(?i)(api[_-]?key|secret[_-]?key|access[_-]?token)\s*[=:]\s*['\"][^'\"]{16,}['\"]", "疑似密钥"),
]

# 真实个人信息模式（可能违反隐私要求）
PII_PATTERNS = [
    (r"\b1[3-9]\d{9}\b", "中国手机号"),
    (r"\b\d{17}[\dXx]\b", "中国身份证号"),
]

MAX_FILE_SIZE = 1024 * 1024  # 1 MB

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", ".pytest_cache"}
TEXT_EXT = {
    ".md", ".txt", ".py", ".yml", ".yaml", ".json", ".cff", ".toml",
    ".cfg", ".ini", ".html", ".css", ".js", ".ts", ".sh", "",
}


class Report:
    def __init__(self):
        self.blocking = []
        self.warnings = []
        self.infos = []
        self.scanned = 0

    def block(self, path, msg):
        self.blocking.append((str(path), msg))

    def warn(self, path, msg):
        self.warnings.append((str(path), msg))

    def info(self, path, msg):
        self.infos.append((str(path), msg))

    def print_and_exit(self):
        print("=" * 68)
        print("公开发布安全门禁 / Public Release Safety Gate")
        print("=" * 68)
        print(f"已扫描文件: {self.scanned}")
        print()

        if self.blocking:
            print(f"❌ 阻断项 {len(self.blocking)} 个 —— 禁止发布")
            for p, m in self.blocking:
                print(f"   [BLOCK] {p}\n           {m}")
            print()

        if self.warnings:
            print(f"⚠️  告警项 {len(self.warnings)} 个 —— 需人工复核")
            for p, m in self.warnings:
                print(f"   [WARN]  {p}\n           {m}")
            print()

        if self.infos:
            print(f"ℹ️  提示项 {len(self.infos)} 个 —— 文档中的边界说明，通常可忽略")
            for p, m in self.infos[:10]:
                print(f"   [INFO]  {p}: {m}")
            if len(self.infos) > 10:
                print(f"   …… 另有 {len(self.infos) - 10} 项")
            print()

        if self.blocking:
            print("结论：FAIL — 存在阻断项，禁止推送公开仓库。")
            return 1
        if self.warnings:
            print("结论：PASS WITH WARNINGS — 请人工确认告警项后再发布。")
            return 2
        print("结论：PASS — 未发现敏感信息、私有资产或禁止文件。")
        return 0


def is_text_file(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXT:
        return True
    try:
        with open(path, "rb") as f:
            chunk = f.read(2048)
        if b"\x00" in chunk:
            return False
        chunk.decode("utf-8")
        return True
    except (OSError, UnicodeDecodeError):
        return False


def check_file(path: Path, root: Path, rep: Report):
    rel = path.relative_to(root)
    rep.scanned += 1

    # 1. 禁止的扩展名
    if path.suffix.lower() in FORBIDDEN_EXT:
        rep.block(rel, f"禁止的文件类型 {path.suffix}（可能的私有资产/二进制/压缩包）")
        return

    # 2. 文件大小
    try:
        size = path.stat().st_size
    except OSError:
        return
    if size > MAX_FILE_SIZE:
        rep.block(rel, f"文件过大 {size / 1024 / 1024:.2f} MB（上限 1 MB）")

    if not is_text_file(path):
        rep.warn(rel, "二进制或非文本文件，未做内容扫描，请人工确认")
        return

    # 3. 内容扫描
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return

    for pattern, label in SECRET_PATTERNS:
        if re.search(pattern, content):
            # 允许在文档中描述规则本身（如本文件）
            if path.name in ("check_public_safety.py",):
                continue
            rep.block(rel, f"疑似 {label} 泄漏（正则匹配）")

    for pattern, label in PII_PATTERNS:
        if re.search(pattern, content):
            if path.name in ("check_public_safety.py",):
                continue
            rep.warn(rel, f"疑似 {label}（可能是虚构样例，请确认）")

    for kw in PRIVATE_ASSET_KEYWORDS:
        if kw in content:
            if path.name in ("check_public_safety.py", "test_tools.py",
                             "THIRD_PARTY_NOTICES.md", "SECURITY.md"):
                continue
            if path.suffix.lower() in (".md", ".txt", ".cff"):
                rep.info(rel, f"提及「{kw}」（文档中的边界说明）")
            else:
                rep.warn(rel, f"代码/数据文件中出现私有资产关键词「{kw}」，请确认不是实际内容")


def main(argv=None):
    ap = argparse.ArgumentParser(description="公开发布安全门禁")
    ap.add_argument("--root", default=".", help="扫描根目录")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"错误：{root} 不是目录", file=sys.stderr)
        return 1

    rep = Report()

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            p = Path(dirpath) / fn
            # 路径层面检查
            rel_parts = set(p.relative_to(root).parts)
            if rel_parts & FORBIDDEN_PATH_PARTS:
                rep.block(p.relative_to(root), "位于禁止公开的目录")
                continue
            check_file(p, root, rep)

    code = rep.print_and_exit()
    return code


if __name__ == "__main__":
    sys.exit(main())