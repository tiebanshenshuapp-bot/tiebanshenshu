#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
繁简转换 / Chinese Script Conversion

复用 OpenCC（成熟方案），**不自制对照表**。
简体为唯一编辑源，繁体版本由本脚本生成后再人工复核。

依赖：
    pip install opencc-python-reimplemented
    （或使用系统级 opencc CLI）

用法：
    python scripts/i18n_convert.py docs/zh-hans/accuracy.md
    python scripts/i18n_convert.py --all          # 转换全部 zh-hans/*.md
    python scripts/i18n_convert.py --check        # 只检查残留，不写文件

输出：
    docs/zh-hk/<name>.md   OpenCC s2hk
    docs/zh-tw/<name>.md   OpenCC s2twp（含台湾词汇转换）

注意：
- 会保留并改写 front matter 的 lang 字段
- **不覆盖**已存在且标记 `manual: true` 的人工译稿
- 转换结果必须人工复核（尤其地区用语、书名、人名、异体字）

License: PolyForm Noncommercial 1.0.0
"""

import argparse
import io
import os
import re
import sys

try:
    from opencc import OpenCC
except ImportError:
    print("错误：需要 OpenCC。请运行：\n"
          "    pip install opencc-python-reimplemented\n"
          "（本项目要求复用成熟方案，不自制繁简对照表）", file=sys.stderr)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 简体专用字（用于验证转换是否彻底）
SIMP_ONLY = set(
    # 高频简体专用字（简繁不同形）
    "说这为个过实验证据历问题对错试让别认记忆择选传语读页链结杂乱关见现发门华进还变动调"
    "够论谁给当从击标复测确犹财骗钱费买卖赚该应须争议异体种类样级层简双边间时总统计划规则"
    "们会诉两没学评释"
    # 注意：不要包含简繁同形字（如 告/科/解/值/整/告/究/方/法/内/容），否则会误报
)

# 人工微调表：OpenCC 输出后仍需修正的领域用词
REGION_FIX = {
    "zh-hk": [
        ("試著自己算一下", "試吓自己計一計"),
        ("準不準", "準唔準"),
    ],
    "zh-tw": [
        ("軟件", "軟體"),
        ("網絡", "網路"),
        ("打印", "列印"),
    ],
}

TITLES = {
    "zh-hk": None,   # 由 OpenCC 生成
    "zh-tw": None,
}

LANG_MAP = {"zh-hk": "zh-Hant-HK", "zh-tw": "zh-Hant-TW"}


def split_front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def convert_front_matter(fm, cc, lang):
    out = []
    for line in fm.split("\n"):
        if line.startswith("title:"):
            out.append(f'title: "{cc.convert(line[6:].strip().strip(chr(34)))}"')
        elif line.startswith("description:"):
            out.append(f'description: "{cc.convert(line[12:].strip().strip(chr(34)))}"')
        elif line.startswith("lang:"):
            out.append(f"lang: {lang}")
        else:
            out.append(line)
    return "\n".join(out)


def convert_one(src_path, write=True, check_only=False):
    rel = os.path.relpath(src_path, ROOT)
    text = io.open(src_path, encoding="utf-8-sig").read()
    fm, body = split_front_matter(text)

    # 只接受 docs/zh-hans 下的文件 —— 否则传 docs/en/index.md 会把英文写进 zh-hk/zh-tw
    SRC_DIR = os.path.join(ROOT, "docs", "zh-hans")
    if os.path.abspath(os.path.dirname(src_path)) != os.path.abspath(SRC_DIR):
        raise ValueError(f"只能转换 docs/zh-hans 下的文件，收到：{src_path}")

    name = os.path.basename(src_path)
    results = []

    for target_dir in ("zh-hk", "zh-tw"):
        dst = os.path.join(ROOT, "docs", target_dir, name)

        # 默认不覆盖任何已存在文件（人工译稿、地区用词修正都可能被冲掉）
        if os.path.exists(dst) and not os.environ.get("I18N_FORCE"):
            results.append((target_dir, "SKIP (已存在，需 I18N_FORCE=1 才覆盖)"))
            continue

        conv = "s2hk" if target_dir == "zh-hk" else "s2twp"
        cc = OpenCC(conv)

        new_fm = convert_front_matter(fm, cc, LANG_MAP[target_dir])
        new_body = cc.convert(body)

        for a, b in REGION_FIX.get(target_dir, []):
            new_body = new_body.replace(a, b)

        out_text = ("---\n" + new_fm + "\n---\n" + new_body) if fm else new_body

        # 残留简体检查
        found = sorted({c for c in new_body if c in SIMP_ONLY})
        warn = f"残留简体: {''.join(found)}" if found else "OK"

        if write and not check_only:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            io.open(dst, "w", encoding="utf-8", newline="\n").write(out_text)

        results.append((target_dir, warn))

    return rel, results


def main(argv=None):
    ap = argparse.ArgumentParser(description="繁简转换（OpenCC）")
    ap.add_argument("files", nargs="*", help="要转换的简体文件")
    ap.add_argument("--all", action="store_true", help="转换 docs/zh-hans 下全部 .md")
    ap.add_argument("--check", action="store_true", help="只检查残留，不写文件")
    args = ap.parse_args(argv)

    if args.all:
        d = os.path.join(ROOT, "docs", "zh-hans")
        if not os.path.isdir(d):
            print(f"错误：目录不存在 {d}", file=sys.stderr)
            return 2
        files = [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith(".md")]
    elif args.files:
        files = [os.path.abspath(f) for f in args.files]
    else:
        ap.print_help()
        return 1

    if not files:
        print("没有可转换的文件", file=sys.stderr)
        return 1

    total_bad = 0
    skipped = 0
    for f in files:
        if not os.path.exists(f):
            print(f"跳过（不存在）: {f}")
            skipped += 1
            continue
        try:
            rel, results = convert_one(f, write=not args.check, check_only=args.check)
        except ValueError as e:
            print(f"跳过：{e}", file=sys.stderr)
            skipped += 1
            continue
        except (OSError, UnicodeDecodeError) as e:
            print(f"跳过（读取失败）{f}: {e}", file=sys.stderr)
            skipped += 1
            continue
        print(f"\n{rel}")
        for target, status in results:
            mark = "❌" if status.startswith("残留简体") else "✓"
            print(f"  {mark} → docs/{target}/  {status}")
            if status.startswith("残留简体"):
                total_bad += 1

    print()
    if total_bad:
        print(f"⚠️  {total_bad} 处残留简体，请人工核对")
        return 1
    print("✅ 转换完成，无残留简体（仍需人工复核地区用语）")
    return 0


if __name__ == "__main__":
    sys.exit(main())