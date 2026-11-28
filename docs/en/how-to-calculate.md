---
title: "How Tieban Shenshu Is Calculated"
description: "How Tieban Shenshu works: chart casting, true solar time, kaoke hour calibration, clause lookup and book compilation. Method only — no clause text."
lang: en
layout: default
---

# How Tieban Shenshu Is Calculated

People searching "how does Tieban Shenshu work" or "Tieban Shenshu calculation"
want the method. This page explains the **process only**. It contains no classical
clause text and makes no prediction about any individual.

---

## One-sentence summary

Tieban Shenshu does not "analyse a chart". It **derives a set of numbers from the birth
time, then looks up the clauses indexed by those numbers**.

So the whole process reduces to two things:

1. **Get the birth time right** — chart casting, true solar time, hour calibration
2. **Look up clauses by the derived numbers** — derivation is algorithm, clauses are source text

If any step drifts, the numbers change, and every clause changes with them.

---

## The five steps

### Step 1 — Record the birth data

| Field | Why it is required |
|---|---|
| Birth date | Determines year, month and day pillars |
| Birth time (to the minute) | Determines the hour pillar and enters hour calibration |
| Birth longitude | Used for true solar time correction |
| Sex | Some derivation rules depend on it |

**Most common mistake**: people remember "around such-and-such o'clock".
Tieban Shenshu subdivides the hour into *ke* and *fen*, so an uncertain minute
must be resolved in step 3.

### Step 2 — Cast the chart (four pillars + true solar time)

1. Cast the **four pillars** from date and time
2. Correct to **true solar time** using birth longitude (about 4 minutes per degree)
3. Determine the hour branch from the corrected time

**Why this matters**: China spans roughly 62 degrees of longitude, more than four hours
of solar offset. Without correction, a western-born person's hour pillar can be off by
two full hours — and every subsequent number with it.

### Step 3 — Hour calibration (kaoke) using known family facts

This is what distinguishes Tieban Shenshu from other systems.

1. The initial pass yields **multiple candidates**
2. You enter **known family facts** (for example, parents' zodiac signs)
3. Those facts **narrow the candidates** to the one consistent with them
4. The result is a unique *ke* and *fen*

This is not guessing — it uses **verifiable facts** to infer the most likely finer time.
If facts are insufficient, candidates cannot converge and one should not force a result.

### Step 4 — Derive clause numbers

- Four pillars, *ke*, *fen* and related parameters map to **clause numbers** by fixed rules
- The tradition refers to roughly **twelve thousand clauses** — this is where the
  phrase "Tieban Shenshu 12,000 clauses" comes from
- The same clause is applied differently across calibrations

> The derivation rules themselves are the **core algorithm** and are not disclosed in
> public materials. Be cautious with any source claiming to hand you "the complete
> algorithm for free".

### Step 5 — Compile the book

- Clauses are arranged into volumes following the traditional format
- Each clause is labelled with its number and source
- The result is a readable, exportable reading

---

## What cannot be skipped

| Step | Consequence of skipping |
|---|---|
| True solar time correction | Hour pillar wrong for most longitudes |
| Hour calibration | Unconverged candidates — clauses may not match the person |
| Locking calibration before lookup | Same clause behaves differently across calibrations |
| Labelling sources | No way to audit or verify |

---

## Common misconceptions

**"Tieban Shenshu is the same as Bazi."** No. Bazi produces structural analysis;
Tieban Shenshu produces numbered clauses. Different methods, different outputs.

**"I can just self-test online."** Most "self-test" tools only cast the chart —
no calibration convergence, no real clause corpus. **Chart casting is not Tieban Shenshu.**

**"A clause can be read on its own."** No. The same number is applied differently
depending on calibration and family-fact checks.

**"There is an AI that can just tell me my clauses."** AI can explain terminology and
organise knowledge, but it cannot perform your calibration, and it cannot guarantee
the clauses correspond to your real calibration.

---

## See the process yourself

This site ships runnable local education tools that never upload your birth data:

- [Getting started](getting-started.html)
- [Glossary](glossary.html) — precise definitions of kaoke, dingfen, chart casting, clauses
- [Research methods](research-methods.html)

---

## Evidence grading

| Claim | Grade |
|---|---|
| The five-step process and its order | Verifiable (consistent across public sources) |
| Necessity of true solar time | Verifiable (astronomy) |
| Calibration by family facts | Traditional + our own testing |
| "Roughly 12,000 clauses" | Traditional figure (counts differ by edition) |
| Derivation rule details | **Core algorithm — not disclosed here** |

---

> Official site: [tiebanshenshuapp.com](https://tiebanshenshuapp.com?utm_source=github&utm_medium=referral&utm_campaign=tieban_community&utm_content=readme_link) ｜
> [Free trial](https://tiebanshenshuapp.com/trial?utm_source=github&utm_medium=referral&utm_campaign=tieban_community&utm_content=trial_cta)
