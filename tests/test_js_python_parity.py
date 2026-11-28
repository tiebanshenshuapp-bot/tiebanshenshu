#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网页工具与命令行工具的一致性测试 / JS-Python Parity Test

网页版（docs/tools/tools.js）与命令行版（demo/tieban_open_tools.py）
必须使用同一套规则，结果完全一致。

本测试用 Node 执行 JS，与 Python 输出逐项比对。

需要：node（可选，缺失时跳过并返回 0）

用法：
    cd <repo root>
    python tests/test_js_python_parity.py

退出码：0 一致或跳过 / 1 不一致 / 2 环境错误
"""

import io
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NODE_DRIVER = r'''
const fs = require("fs");
const path = require("path");

function fakeEl(id){return{id:id,value:"",_html:"",dataset:{},style:{},
  get innerHTML(){return this._html},set innerHTML(v){this._html=v},
  addEventListener(){},closest(){return null}};}
const EL={};
global.document={readyState:"complete",
  getElementById(i){if(!EL[i])EL[i]=fakeEl(i);return EL[i]},addEventListener(){}};
global.window={};

const jsPath = path.join(process.cwd(), "docs", "tools", "tools.js");
const src = fs.readFileSync(jsPath, "utf8");
const patched = src.replace(
  'if (document.readyState === "loading")',
  "global.__T={ganzhiOfYear,jiaziIndex,jiaziAt,checkVerseNumber,cite,convCompare,ganzhiRelation};\n" +
  'if (document.readyState === "loading")'
);
eval(patched);
const T = global.__T;
const out = {};

out.ganzhi = [1,4,60,100,1900,1911,1949,1984,2000,2024,2026,9999]
  .map(y => [y, T.ganzhiOfYear(y)]);

const terms = [];
for (let n = 1; n <= 60; n++) terms.push(T.jiaziAt(n));
out.jiaziAt = terms;
out.jiaziIndex = terms.map(t => T.jiaziIndex(t));

out.check = [1000,1001,13000,13001,4082,0,99999].map(n => {
  try { return [n, T.checkVerseNumber(n)]; } catch (e) { return [n, "ERR"]; }
});

out.cite = ["皇极经世","太玄经","升庵集","某未知名古籍"].map(w => [w, T.cite(w)]);

out.badJiazi = ["甲丑","甲","AB","甲子丑"].map(t => {
  try { return [t, T.jiaziIndex(t)]; } catch (e) { return [t, "ERR"]; }
});

out.he = [["甲子","己丑"],["乙丑","庚子"],["丙寅","辛丑"],["丁卯","壬寅"],["戊辰","癸卯"],
          ["甲","己"],["乙","庚"],["丙","辛"],["丁","壬"],["戊","癸"]].map(p => {
  try { return [p[0]+"/"+p[1], T.ganzhiRelation(p[0], p[1])]; }
  catch (e) { return [p[0]+"/"+p[1], "ERR"]; }
});

out.chong = [["甲子","甲午"],["乙丑","乙未"],["丙寅","丙申"],
             ["丁卯","丁酉"],["戊辰","戊戌"],["己巳","己亥"]].map(p => {
  try { return [p[0]+"/"+p[1], T.ganzhiRelation(p[0], p[1])]; }
  catch (e) { return [p[0]+"/"+p[1], "ERR"]; }
});

out.liuhe = [["甲子","乙丑"],["丙寅","丁亥"],["戊辰","己酉"]].map(p => {
  try { return [p[0]+"/"+p[1], T.ganzhiRelation(p[0], p[1])]; }
  catch (e) { return [p[0]+"/"+p[1], "ERR"]; }
});

out.sanhe = [["甲申","甲子"],["乙亥","乙卯"],["丙寅","丙午"],["丁巳","丁酉"]].map(p => {
  try { return [p[0]+"/"+p[1], T.ganzhiRelation(p[0], p[1])]; }
  catch (e) { return [p[0]+"/"+p[1], "ERR"]; }
});

out.neutral = [["甲子","乙卯"]].map(p => {
  try { return [p[0]+"/"+p[1], T.ganzhiRelation(p[0], p[1])]; }
  catch (e) { return [p[0]+"/"+p[1], "ERR"]; }
});

out.conv = T.convCompare("铁板神数 考刻 定分 条文 太玄数");

console.log(JSON.stringify(out));
'''


def has(lines, kw):
    return any(kw in x for x in lines)


def main():
    if not os.path.isdir(os.path.join(ROOT, "demo")):
        print("错误：请在仓库根目录运行", file=sys.stderr)
        return 2

    try:
        subprocess.run(["node", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, OSError, subprocess.CalledProcessError):
        print("跳过：未安装 node（JS-Python 一致性测试需要 node）")
        return 0

    js_file = os.path.join(ROOT, "docs", "tools", "tools.js")
    py_file = os.path.join(ROOT, "demo", "tieban_open_tools.py")
    for f in (js_file, py_file):
        if not os.path.exists(f):
            print(f"错误：缺少 {f}", file=sys.stderr)
            return 2

    tmpdir = tempfile.mkdtemp()
    driver = os.path.join(tmpdir, "_parity.cjs")
    io.open(driver, "w", encoding="utf-8").write(NODE_DRIVER)

    r = subprocess.run(["node", driver], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=ROOT)
    if r.returncode != 0:
        print("Node 执行失败：", r.stderr[:800], file=sys.stderr)
        return 1

    js = json.loads(r.stdout)

    sys.path.insert(0, os.path.join(ROOT, "demo"))
    import tieban_open_tools as P

    errors = []
    checks = 0

    for y, gz in js["ganzhi"]:
        checks += 1
        if P.ganzhi_of_year(y) != gz:
            errors.append(f"ganzhi({y}): py={P.ganzhi_of_year(y)} js={gz}")

    for i, gz in enumerate(js["jiaziAt"], start=1):
        checks += 1
        if P.jiazi_at(i) != gz:
            errors.append(f"jiaziAt({i}): py={P.jiazi_at(i)} js={gz}")

    for gz, idx in zip(js["jiaziAt"], js["jiaziIndex"]):
        checks += 1
        if P.jiazi_index(gz) != idx:
            errors.append(f"jiaziIndex({gz}): py={P.jiazi_index(gz)} js={idx}")

    for n, rr in js["check"]:
        checks += 1
        if rr == "ERR":
            try:
                P.check_verse_number(n)
                errors.append(f"check({n}): js 报错但 py 成功")
            except Exception:
                pass
            continue
        pr = P.check_verse_number(n)
        if pr["format_ok"] != rr["ok"]:
            errors.append(f"check({n}).ok 不一致")
        if pr["format_ok"]:
            if pr["volume_index"] != rr["volumeIndex"]:
                errors.append(f"check({n}).volume_index 不一致")
            if pr["position_in_volume"] != rr["positionInVolume"]:
                errors.append(f"check({n}).position 不一致")

    for w, jt in js["cite"]:
        checks += 1
        if P.cite(w) != jt:
            errors.append(f"cite({w}) 不一致")

    for t, rr in js["badJiazi"]:
        checks += 1
        if rr == "ERR":
            try:
                P.jiazi_index(t)
                errors.append(f"badJiazi({t}): js 报错但 py 未报错")
            except Exception:
                pass

    expect_he = {
        "甲子/己丑": "化土", "乙丑/庚子": "化金", "丙寅/辛丑": "化水",
        "丁卯/壬寅": "化木", "戊辰/癸卯": "化火",
        "甲/己": "化土", "乙/庚": "化金", "丙/辛": "化水",
        "丁/壬": "化木", "戊/癸": "化火",
    }
    for pair, lines in js["he"]:
        checks += 1
        want = expect_he.get(pair)
        if not want:
            continue
        if lines == "ERR" or not has(lines, "五合") or not has(lines, want):
            errors.append(f"五合 {pair} 不符：{lines}")

    for pair, lines in js["chong"]:
        checks += 1
        if not has(lines, "→ 六冲"):
            errors.append(f"六冲 {pair} 未识别：{lines}")

    for pair, lines in js["liuhe"]:
        checks += 1
        if not has(lines, "→ 六合"):
            errors.append(f"六合 {pair} 未识别：{lines}")

    for pair, lines in js["sanhe"]:
        checks += 1
        if not has(lines, "三合："):
            errors.append(f"三合 {pair} 未识别：{lines}")

    for pair, lines in js["neutral"]:
        checks += 1
        if has(lines, "→ 六冲") or has(lines, "→ 六合") or has(lines, "三合："):
            errors.append(f"{pair} 不应有冲合：{lines}")

    checks += 1
    if js["conv"]["diffCount"] < 3:
        errors.append(f"繁简对照差异过少：{js['conv']['diffCount']}")

    print(f"一致性检查：{checks} 项")
    if errors:
        print(f"\n[FAIL] {len(errors)} 处不一致：")
        for e in errors[:25]:
            print("  " + e)
        return 1

    print("[PASS] 网页版与命令行版结果完全一致；干支关系语义正确")
    return 0


if __name__ == "__main__":
    sys.exit(main())
