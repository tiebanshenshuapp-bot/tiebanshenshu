#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公开发布安全门禁 / Public Release Safety Gate

在推送公开仓库前检查：敏感信息、私有资产、超大文件、禁止文件类型、私有算法关键词。

用法：
    python scripts/check_public_safety.py            # 检查当前目录
    python scripts/check_public_safety.py --root .   # 指定根目录
    python scripts/check_public_safety.py --quiet    # 只输出阻断与告警

退出码：
    0 = 通过
    1 = 发现阻断项（禁止发布）
    2 = 发现告警项（需人工复核）

## 安全设计说明（每一项都对应一次真实漏洞修复）

1. **密钥正则覆盖无引号赋值**
   `.env` 里的 `DB_PASSWORD=xxx` 是最常见的真实泄漏形态。
   旧版只认带引号的赋值，导致这种格式直接 PASS。

2. **文件名白名单改为精确相对路径**
   旧版按文件名匹配，任意目录下的同名文件（如 `evil/check_public_safety.py`）
   可完全绕过扫描。

3. **文本判定改为多段采样**
   旧版只读前 2048 字节，若正好切断多字节汉字，
   整个文件会被误判为二进制并跳过内容扫描。

4. **边界声明识别要求上下文相邻**
   旧版"文件里任何位置出现'不含'就整体豁免"，
   实测可让 `不含完整条文库。\n完整条文库已打包在 priv/tiaowen.db` 通过检查。

5. **符号链接目录会被遍历**（含循环检测）
   旧版 `os.walk` 默认不跟随符号链接，实测 `scan/link -> ../real`
   可让内含 Token 的目录完全不被扫描。

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
    ".db", ".sqlite", ".sqlite3",
    ".exe", ".dll", ".msi", ".dmg",
    ".zip", ".rar", ".7z", ".tar", ".gz",
    ".pem", ".key", ".p12", ".pfx",
    ".pyc", ".pyo",
    ".map",
    ".onnx", ".pt", ".safetensors", ".bin",
    ".db-shm", ".db-wal",
}

# 位于这些目录的内容不扫描
SKIP_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "venv",
    ".pytest_cache", "dist", "_preview", "_site", ".tox", ".mypy_cache",
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

# 允许提及上述关键词的**精确相对路径**（不是文件名 —— 防止同名绕过）
KEYWORD_EXEMPT_PATHS = {
    "scripts/check_public_safety.py",
    # 安全门回归测试文件：必须内置格式正确的**样本** token 才能验证检测有效。
    # 这些样本是虚构的，不是真实凭据；该文件本身受 PR review 监督。
    "tests/test_safety_gate.py",
    "demo/tests/test_tools.py",
    "THIRD_PARTY_NOTICES.md",
    "SECURITY.md",
    "docs/QUALITY_BASELINE.md",
    "docs/zh-hans/kaoke.md",
    "docs/zh-hk/kaoke.md",
    "docs/zh-tw/kaoke.md",
    "docs/en/kaoke.md",
    "README.md", "README.zh-HK.md", "README.zh-TW.md", "README.en.md",
    "ROADMAP.md", "CONTRIBUTING.md", "CHANGELOG.md", "CITATION.cff",
    "samples/README.md", "NOTICE.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    "docs/zh-hans/faq.md", "docs/zh-hk/faq.md", "docs/zh-tw/faq.md", "docs/en/faq.md",
    "docs/zh-hans/getting-started.md", "docs/zh-hk/getting-started.md",
    "docs/zh-tw/getting-started.md", "docs/en/getting-started.md",
    "docs/zh-hans/reading-a-report.md", "docs/zh-hk/reading-a-report.md",
    "docs/zh-tw/reading-a-report.md", "docs/en/reading-a-report.md",
}

# 疑似 Secret 的正则
SECRET_PATTERNS = [
    # --- Token 本体 ---
    (r"gh[pousr]_[A-Za-z0-9]{20,}", "GitHub Token"),
    (r"github_pat_[A-Za-z0-9_]{20,}", "GitHub Fine-grained PAT"),
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI 风格 API Key"),
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
    (r"AIza[0-9A-Za-z_\-]{35}", "Google API Key"),
    (r"-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----", "私钥"),
    (r"xox[baprs]-[A-Za-z0-9\-]{10,}", "Slack Token"),
    (r"glpat-[A-Za-z0-9_\-]{20,}", "GitLab Token"),
    (r"npm_[A-Za-z0-9]{36}", "npm Token"),
    (r"dop_v1_[a-f0-9]{64}", "DigitalOcean Token"),
    (r"SG\.[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}", "SendGrid API Key"),

    # --- 密码/密钥赋值：带引号（JSON / YAML / 代码） ---
    (r"(?i)(?:password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key)"
     r"\s*[:=]\s*['\"][^'\"\s]{6,}['\"]", "明文密码/密钥（带引号）"),

    # --- 密码/密钥赋值：不带引号（.env / INI / shell —— 最高频的真实泄漏） ---
    (r"(?im)^\s*(?:export\s+)?(?:DB|MYSQL|POSTGRES|REDIS|MONGO|SMTP|PAY|WX|ALI)_?"
     r"(?:PASSWORD|PASSWD|PWD|SECRET|SECRET_KEY|API_KEY|APIKEY|ACCESS_KEY|"
     r"PRIVATE_KEY|AUTH_TOKEN|ACCESS_TOKEN|SECRETKEY)\s*=\s*\S{6,}\s*$",
     "明文密码/密钥（.env / INI 无引号赋值）"),

    # --- 单独的 SESSION_SECRET / JWT_SECRET 等 ---
    (r"(?im)^\s*(?:export\s+)?(?:SESSION|JWT|COOKIE|CSRF|ENCRYPTION)_?"
     r"(?:SECRET|KEY|TOKEN)\s*=\s*\S{6,}\s*$",
     "明文会话密钥（无引号赋值）"),

    # --- 纯裸键赋值（a.ini 里的 password=xxx / secret=xxx）---
    (r"(?im)^\s*(?:password|passwd|pwd|secret|token|apikey|api_key|"
    r"access_key|private_key)\s*=\s*\S{6,}\s*$",
     "明文密码/密钥（INI 裸键）"),

    # --- JSON 键值形态 ---
    (r'(?i)"(?:password|passwd|secret|api_?key|access_?token|private_?key)"'
     r'\s*:\s*"[^"]{6,}"', "明文密码/密钥（JSON）"),

    # --- YAML 键值形态 ---
    (r"(?im)^\s*(?:password|passwd|secret|api_?key|access_?token|private_?key)"
     r"\s*:\s*[^\s\"'][^\s]{5,}\s*$", "明文密码/密钥（YAML）"),
]

# 真实个人信息模式
PII_PATTERNS = [
    (r"\b1[3-9]\d{9}\b", "中国手机号"),
    (r"\b\d{17}[\dXx]\b", "中国身份证号"),
]

MAX_FILE_SIZE = 1024 * 1024  # 1 MB

TEXT_EXT = {
    ".md", ".txt", ".py", ".yml", ".yaml", ".json", ".cff", ".toml",
    ".cfg", ".ini", ".html", ".css", ".js", ".ts", ".sh", ".svg", ".xml",
    ".env", ".example", ".csv", ".gitignore", ".editorconfig", "",
}

# 「边界声明」标志：命中所在行或紧邻行出现这些表述，才算"声明不公开"
BOUNDARY_MARKERS = (
    "不在此", "不公开", "不在本仓库", "禁止公开", "不得公开", "不予公开",
    "not part of", "not published", "is not included", "do not publish",
    "不包含", "不含", "排除", "不发布", "不在公开",
)


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

    def print_and_exit(self, quiet=False):
        if not quiet:
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

        if self.infos and not quiet:
            print(f"ℹ️  提示项 {len(self.infos)} 个 —— 通常可忽略")
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
    """判定是否文本文件。

    不使用"前 2048 字节含 \\x00 就判二进制"的粗糙做法 ——
    那样会把在 2048 边界切断多字节汉字的文件误判为二进制，
    导致整个文件跳过内容扫描（这是真实漏洞，已修复）。
    """
    if path.suffix.lower() in TEXT_EXT or path.name in {
        ".env", ".gitignore", ".gitattributes", "LICENSE", "NOTICE", "Dockerfile", "Makefile",
    }:
        return True
    try:
        size = path.stat().st_size
        samples = []
        with open(path, "rb") as f:
            samples.append(f.read(4096))
            if size > 8192:
                f.seek(size // 2)
                samples.append(f.read(4096))
                f.seek(max(0, size - 4096))
                samples.append(f.read(4096))
        blob = b"".join(samples)
        if b"\x00" in blob:
            return False
        try:
            blob.decode("utf-8")
            return True
        except UnicodeDecodeError:
            replaced = blob.decode("utf-8", errors="replace")
            bad = replaced.count("\ufffd")
            return bad / max(1, len(replaced)) < 0.02
    except OSError:
        return False


def line_of(content: str, pos: int) -> int:
    return content.count("\n", 0, pos) + 1


def context_lines(content: str, pos: int, radius: int = 1) -> str:
    """取命中位置所在行及其相邻行，用于判断是否属于边界声明。"""
    lines = content.split("\n")
    ln = line_of(content, pos) - 1
    lo = max(0, ln - radius)
    hi = min(len(lines), ln + radius + 1)
    return "\n".join(lines[lo:hi])


def is_boundary_statement(content: str, match, radius: int = 0) -> bool:
    """命中是否出现在「边界声明」语境中。

    **默认只认同一行**（radius=0）。
    旧版用"文件里任何位置写了不含就整体豁免"，实测可这样绕过：
        本仓库不含完整条文库。
        完整条文库已打包在 priv/private_core/tiaowen.db
    → 两条都被判为声明，整体 PASS。

    收紧为同行后，上面第 2 行不含禁令词 → 会被判为 unsafe → WARN。
    这是"宁严勿宽"的选择：安全门漏报的代价远大于误报。
    """
    ctx = match.group(0) + "\n" + context_lines(content, match.start(), radius)
    return any(m in ctx for m in BOUNDARY_MARKERS)


def check_file(path: Path, root: Path, rep: Report):
    rel = path.relative_to(root)
    rel_posix = Path(rel).as_posix()
    rep.scanned += 1

    # 1. 禁止的扩展名
    if path.suffix.lower() in FORBIDDEN_EXT:
        rep.block(rel, f"禁止的文件类型 {path.suffix}（可能的私有资产/二进制/压缩包）")
        return

    # 2. 文件大小（超限立即返回，不再读入内存）
    try:
        size = path.stat().st_size
    except OSError:
        return
    if size > MAX_FILE_SIZE:
        rep.block(rel, f"文件过大 {size / 1024 / 1024:.2f} MB（上限 1 MB）")
        return

    # 3. 自有品牌资源目录
    allowed_asset_dirs = ("assets/brand", "assets/social-preview", "assets/screenshots")
    if any(rel_posix.startswith(d) for d in allowed_asset_dirs) and \
       path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".svg"}:
        rep.info(rel, "自有品牌资源（来源可通过 git 历史追溯）")
        return

    if not is_text_file(path):
        rep.warn(rel, "二进制或非文本文件，未做内容扫描，请人工确认")
        return

    # 4. 内容扫描
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        rep.warn(rel, "无法读取，未扫描")
        return

    exempt = rel_posix in KEYWORD_EXEMPT_PATHS

    # 4a. Secret
    secret_hit = False
    for pattern, label in SECRET_PATTERNS:
        if secret_hit:
            break
        for m in re.finditer(pattern, content):
            if exempt:
                break
            sample = m.group(0)
            # 占位符 / 示例值放行
            if re.search(r"(?i)(xxx+|your[_-]?|<[^>]+>|\$\{|placeholder|example|"
                         r"dummy|fake|redacted|changeme|sample)", sample):
                rep.info(rel, f"{label} 疑似占位符（第 {line_of(content, m.start())} 行）")
                continue
            rep.block(rel, f"疑似 {label} 泄漏（第 {line_of(content, m.start())} 行）")
            secret_hit = True
            break

    # 4b. PII
    pii_hit = False
    for pattern, label in PII_PATTERNS:
        if pii_hit:
            break
        for m in re.finditer(pattern, content):
            if exempt:
                break
            rep.warn(rel, f"疑似 {label}（第 {line_of(content, m.start())} 行，可能是虚构样例，请确认）")
            pii_hit = True
            break

    # 4c-前置：可疑私有路径（.db / private_core / priv/ 等）
    # 这类路径出现在公开仓意味着「在指引读者去找私有资产」
    # 只匹配**具体资产路径**，不匹配 private 这类普通英文词
    SUSPICIOUS_PATH = re.compile(
        r"(?i)(?:^|[\s\"'(])"
        r"(?:priv|private[_-]core|golden[_-]cases?|holdout[_-]?cases?)/[\w./-]+"
        r"|(?:^|[\s\"'(])[\w.-]+/[\w.-]+\.(?:db|sqlite3?)\b"
    )
    if not exempt:
        for m in SUSPICIOUS_PATH.finditer(content):
            frag = m.group(0)
            # 排除文档中的正当提及（如说明"禁止使用 priv/ 目录"）
            if is_boundary_statement(content, m):
                continue
            rep.warn(rel, f"出现可疑私有路径「{frag}」（第 {line_of(content, m.start())} 行），"
                          f"请确认不是真实资产位置")
            break

    # 4d. 私有资产关键词
    for kw in PRIVATE_ASSET_KEYWORDS:
        if kw not in content:
            continue
        if exempt:
            rep.info(rel, f"提及「{kw}」（该文件属允许说明清单）")
            continue

        # 逐处检查：只要有一处**不在**边界声明语境，就需要人工确认
        unsafe = None
        boundary = False
        for m in re.finditer(re.escape(kw), content):
            if is_boundary_statement(content, m):
                boundary = True
            else:
                unsafe = m
                break

        if unsafe is not None:
            suffix = path.suffix.lower()
            if suffix in (".md", ".txt", ".cff", ".svg", ".html"):
                rep.info(rel, f"提及「{kw}」（第 {line_of(content, unsafe.start())} 行，文档说明）")
            else:
                rep.warn(rel, f"出现私有资产关键词「{kw}」（第 {line_of(content, unsafe.start())} 行），"
                              f"请确认不是实际内容")
        elif boundary:
            rep.info(rel, f"提及「{kw}」（边界声明语境）")


def iter_files(root: Path):
    """遍历文件。跟随符号链接并检测循环（防止 symlink 逃逸扫描）。"""
    seen = set()

    def walk(d):
        try:
            real = os.path.realpath(d)
        except OSError:
            return
        if real in seen:
            return
        seen.add(real)
        try:
            entries = list(os.scandir(d))
        except OSError:
            return
        for e in entries:
            try:
                if e.is_dir(follow_symlinks=True):
                    if e.name in SKIP_DIRS:
                        continue
                    yield from walk(e.path)
                elif e.is_file(follow_symlinks=True):
                    yield Path(e.path)
            except OSError:
                continue

    yield from walk(str(root))


def main(argv=None):
    ap = argparse.ArgumentParser(description="公开发布安全门禁")
    ap.add_argument("--root", default=".", help="扫描根目录")
    ap.add_argument("--quiet", action="store_true", help="不输出提示项")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"错误：{root} 不是目录", file=sys.stderr)
        return 1

    rep = Report()
    for p in iter_files(root):
        try:
            rel_parts = set(p.relative_to(root).parts)
        except ValueError:
            continue
        if rel_parts & SKIP_DIRS:
            continue
        check_file(p, root, rep)

    return rep.print_and_exit(quiet=args.quiet)


if __name__ == "__main__":
    sys.exit(main())