#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
铁板神数 · 公开教学工具 (Tieban Shenshu Open Educational Tools)

零依赖、纯本地运行。只做可公开核查的确定性计算：
干支换算、六十甲子序号、术语查询、编号格式校验、文献引用生成。

不实现任何私有取数链，不产出个人命书，不采集任何用户资料。

License: PolyForm Noncommercial 1.0.0 (see ../LICENSE)
"""

import argparse
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 公开基础表（任何一本传统历书/命理入门书都载有，属公有领域知识）
# ---------------------------------------------------------------------------

TIANGAN = "甲乙丙丁戊己庚辛壬癸"
DIZHI = "子丑寅卯辰巳午未申酉戌亥"

# 天干五行（公开知识）
TIANGAN_WUXING = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
    "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水",
}

# 地支五行（公开知识）
DIZHI_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
    "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水",
}

# 天干五合（公开知识）
TIANGAN_HE = {
    "甲己": "土", "乙庚": "金", "丙辛": "水", "丁壬": "木", "戊癸": "火",
}

# 地支六冲（公开知识）
DIZHI_CHONG = [
    ("子", "午"), ("丑", "未"), ("寅", "申"),
    ("卯", "酉"), ("辰", "戌"), ("巳", "亥"),
]

# 地支三合局（公开知识）
DIZHI_SANHE = {
    "申子辰": "水局", "亥卯未": "木局",
    "寅午戌": "火局", "巳酉丑": "金局",
}

# ---------------------------------------------------------------------------
# 术语表
#
# 每条术语都必须标注 evidence_level：
#   "classical"  —— 古籍/传统文献可查
#   "traditional"—— 传统说法（师传、流派自述），非史实
#   "scholarly"  —— 学术讨论，存在争议
#   "editorial"  —— 本项目编者说明
# ---------------------------------------------------------------------------

GLOSSARY = {
    "铁板神数": {
        "also": ["铁版神数", "鐵板神數", "鐵版神數", "Tieban Shenshu"],
        "summary": "托名北宋邵雍的清代命理术数体系，以考刻推演著称。",
        "detail": (
            "铁板神数在清代乾隆、嘉庆年间兴起，相传由「铁卜子（铁道人）」校订条文。"
            "其法以出生年月日时干支配卦，核对六亲生肖，起数后按数取条文断语。"
        ),
        "evidence_level": "scholarly",
        "note": "托名邵雍之说缺乏宋代文献支持，学界多认为晚出。",
        "sources": [
            "维基百科「铁版神数」条目（综述性，供入门参考）",
            "明代杨慎对「大定数、蠢子数托名康节」的批评（见《升庵集》）",
        ],
    },
    "考刻": {
        "summary": "把出生时辰细分为刻，再借六亲信息校验，以确定「真刻」。",
        "detail": (
            "一个时辰（两小时）可分为八刻，每刻再分十五分。"
            "传统做法是先按六亲（父母、兄弟、配偶、子女）生肖等信息反推，"
            "在候选刻分中收窄，定位与已知事实相符的那一刻。"
        ),
        "evidence_level": "traditional",
        "note": "具体刻分划分法各流派不尽相同，不存在唯一公定标准。",
        "sources": ["传统命理文献对「刻」的通用定义（一时辰八刻）"],
    },
    "定分": {
        "summary": "在已定的「刻」内再细分十五分，进一步定位出生时刻。",
        "detail": "与考刻合称「考刻定分」，是铁板神数最具辨识度的操作环节。",
        "evidence_level": "traditional",
        "note": "分值的具体对应表属各家师传，公开文献记载并不一致。",
        "sources": [],
    },
    "条文": {
        "also": ["條文", "tiaowen"],
        "summary": "按编号排列的断语，是铁板神数的输出形态。",
        "detail": (
            "传统上通称约一万二千条，按地支分为子集至亥集共十二集。"
            "坊间抄本文字互有出入，目前不存在公认的善本定本。"
        ),
        "evidence_level": "scholarly",
        "note": "各家转录本的编号范围与分集方式存在差异。",
        "sources": ["清代术数文献通例", "公开数字化转录项目的自述"],
    },
    "太玄数": {
        "also": ["太玄數"],
        "summary": "起数环节使用的一种配数方法。",
        "detail": (
            "太玄数与《太玄经》数理相关，被用于把干支转换为数值。"
            "不同传承对具体配值有不同说法。"
        ),
        "evidence_level": "traditional",
        "note": "本工具不提供具体配值算法，因各家说法不一且部分属师传。",
        "sources": ["扬雄《太玄经》相关数理（公版古籍）"],
    },
    "皇极经世": {
        "also": ["皇極經世", "Huangji Jingshi"],
        "summary": "北宋邵雍所著，以元会运世推演历史周期的著作。",
        "detail": (
            "《皇极经世》是邵雍的代表作，属易学与历史哲学范畴。"
            "铁板神数常被说成借用其数理概念，但二者并非同一体系。"
        ),
        "evidence_level": "classical",
        "note": "把铁板神数直接等同于《皇极经世》推演法，属于过度简化。",
        "sources": ["邵雍《皇极经世》（公版古籍）"],
    },
    "邵子神数": {
        "also": ["邵子神數"],
        "summary": "铁板神数的别称之一，因托名邵雍而得名。",
        "detail": "不同地区与流派对该体系的称呼不统一，需按上下文判断。",
        "evidence_level": "traditional",
        "note": "名称混用常见，不宜据此认定传承关系。",
        "sources": [],
    },
}


# ---------------------------------------------------------------------------
# 核心计算
# ---------------------------------------------------------------------------

def ganzhi_of_year(year: int) -> str:
    """公历年 -> 干支。基准：公元 4 年为甲子年（公认算法）。"""
    if year < 1:
        raise ValueError("年份需为正整数")
    return TIANGAN[(year - 4) % 10] + DIZHI[(year - 4) % 12]


def jiazi_index(term: str) -> int:
    """返回六十甲子序号（1-60）。输入如「甲子」「癸亥」。"""
    term = term.strip()
    if len(term) != 2:
        raise ValueError("请输入两个字的干支，例如「甲子」")
    g, z = term[0], term[1]
    if g not in TIANGAN or z not in DIZHI:
        raise ValueError(f"「{term}」不是合法干支")
    gi, zi = TIANGAN.index(g), DIZHI.index(z)
    if gi % 2 != zi % 2:
        raise ValueError(f"「{term}」在六十甲子中不存在（阴阳不配）")
    # 解 (n-1) % 10 == gi 且 (n-1) % 12 == zi
    for n in range(1, 61):
        if (n - 1) % 10 == gi and (n - 1) % 12 == zi:
            return n
    raise ValueError(f"「{term}」无解")


def jiazi_at(n: int) -> str:
    """六十甲子第 n 位（1-60）。"""
    if not 1 <= n <= 60:
        raise ValueError("序号需在 1-60 之间")
    return TIANGAN[(n - 1) % 10] + DIZHI[(n - 1) % 12]


def check_verse_number(num: int, lo: int = 1001, hi: int = 13000) -> dict:
    """
    条文编号格式校验。

    注意：这里只校验「编号是否落在公开讨论的编号区间内」这一格式问题，
    不返回任何条文内容，也不做任何个人取数。

    默认区间 1001-13000 来自公开讨论中反复出现的编号范围描述，
    并非任何特定抄本的私有映射。
    """
    ok = lo <= num <= hi
    result = {
        "input": num,
        "valid_range": [lo, hi],
        "format_ok": ok,
    }
    if ok:
        offset = num - lo
        result["volume_index"] = offset // 1000 + 1   # 第几集（1-12）
        result["position_in_volume"] = offset % 1000 + 1
        result["note"] = "仅为编号格式校验，不包含条文内容。"
    else:
        result["note"] = f"编号不在 {lo}-{hi} 区间内。"
    return result


def cite(work: str) -> str:
    """生成基础文献引用骨架，提醒补全版本信息。"""
    templates = {
        "皇极经世": "邵雍. 皇极经世[M]. 宋. （请补：具体版本、影印或点校本、出版者、页码）",
        "太玄经": "扬雄. 太玄经[M]. 汉. （请补：具体版本、影校者、出版者、页码）",
        "升庵集": "杨慎. 升庵集[M]. 明. （请补：具体版本、卷次、页码）",
    }
    for key, val in templates.items():
        if key in work or work in key:
            return val
    return (
        f"《{work}》\n"
        "请按以下格式补全：\n"
        "  作者. 书名[M]. 朝代/年代. 版本信息. 出版者, 出版年: 页码.\n"
        "提示：引用公版古籍时，务必注明你实际使用的版本，"
        "因为不同版本的条文文字存在差异。"
    )


def show_term(name: str) -> dict:
    """返回术语条目；支持别名匹配。"""
    name = name.strip()
    if name in GLOSSARY:
        return {"term": name, **GLOSSARY[name]}
    for key, val in GLOSSARY.items():
        if name in val.get("also", []):
            return {"term": key, "matched_alias": name, **val}
    hits = [k for k in GLOSSARY if name in k]
    if hits:
        return {"term": None, "suggestions": hits}
    return {"term": None, "suggestions": list(GLOSSARY.keys())}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _print_json(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def _term_human(entry: dict) -> str:
    if entry.get("term") is None:
        return "未找到。可用术语：\n  " + "\n  ".join(entry["suggestions"])
    lines = [f"【{entry['term']}】"]
    if entry.get("matched_alias"):
        lines.append(f"  （由别名「{entry['matched_alias']}」匹配）")
    if entry.get("also"):
        lines.append(f"  别名：{' / '.join(entry['also'])}")
    lines.append(f"  释义：{entry.get('summary', '')}")
    if entry.get("detail"):
        lines.append(f"  说明：{entry['detail']}")
    lines.append(f"  证据层级：{entry.get('evidence_level', 'unknown')}")
    if entry.get("note"):
        lines.append(f"  注意：{entry['note']}")
    if entry.get("sources"):
        lines.append("  来源：")
        for s in entry["sources"]:
            lines.append(f"    - {s}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="tieban_open_tools",
        description="铁板神数·公开教学工具（零依赖，纯本地，不含私有算法）",
    )
    p.add_argument("--json", action="store_true", help="以 JSON 输出")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("ganzhi", help="公历年 -> 干支（例：ganzhi 1984）")
    s.add_argument("year", type=int)

    s = sub.add_parser("jiazi", help="六十甲子序号查询（例：jiazi 甲子）")
    s.add_argument("term")

    s = sub.add_parser("at", help="按序号取干支（例：at 1）")
    s.add_argument("n", type=int)

    s = sub.add_parser("term", help="传统术语查询（例：term 考刻）")
    s.add_argument("name")
    s.add_argument("--list", action="store_true", help="列出全部术语")

    s = sub.add_parser("check", help="条文编号格式校验（例：check 4082）")
    s.add_argument("num", type=int)

    s = sub.add_parser("cite", help="文献引用骨架（例：cite 皇极经世）")
    s.add_argument("work")

    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    try:
        if args.cmd == "ganzhi":
            gz = ganzhi_of_year(args.year)
            out = {
                "year": args.year,
                "ganzhi": gz,
                "tiangan_wuxing": TIANGAN_WUXING[gz[0]],
                "dizhi_wuxing": DIZHI_WUXING[gz[1]],
            }
            if args.json:
                _print_json(out)
            else:
                print(f"{args.year} 年 → {gz}")
                print(f"  天干 {gz[0]}（{TIANGAN_WUXING[gz[0]]}）· 地支 {gz[1]}（{DIZHI_WUXING[gz[1]]}）")
                print("  注：此处按公元 4 年为甲子年的通用算法换算；若用于命理，还需按立春分年。")

        elif args.cmd == "jiazi":
            n = jiazi_index(args.term)
            out = {"term": args.term, "index": n, "total": 60}
            if args.json:
                _print_json(out)
            else:
                print(f"{args.term} 是六十甲子第 {n} 位。")

        elif args.cmd == "at":
            gz = jiazi_at(args.n)
            out = {"index": args.n, "ganzhi": gz}
            if args.json:
                _print_json(out)
            else:
                print(f"第 {args.n} 位 → {gz}")

        elif args.cmd == "term":
            if args.list:
                entries = [{"term": k, "summary": v["summary"],
                            "evidence_level": v["evidence_level"]} for k, v in GLOSSARY.items()]
                if args.json:
                    _print_json(entries)
                else:
                    for e in entries:
                        print(f"{e['term']:<8} [{e['evidence_level']:<11}] {e['summary']}")
                return 0
            entry = show_term(args.name)
            if args.json:
                _print_json(entry)
            else:
                print(_term_human(entry))

        elif args.cmd == "check":
            out = check_verse_number(args.num)
            if args.json:
                _print_json(out)
            else:
                print(f"编号 {out['input']}：格式 {'通过' if out['format_ok'] else '不通过'}")
                if out["format_ok"]:
                    print(f"  所在集次：第 {out['volume_index']} 集")
                    print(f"  集内位置：第 {out['position_in_volume']} 位")
                print(f"  {out['note']}")

        elif args.cmd == "cite":
            text = cite(args.work)
            if args.json:
                _print_json({"work": args.work, "template": text})
            else:
                print(text)

    except ValueError as e:
        print(f"输入有误：{e}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())