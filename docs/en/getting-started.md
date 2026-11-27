---
title: "Getting Started with Tieban Shenshu"
description: "A reading order for newcomers: the three concepts you must not confuse, common pitfalls, and runnable local educational tools."
lang: en
layout: default
---

# Getting Started

> Five minutes to understand what this repository offers.

---

## 1. Which one are you?

| You are… | Go to |
|---|---|
| 🔍 Curious what Tieban Shenshu is | [§2](#2-if-you-are-just-curious) |
| 🛠 Want to run something | [§3](#3-if-you-want-to-run-something) |
| 📚 Researching texts and origins | [§4](#4-if-you-are-researching) |
| 🌐 Want to help translate or correct | [§5](#5-if-you-want-to-contribute) |
| 💼 Want the commercial product | [§6](#6-if-you-want-the-full-product) |

---

## 2. If you are just curious

**Three minutes**: read the [**Overview**](index.md) — what it is, how it differs from BaZi,
and which parts of its history are clear versus unknown.

**Two more minutes**: skim the [**Glossary**](glossary.md) — so that *kaoke*, *dingfen*, and
*tiaowen* stop being opaque.

**One question only?** The [**FAQ**](faq.md) has sixteen.

---

## 3. If you want to run something

### Requirements

**Python 3.9+ only.** No `pip install` needed.

```bash
python --version
```

### Run it

```bash
git clone https://github.com/tiebanshenshuapp-bot/tiebanshenshu.git
cd tiebanshenshu/demo
```

Then try these five:

```bash
# 1. What year is 1984?
python tieban_open_tools.py ganzhi 1984
# → 1984 年 → 甲子

# 2. Where does 甲子 sit in the 60-cycle?
python tieban_open_tools.py jiazi 甲子
# → 甲子 是六十甲子第 1 位。

# 3. What does "kaoke" actually mean?
python tieban_open_tools.py term 考刻

# 4. Is verse number 4082 well-formed?
python tieban_open_tools.py check 4082

# 5. How should I cite the Huangji Jingshi?
python tieban_open_tools.py cite 皇极经世
```

Note: outputs are in Chinese, since the subject matter and terminology are Chinese.
The `--json` flag gives machine-readable output you can process.

### Everything else

```bash
python tieban_open_tools.py --help
python tieban_open_tools.py term x --list     # list all terms
python tieban_open_tools.py --json ganzhi 1984
```

```json
{
  "year": 1984,
  "ganzhi": "甲子",
  "tiangan_wuxing": "木",
  "dizhi_wuxing": "水"
}
```

### Verify it does not phone home

```bash
grep -E "import.*(requests|urllib|socket)" tieban_open_tools.py
```

**Expect no output.** If there is output, that is a bug — please report it.

### Run the tests

```bash
python -m unittest discover -s tests -v
```

Expect `Ran 26 tests ... OK`.

---

## 4. If you are researching

Read [**Research Methods**](research-methods.md) first — our standards, citation format, and how
to evaluate our credibility.

Then [**History**](history.md) — timeline, key evidence, and which questions remain open.

Then **verify us independently**:

| To check | Look at |
|---|---|
| Yang Shen's criticism | *Sheng'an ji*, original text |
| Shao Yong's biography | *Song shi* (《宋史》) |
| *Huangji Jingshi* content | The text itself or an authoritative edition |
| Verse content | Your own manuscript or photoreprint |

We strongly encourage you **not to take us on trust**.

---

## 5. If you want to contribute

Easiest three contributions:

| Type | How |
|---|---|
| Report an error | Open an issue: which sentence, what is wrong, your source |
| Improve translation | Especially regional usage (Hong Kong / Taiwan) |
| Add bibliographic detail | Title + edition + page |

Read [**CONTRIBUTING.md**](../../CONTRIBUTING.md) first (10 minutes, prevents wasted work).

**Do not submit**: real birth data, personal names, reading reports, unattributed verse texts,
or content copied from non-commercial-licensed projects.

---

## 6. If you want the full product

This repository is a **research community**, not the commercial product.

| You need | Where |
|---|---|
| Complete verse corpus | Official website |
| Chart casting, kaoke | Official website |
| Generated reading reports | Official website |
| Free trial | https://tiebanshenshuapp.com/trial |

Official website: **https://tiebanshenshuapp.com**

---

## 7. Common snags

**"`python` not found"** — try `python3` (macOS/Linux) or `py` (Windows).

**"Chinese shows as mojibake"** — on Windows PowerShell:
```powershell
$env:PYTHONIOENCODING="utf-8"
```

**"`ganzhi 1984-01-15` gives 甲子 but another program says 癸亥"** — **not a bug.**
This tool converts by calendar year. The year pillar in practice changes at **Lichun** (立春),
so someone born in January 1984 still belongs to 1983 (癸亥). The tool flags this in its output.
See [FAQ Q11](faq.md).

**"Why doesn't it cast a BaZi chart?"** — because chart casting depends on Lichun boundaries
(to the minute, requiring astronomical calculation), true solar time (requiring birth coordinates),
and the zi-hour day boundary (23:00 vs 00:00, schools differ). Rather than ship a fake authority,
we state the boundary.

---

## 8. Next

| To go deeper | Go to |
|---|---|
| Full terminology | [Glossary](glossary.md) |
| Origins and debates | [History](history.md) |
| Our methodology | [Research methods](research-methods.md) |
| Contribute | [CONTRIBUTING.md](../../CONTRIBUTING.md) |
| Plans | [ROADMAP.md](../../ROADMAP.md) |

---

*Last updated: 2026-11-27*