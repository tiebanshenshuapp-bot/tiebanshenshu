#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 结构检查 / Markdown Structure Check

检查项：
  1. 代码块围栏是否闭合
  2. 表格列数是否一致
  3. 标题是否跳级（h1 -> h3）

用法：
    python scripts/check_markdown_structure.py

退出码：0 通过 / 1 发现问题

License: PolyForm Noncommercial 1.0.0
"""

import os
import re
import sys

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv"}


def check_file(path):
    problems = []
    lines = open(path, encoding="utf-8", errors="replace").read().split("\n")

    # 标记代码块内的行（围栏本身也算代码块内）
    in_code = False
    flags = []
    for line in lines:
        if line.strip().startswith("```"):
            flags.append(True)
            in_code = not in_code
        else:
            flags.append(in_code)

    # 1. 围栏闭合
    fences = sum(1 for line in lines if line.strip().startswith("```"))
    if fences % 2 != 0:
        problems.append(f"{path}: 代码块未闭合（``` 出现 {fences} 次）")

    # 2. 表格列数
    i = 0
    while i < len(lines):
        if not flags[i] and lines[i].strip().startswith("|"):
            block, j = [], i
            while j < len(lines) and not flags[j] and lines[j].strip().startswith("|"):
                block.append(lines[j])
                j += 1
            if len(block) >= 2:
                counts = [row.count("|") for row in block]
                if len(set(counts)) > 1:
                    problems.append(
                        f"{path}:{i + 1} 表格列数不一致 {sorted(set(counts))}")
            i = j
        else:
            i += 1

    # 3. 标题跳级
    prev = 0
    for n, line in enumerate(lines):
        if flags[n]:
            continue
        m = re.match(r"^(#{1,6})\s", line)
        if m:
            level = len(m.group(1))
            if prev and level > prev + 1:
                problems.append(
                    f"{path}:{n + 1} 标题跳级 h{prev}->h{level}: {line.strip()[:40]}")
            prev = level

    return problems


def main(root="."):
    root = os.path.abspath(root)
    all_problems = []
    count = 0

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".md"):
                count += 1
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, root)
                all_problems.extend(p.replace(full, rel) for p in check_file(full))

    print(f"检查 Markdown 文件: {count}")
    if all_problems:
        print(f"发现 {len(all_problems)} 个结构问题:")
        for p in all_problems[:30]:
            print("  ", p)
        return 1
    print("OK: 所有 Markdown 结构完整（代码块闭合 / 表格对齐 / 无标题跳级）")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))