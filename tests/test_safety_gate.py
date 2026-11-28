#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全门禁回归测试 / Safety Gate Regression Tests

每个用例对应一次**真实发现过的漏洞**。防止未来改动把洞重新打开。

用法：
    python tests/test_safety_gate.py

退出码：0 全通过 / 1 有失败
"""

import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, "scripts", "check_public_safety.py")

# (用例名, 相对路径, 内容, 期望是否应被拦截)
CASES = [
    # ---- 已修复的真实漏洞 ----
    ("env_password", ".env", "DB_PASSWORD=RealSecret123456", True),
    ("ini_bare_key", "c.ini", "password=RealSecret987654", True),
    ("json_key", "d.json", '{"api_key":"RealKeyAbCdEf123456"}', True),
    ("yaml_key", "e.yml", "api_key: SI_SECRET_YAMLKEY_7TX22B1V\n", True),
    ("gh_token", "t.txt", "ghp_RealTokenAbCdEfGhIjKlMnOpQrStUvWxYz", True),
    # 注意：AKIAIOSFODNN7EXAMPLE 是 AWS 官方示例 key，会被占位符规则正确放行，
    # 所以这里用一个不含 example/dummy 等词的真实格式样本
    ("aws_key", "a.txt", "AKIAZ7X9KQ2MN4PQ8RTU", True),
    ("private_key", "k.txt",
     "-----BEGIN RSA PRIVATE KEY-----\nMIIEow...\n-----END RSA PRIVATE KEY-----", True),
    ("private_path", "p.md", "部署时把 priv/private_core/tiaowen.db 复制过去", True),
    ("db_file", "data.sqlite3", "x", True),
    ("zip_file", "pack.zip", "x", True),

    # ---- 文件名绕过：任意目录的同名检测脚本不得豁免 ----
    ("filename_bypass", "evil/check_public_safety.py",
     "ghp_RealTokenAbCdEfGhIjKlMnOpQrStUvWxYz", True),
    ("filename_bypass2", "evil/SECURITY.md",
     "ghp_RealTokenAbCdEfGhIjKlMnOpQrStUvWxYz", True),

    # ---- 边界声明逃逸：写一句"不含"不能豁免另一行的泄漏 ----
    ("boundary_escape", "evil.md",
     "本仓库不含完整条文库。\n完整条文库已打包在 priv/private_core/tiaowen.db", True),

    # ---- 不应误伤 ----
    ("normal_boundary", "ok.md",
     "本站不公开完整条文库。\n这是正常的说明文本。", False),
    ("placeholder", "sample.md",
     "示例：API_KEY=your_api_key_here\n占位：DB_PASSWORD=xxx", False),
    ("normal_doc", "readme.md", "# 说明\n\n这是正常文档。\n", False),
]


def run_gate(root):
    p = subprocess.run(
        [sys.executable, GATE, "--root", root, "--quiet"],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def main():
    if not os.path.exists(GATE):
        print(f"错误：找不到 {GATE}", file=sys.stderr)
        return 2

    passed = 0
    failed = []

    for name, rel, content, expect_block in CASES:
        tmp = tempfile.mkdtemp(prefix=f"sg_{name}_")
        try:
            target = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(target) or tmp, exist_ok=True)
            with open(target, "w", encoding="utf-8") as f:
                f.write(content)

            rc, out = run_gate(tmp)
            blocked = rc != 0

            ok = (blocked == expect_block)
            if ok:
                passed += 1
                print(f"  ✓ {name:22s} {'拦截' if expect_block else '放行'}")
            else:
                failed.append(name)
                print(f"  ✗ {name:22s} 期望{'拦截' if expect_block else '放行'}，"
                      f"实际 rc={rc}")
                print(f"      输出: {out.strip()[:160]}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # ---- 额外：symlink 逃逸 ----
    if hasattr(os, "symlink"):
        tmp = tempfile.mkdtemp(prefix="sg_symlink_")
        outside = tempfile.mkdtemp(prefix="sg_outside_")
        try:
            with open(os.path.join(outside, "secret.txt"), "w", encoding="utf-8") as f:
                f.write("ghp_RealTokenAbCdEfGhIjKlMnOpQrStUvWxYz")
            try:
                os.symlink(outside, os.path.join(tmp, "link"), target_is_directory=True)
                rc, out = run_gate(tmp)
                if rc != 0:
                    passed += 1
                    print("  ✓ symlink_escape        拦截")
                else:
                    failed.append("symlink_escape")
                    print("  ✗ symlink_escape        未拦截（符号链接逃逸）")
            except (OSError, NotImplementedError):
                print("  - symlink_escape        跳过（无权限创建符号链接）")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
            shutil.rmtree(outside, ignore_errors=True)

    print()
    total = passed + len(failed)
    print(f"通过 {passed}/{total}")
    if failed:
        print(f"失败: {', '.join(failed)}")
        return 1
    print("安全门回归测试全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())