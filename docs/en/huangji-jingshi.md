---
title: "What is Huangji Jingshi? Shao Yong's Yuan-Hui-Yun-Shi System"
description: "Huangji Jingshi (皇極經世) is Shao Yong's Northern Song treatise computing historical cycles in yuan, hui, yun, and shi. This page explains the framework, its actual relationship to Tieban Shenshu, and open-source implementations."
lang: en
layout: default
---

# What is Huangji Jingshi (皇極經世)?

> This text is often cited to claim "Tieban Shenshu derives from the Huangji Jingshi."
> What is the actual relationship? This page explains.

---

## 1. In one sentence

**Huangji Jingshi** (皇極經世, "Book of Supreme World Ordering Principles") is the major work of
**Shao Yong** (邵雍, 1011–1077) of the Northern Song, computing historical and cosmic cycles in
units of *yuan* (元), *hui* (會), *yun* (運), and *shi* (世).

It is a work of **historical philosophy** — **not** a manual for predicting individual lives.

> Evidence level: **classical text**. That Shao Yong wrote the *Huangji Jingshi* is established
> history (see the *Song shi* biography).

---

## 2. The framework: yuan, hui, yun, shi

This is the most frequently quoted part of the book.

```
1 yuan (元)  = 12 hui (會)
1 hui        = 30 yun (運)
1 yun        = 12 shi (世)
1 shi        = 30 years

Therefore:
1 yuan = 12 × 30 × 12 × 30 = 129,600 years
1 hui  = 30 × 12 × 30      = 10,800 years
1 yun  = 12 × 30           = 360 years
1 shi  = 30 years
```

### What the framework does

Shao Yong uses these ratios to compress **extremely long time spans** into workable cycles,
assigns hexagrams to each cycle, and uses hexagram transitions to explain historical rise and fall.

Its position in Chinese intellectual history:

- It brings "history" into the framework of Yijing numerology
- It attempts to find a "calculable rhythm" in history
- It is **speculative historical philosophy**, not empirical historiography

### Common misconceptions

| Misconception | Fact |
|---|---|
| "129,600 years is a cosmic cycle that will destroy the world" | This is a **theoretical unit**, not a physical prophecy |
| "Huangji Jingshi can predict an individual's fate" | Its object is **history and eras**, not individuals |
| "Computing the cycles tells you the future" | It is an **interpretive framework**, not a predictive tool |

---

## 3. Who was Shao Yong?

| Item | Detail |
|---|---|
| Dates | 1011–1077 |
| Courtesy name | Yaofu (堯夫) |
| Posthumous name | Kangjie (康節) — hence "Shao Kangjie" |
| Era | Northern Song |
| Role | Neo-Confucian scholar, Yijing specialist |
| Standing | One of the "Five Masters of Northern Song" |

His intellectual signature: **using numerical patterns to connect cosmos, history, and human affairs.**

This orientation deeply influenced later divination systems — **including Tieban Shenshu**.

---

## 4. The relationship to Tieban Shenshu (important)

This is where confusion is most common. Three layers:

### Layer 1: Numerical concepts were indeed borrowed

Tieban Shenshu is traditionally called "皇極經世鐵版神數," and its naming and some terminology
(such as *huangji*, "value hexagram") do come from Shao Yong's system.

> Evidence level: **traditional account**. To what extent borrowing occurred lacks systematic study.

### Layer 2: But they are not the same system

| Dimension | Huangji Jingshi | Tieban Shenshu |
|---|---|---|
| Object of computation | History, eras | Individuals |
| Basic units | yuan/hui/yun/shi (10,000-year scale) | ke/fen (minute scale) |
| Output form | Hexagram transitions, historical periods | Numbered verses |
| Purpose | Explain historical rhythm | Describe individual circumstances |

**The scales differ by roughly ten orders of magnitude** (1 yuan = 129,600 years, while ke/fen are measured in minutes), **and the purposes are entirely different.**

Treating them as one thing is a fundamental category error.

### Layer 3: The attribution problem

Tieban Shenshu is **attributed to** Shao Yong. But:

- There is **no** record of Tieban Shenshu in Song-dynasty sources
- As early as the Ming, Yang Shen criticised "wandering diviners recklessly fabricating the
  *Dading shu* and *Chunzi shu*, falsely attributing them to Kangjie"

So: **"personally transmitted by Shao Yong" lacks documentary support.**

See [History and debates](history.md).

### One sentence

> Tieban Shenshu **borrowed the branding and some concepts** of the Huangji Jingshi,
> but it is **not** the Huangji Jingshi method, and **not** written by Shao Yong.

---

## 5. How scholarship views it

### Affirmative

- The *Huangji Jingshi* is an **important document in Song intellectual history**
- The yuan-hui-yun-shi framework reflects **ancient cosmological and historical imagination**
- It influenced later Yijing studies, divination, and even some modern cyclical theories of history

### Critical

- Its historical periodisation **lacks empirical grounding**
- The method of "matching hexagrams to history" is **not testable**
- It contains substantial **later interpolation**, mixing authentic and spurious material

**In short**: worth studying as intellectual history; lacking empirical foundation as a tool for
explaining history.

---

## 6. If you want to read the original

### A note on editions

The *Huangji Jingshi* is voluminous, with many commentaries across dynasties. Common types:

| Type | Note |
|---|---|
| Original editions | Need to check specific imprints (Song printings are rare; most are Ming/Qing) |
| Commentaries | Many across dynasties, of uneven quality |
| Modern collations | Exist, but verify the quality of the collation |

> ⚠️ **Always cite the edition.** Content differs substantially between editions; this is a
> basic requirement for research on this text.

### Suggested entry path

Do not start with the original. Suggested order:

1. Understand Shao Yong's intellectual context (Northern Song Neo-Confucianism)
2. Learn the basic yuan-hui-yun-shi framework (given above)
3. Pick a reliable commentary or research monograph
4. Then return to the original

---

## 7. Open-source implementations (engineering view)

If you want to **implement** Huangji Jingshi computations in code, here is our survey:

**✅ Usable commercially (MIT)**: `Ryanlyly-ai/huangji-jingshi`
- TypeScript, self-described as an "auditable, testable yuan-hui-yun-shi era computation algorithm"
- MIT licence, commercially usable

**❌ Not recommended**:
- `kentang2017/kinwangji` (16★) — no licence, legally unusable
- `jiaguoxinzhi/HuangjiJingshi` — GPL-3.0, copyleft

> Full survey: [Huangji Jingshi and Tieban Shenshu open-source survey](https://github.com/tiebanshenshuapp-bot/tiebanshenshu/blob/main/research/huangji-jingshi-opensource.md).

---

## 8. One-line summary

> **Huangji Jingshi** is Shao Yong's work computing historical rhythm through
> yuan-hui-yun-shi; it is historical philosophy.
> Tieban Shenshu **borrowed its branding and some concepts**, but the two differ in
> **scale, purpose, and method**.
> "Personally transmitted by Shao Yong" lacks documentary support.
> To study it, read the original and cite the edition; to implement it, MIT has a usable algorithm.

---

## Further reading

| Topic | Page |
|---|---|
| Origins of Tieban Shenshu | [History and debates](history.md) |
| Terminology | [Glossary](glossary.md) |
| Accuracy | [An honest analysis](accuracy.md) |
| Kaoke | [Kaoke and dingfen](kaoke.md) |
| Open-source survey | [Huangji Jingshi survey](https://github.com/tiebanshenshuapp-bot/tiebanshenshu/blob/main/research/huangji-jingshi-opensource.md) |

---

*Evidence levels: "classical text" refers to the established fact that Shao Yong wrote the book;
"traditional account" refers to the attribution and borrowing claims; "scholarly discussion"
refers to academic assessments.*
*This page contains no transcription of any specific edition.*