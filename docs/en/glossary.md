---
title: "Tieban Shenshu Glossary"
description: "Terminology index for Tieban Shenshu: kaoke, dingfen, tiaowen, taixuan numbers, yuantang and gua-qi, each with an evidence grade."
lang: en
layout: default
---

# Glossary

> Every entry carries an **evidence level**. See [the legend](#evidence-levels).
> Found an error? Open an issue.

---

## A. The system and its names

### Tieban Shenshu (鐵板神數)
**Evidence level**: scholarly discussion

A Qing-dynasty Chinese divination system attributed by tradition to Shao Yong (邵雍, 1011–1077)
of the Northern Song. Known for **kaoke** — narrowing a birth time to a specific *ke* — and for
mapping derived numbers to numbered verses.

Variant writing: **鐵版神數** (版 and 板 are interchangeable here).

Common English renderings: "Tieban Shenshu", "Tie Ban Shen Shu", "Iron Plate Divine Numbers".
The last is a literal translation, not an established academic term.

> **Note**: naming is not standardised across schools or regions. A different name does not imply
> a different lineage, and an identical name does not imply identical content.

---

### Tie Buzi / Tie Daoren (鐵卜子 / 鐵道人)
**Evidence level**: traditional account

A figure said to have revised the verses during the Qianlong–Jiaqing period (1736–1820), from whom
the "Tie ban" (Iron Plate edition) name is said to derive.

**Problem**: his name, dates, birthplace, and even existence have **no reliable primary source**.
He leaves no trace in contemporaneous records — which is itself suspicious for someone said to have
revised twelve thousand verses.

---

### Chunzi shu / Dading shu (蠢子數 / 大定數)
**Evidence level**: scholarly discussion

Two names mentioned in Ming-dynasty criticism, generally considered early forms of, or cognate with,
Tieban Shenshu.

Yang Shen (楊慎, 1488–1559), *Sheng'an ji* (《升庵集》):

> "Nowadays wandering diviners recklessly fabricate the *Dading shu* and *Chunzi shu*,
> falsely attributing them to Kangjie — is this not a grave slander of a former worthy?"

This is the earliest explicit criticism currently traceable.

---

## B. Core operations

### Kaoke (考刻)
**Evidence level**: traditional account

Subdividing the birth hour into *ke* (刻), then using known life facts — chiefly family
information — as cross-checks to determine the correct *ke*.

**Basic framework** (details vary by school):

```
1 shichen (時辰) = 2 hours
      ↓ divide into 8
1 ke (刻) = 15 minutes
      ↓ subdivide into 15
1 fen (分) = 1 minute
```

> **Important**: the framework above is the **general traditional scheme** found in many texts.
> But *which* family details are used, *how* they map, and *how* candidates are ranked
> differ between schools. There is **no single authoritative standard**.

---

### Dingfen (定分)
**Evidence level**: traditional account

Subdividing within an established *ke* to reach a *fen*.

Together with *kaoke*, this forms **考刻定分** — the most distinctive operation in the system.

**Contested point**: the specific fifteen-part correspondence tables are transmitted privately.
Published accounts disagree. This project **publishes no such table**.

---

### Qishu (起數) — number derivation
**Evidence level**: traditional account

The process of converting the four pillars into a number.

Commonly described as:

```
Four pillars → assign numbers → derive hexagram → extract number → verse ID
```

**Note**: the specific assignments, hexagram rules, and extraction formulas are **privately
transmitted or proprietary**. Sources differ substantially. This project implements none of them.

---

### Taixuan shu (太玄數)
**Evidence level**: traditional account

One number-assignment scheme possibly used in derivation, related to the numerology of Yang Xiong's
*Taixuan jing* (《太玄經》).

**What is public**: only the concept that certain stems/branches map to certain numbers.
**What is not**: the specific values — accounts differ.

> Our educational tool therefore **does not implement** taixuan assignment.

---

## C. Output form

### Tiaowen (條文) — verses
**Evidence level**: scholarly discussion

Numbered verses — the final output form of the system.

**Traditional scale**: commonly said to be about twelve thousand verses, divided by earthly branch
into twelve volumes (子集 through 亥集).

**Numbering**: the range 1001–13000 is often cited in public discussion, but **manuscripts differ**.

**Important facts**:

- There is **no critical edition**
- Manuscript copies **differ in wording**
- **No** scholarly consensus edition exists

> Treat any claim of "the one correct version" with scepticism.

---

### Mingshu (命書) — reading report
**Evidence level**: traditional account

The full written reading produced by the system, usually comprising verses across several categories.

> This project **does not generate reading reports** and provides no personal analysis.

---

## D. Related but distinct systems

### Huangji Jingshi (皇極經世)
**Evidence level**: classical text

Shao Yong's major work, computing historical and cosmic cycles in *yuan, hui, yun, shi*
(元會運世). It belongs to Yijing studies and historical philosophy.

**Relationship to Tieban Shenshu**:

- Tradition says Tieban Shenshu "borrows" its numerological concepts
- But the two are **not the same system**
- Equating them is an **oversimplification**

> *Huangji Jingshi* itself is **public domain** and free to read and cite.

---

### Sizhu (四柱) — Four Pillars / BaZi
**Evidence level**: classical text

Year, month, day, and hour pillars, each a heavenly stem plus an earthly branch — eight characters
in total, hence *bazi* (八字).

**Critical boundary settings** (sources differ):

| Pillar | Boundary rule |
|---|---|
| Year | Begins at **Lichun** (立春, start of spring), not 1 January or lunar new year |
| Month | Begins at **solar terms**, not lunar month boundaries |
| Day | Changes at **zi hour** (23:00 or 00:00 — schools differ) |
| Hour | **True solar time** vs standard time — schools differ |

> ⚠️ These four settings alone can produce **different charts for the same person**.
> If two programs disagree, check these first.

---

### Liuqin (六親) — six relations
**Evidence level**: classical text

Traditionally father, mother, siblings, spouse, children (or the four categories: parents, siblings,
spouse, children).

In *kaoke*, relatives' zodiac signs and counts serve as **verification anchors**.

---

## E. Tools and formats

### Sixty-year cycle (六十甲子)
**Evidence level**: classical text

Ten heavenly stems combine with twelve earthly branches; yin–yang pairing yields exactly 60
combinations, cycling indefinitely.

```bash
python tieban_open_tools.py jiazi 甲子     # → position 1
python tieban_open_tools.py at 60          # → 癸亥
```

---

### Heavenly stem combinations (天干五合)
**Evidence level**: classical text

| Pair | Transforms to |
|---|---|
| 甲己 | Earth |
| 乙庚 | Metal |
| 丙辛 | Water |
| 丁壬 | Wood |
| 戊癸 | Fire |

---

### Earthly branch clashes (地支六沖)
**Evidence level**: classical text

子午 · 丑未 · 寅申 · 卯酉 · 辰戌 · 巳亥

---

### Earthly branch trines (地支三合)
**Evidence level**: classical text

| Combination | Formation |
|---|---|
| 申子辰 | Water |
| 亥卯未 | Wood |
| 寅午戌 | Fire |
| 巳酉丑 | Metal |

---

## Evidence levels

| Label | Meaning |
|---|---|
| **Classical text** | Traceable to a Qing-era or earlier edition; public domain |
| **Traditional account** | Lineage claims, folklore — **not fact** |
| **Scholarly discussion** | Verifiable philological research; disagreement allowed |
| **Editorial note** | Our own arrangement |
| **Synthetic sample** | Fabricated for demonstration; clearly marked |

---

## Contributing

Found an error, a missing term, or a mislabelled evidence level?

Open an issue stating: (1) which entry, (2) what you believe is correct, (3) **your source**
(book, edition, page, or link).

Claims without a source cannot be adopted, but we welcome pointers telling us where to look.

---

*Last updated: 2026-11-27*