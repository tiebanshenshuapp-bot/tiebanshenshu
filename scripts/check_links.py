#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
链接检查 / Link Checker

检查 Markdown 中的相对链接是否指向真实存在的文件。

支持 Jekyll 语义：GitHub Pages 会把 `foo.md` 渲染为 `foo.html`，
因此 `docs/index.md` 里的 `zh-hans/faq.html` 是合法的。
本脚本会把 `.html` 目标同时尝试映射回 `.md` 与 `index.md`。

用法：
    python scripts/check_links.py            # 检查当前目录
    python scripts/check_links.py --root .   # 指定根目录
    python scripts/check_links.py --external # 额外检查官网外链可达性

退出码：0 通过 / 1 失败

License: PolyForm Noncommercial 1.0.0
"""

import argparse
import os
import re
import ssl
import sys
import urllib.request

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "_preview", "_site"}

# Markdown 链接：排除 http(s)、锚点、mailto
MD_LINK = re.compile(r"\]\((?!https?://|#|mailto:)([^)#\s]+)(?:#[^)\s]*)?")

# 外链
EXT_LINK = re.compile(r"https?://[^\s\)\]\>" + chr(39) + chr(96) + "，。]+")


def resolve(base_dir, target):
    """判断相对链接目标是否存在（含 Jekyll .html -> .md 映射）。"""
    clean = target.strip().split("?")[0]
    if not clean:
        return True

    direct = os.path.normpath(os.path.join(base_dir, clean))
    if os.path.exists(direct):
        return True

    # Jekyll 语义：foo.html 可能来自 foo.md 或 foo/index.md
    if clean.endswith(".html"):
        stem = clean[:-5]
        for cand in (stem + ".md",
                     os.path.join(stem, "index.md"),
                     os.path.join(stem, "README.md")):
            if os.path.exists(os.path.normpath(os.path.join(base_dir, cand))):
                return True

    # 目录型链接：foo/ 可能指向 foo/index.md
    if clean.endswith("/"):
        for cand in ("index.md", "README.md"):
            if os.path.exists(os.path.normpath(os.path.join(base_dir, clean, cand))):
                return True

    return False


def collect_md_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.lower().endswith(".md"):
                yield dirpath, fn


def check_relative(root):
    bad, total = [], 0
    for dirpath, fn in collect_md_files(root):
        p = os.path.join(dirpath, fn)
        rel_p = os.path.relpath(p, root)
        try:
            text = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for m in MD_LINK.finditer(text):
            target = m.group(1).strip()
            if not target:
                continue
            total += 1
            if not resolve(dirpath, target):
                bad.append((rel_p, target))
    return total, bad


def check_external(root, timeout=25):
    """只检查官网域名，避免拖慢且不误伤第三方站点。"""
    urls = set()
    for dirpath, fn in collect_md_files(root):
        p = os.path.join(dirpath, fn)
        try:
            text = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for m in EXT_LINK.finditer(text):
            u = m.group().strip(".,;:*_ `。，" + chr(34) + chr(39) + "<>")
            if "tiebanshenshuapp.com" in u:
                urls.add(u)

    ctx = ssl.create_default_context()
    results, fail = [], []
    for u in sorted(urls):
        try:
            req = urllib.request.Request(
                u, method="HEAD",
                headers={"User-Agent": "Mozilla/5.0 (compatible; tieban-ci/1.0)"})
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                results.append((u, r.status))
        except Exception as e:
            fail.append((u, str(e)[:80]))
    return results, fail


def main(argv=None):
    ap = argparse.ArgumentParser(description="相对链接检查（支持 Jekyll 映射）")
    ap.add_argument("--root", default=".", help="扫描根目录")
    ap.add_argument("--external", action="store_true", help="同时检查官网外链")
    args = ap.parse_args(argv)

    root = os.path.abspath(args.root)
    total, bad = check_relative(root)

    print(f"检查文件夹: {root}")
    print(f"相对链接: {total} 条")

    if bad:
        print(f"\n❌ 失效链接 {len(bad)} 条：")
        for p, t in bad:
            print(f"   {p} -> {t}")
    else:
        print("✅ 全部有效（含 Jekyll .html -> .md 映射）")

    ext_fail = []
    if args.external:
        ok, ext_fail = check_external(root)
        print(f"\n官网外链: {len(ok)}/{len(ok) + len(ext_fail)} 可达")
        for u, st in ok:
            print(f"   {st} {u}")
        for u, err in ext_fail:
            print(f"   FAIL {u} :: {err}")

    if bad or ext_fail:
        print("\n结论：FAIL")
        return 1
    print("\n结论：PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())