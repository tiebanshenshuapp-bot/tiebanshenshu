#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tieban_open_tools 的测试。零依赖，只用标准库 unittest。

运行：
    cd demo
    python -m unittest discover -s tests -v
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import tieban_open_tools as T  # noqa: E402


class TestGanzhi(unittest.TestCase):
    """干支换算。基准：公元 4 年为甲子年。"""

    def test_known_years(self):
        # 公认锚点：1984 甲子、2024 甲辰、2026 丙午、1911 辛亥、1949 己丑
        self.assertEqual(T.ganzhi_of_year(1984), "甲子")
        self.assertEqual(T.ganzhi_of_year(2024), "甲辰")
        self.assertEqual(T.ganzhi_of_year(2026), "丙午")
        self.assertEqual(T.ganzhi_of_year(1911), "辛亥")
        self.assertEqual(T.ganzhi_of_year(1949), "己丑")

    def test_cycle_is_60(self):
        self.assertEqual(T.ganzhi_of_year(1984), T.ganzhi_of_year(1984 + 60))
        self.assertEqual(T.ganzhi_of_year(2000), T.ganzhi_of_year(2000 + 120))

    def test_ten_year_step_keeps_tiangan(self):
        # 天干周期 10：+10 年天干不变
        a = T.ganzhi_of_year(2000)
        b = T.ganzhi_of_year(2010)
        self.assertEqual(a[0], b[0], f"{a} -> {b} 天干应相同")

    def test_twelve_year_step_keeps_dizhi(self):
        # 地支周期 12：+12 年地支不变
        a = T.ganzhi_of_year(2000)
        b = T.ganzhi_of_year(2012)
        self.assertEqual(a[1], b[1], f"{a} -> {b} 地支应相同")

    def test_rejects_non_positive(self):
        with self.assertRaises(ValueError):
            T.ganzhi_of_year(0)
        with self.assertRaises(ValueError):
            T.ganzhi_of_year(-5)


class TestJiazi(unittest.TestCase):
    """六十甲子序号，双向一致。"""

    def test_boundaries(self):
        self.assertEqual(T.jiazi_index("甲子"), 1)
        self.assertEqual(T.jiazi_index("癸亥"), 60)

    def test_roundtrip_all_60(self):
        for n in range(1, 61):
            gz = T.jiazi_at(n)
            self.assertEqual(T.jiazi_index(gz), n, f"roundtrip failed at {n}: {gz}")

    def test_rejects_invalid_length(self):
        with self.assertRaises(ValueError):
            T.jiazi_index("甲")
        with self.assertRaises(ValueError):
            T.jiazi_index("甲子丑")

    def test_rejects_unknown_char(self):
        with self.assertRaises(ValueError):
            T.jiazi_index("AB")

    def test_rejects_yin_yang_mismatch(self):
        # 甲(阳) + 丑(阴) 在六十甲子中不存在
        with self.assertRaises(ValueError):
            T.jiazi_index("甲丑")

    def test_out_of_range_index(self):
        with self.assertRaises(ValueError):
            T.jiazi_at(0)
        with self.assertRaises(ValueError):
            T.jiazi_at(61)


class TestVerseNumberCheck(unittest.TestCase):
    """编号格式校验：只校验格式，不返回内容。"""

    def test_in_range(self):
        r = T.check_verse_number(4082)
        self.assertTrue(r["format_ok"])
        self.assertEqual(r["volume_index"], 4)
        self.assertEqual(r["position_in_volume"], 82)

    def test_lower_boundary(self):
        r = T.check_verse_number(1001)
        self.assertTrue(r["format_ok"])
        self.assertEqual(r["volume_index"], 1)
        self.assertEqual(r["position_in_volume"], 1)

    def test_upper_boundary(self):
        r = T.check_verse_number(13000)
        self.assertTrue(r["format_ok"])
        self.assertEqual(r["volume_index"], 12)
        self.assertEqual(r["position_in_volume"], 1000)

    def test_out_of_range(self):
        self.assertFalse(T.check_verse_number(1000)["format_ok"])
        self.assertFalse(T.check_verse_number(0)["format_ok"])
        self.assertFalse(T.check_verse_number(99999)["format_ok"])

    def test_never_leaks_verse_text(self):
        """硬性检查：结果中不得出现任何疑似条文正文的字段。"""
        r = T.check_verse_number(4082)
        forbidden = {"text", "verse", "content", "tiaowen", "judgement", "断语"}
        self.assertEqual(forbidden & set(r.keys()), set(),
                         "编号校验不得返回条文内容")


class TestGlossary(unittest.TestCase):
    """术语表：结构完整、证据层级合法。"""

    VALID_LEVELS = {"classical", "traditional", "scholarly", "editorial"}

    def test_all_entries_have_required_keys(self):
        for k, v in T.GLOSSARY.items():
            self.assertIn("summary", v, f"{k} 缺 summary")
            self.assertIn("evidence_level", v, f"{k} 缺 evidence_level")
            self.assertIn(v["evidence_level"], self.VALID_LEVELS,
                          f"{k} 的 evidence_level 非法: {v['evidence_level']}")

    def test_alias_lookup(self):
        r = T.show_term("鐵板神數")
        self.assertEqual(r["term"], "铁板神数")
        self.assertEqual(r["matched_alias"], "鐵板神數")

    def test_unknown_term_returns_suggestions(self):
        r = T.show_term("这不是术语")
        self.assertIsNone(r["term"])
        self.assertTrue(len(r["suggestions"]) > 0)

    def test_no_private_algorithm_marker(self):
        """术语表不得包含私有配值表或取数公式。"""
        blob = repr(T.GLOSSARY)
        for word in ["取数公式", "配值表", "秘数表", "本命基数"]:
            self.assertNotIn(word, blob, f"术语表疑似含私有算法线索: {word}")


class TestCite(unittest.TestCase):

    def test_known_work(self):
        out = T.cite("皇极经世")
        self.assertIn("邵雍", out)
        self.assertIn("补", out)  # 必须提醒补全版本信息

    def test_unknown_work_gives_template(self):
        out = T.cite("某未知名古籍")
        self.assertIn("某未知名古籍", out)
        self.assertIn("版本", out)


class TestCli(unittest.TestCase):
    """CLI 层：返回值正确。"""

    def test_ganzhi_cli(self):
        self.assertEqual(T.main(["ganzhi", "1984"]), 0)

    def test_json_flag(self):
        self.assertEqual(T.main(["--json", "jiazi", "甲子"]), 0)

    def test_bad_input_returns_2(self):
        self.assertEqual(T.main(["jiazi", "甲丑"]), 2)
        self.assertEqual(T.main(["at", "0"]), 2)

    def test_all_subcommands_have_help(self):
        for cmd in ["ganzhi", "jiazi", "at", "term", "check", "cite"]:
            with self.assertRaises(SystemExit) as cm:
                T.main([cmd, "--help"])
            self.assertEqual(cm.exception.code, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)