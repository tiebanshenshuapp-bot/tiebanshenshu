# FAQ

## About this project

### Q1: Is this repository official? How does it relate to the website?

This is the **officially maintained public research community**. It is **not** the commercial product:

| | This repository | Official website |
|---|---|---|
| Nature | Public research and educational demos | Commercial service |
| Content | Introductions, terminology, tools, bibliography | Full features, reading generation |
| Verse corpus | A few attributed excerpts (≤30) | Complete |
| Algorithms | Basic public conversions only | Full private implementation |
| Cost | Free | Per website policy |

Official site: https://tiebanshenshuapp.com

---

### Q2: Can I get a free reading here?

**No.** This repository provides no personal divination of any kind.

Two reasons: (1) we are a **textual research project**, not a reading service;
(2) the full algorithm is not here — the tool performs only basic conversions.

For the full service, use the free trial on the official website:
https://tiebanshenshuapp.com/trial

---

### Q3: Why not open source everything?

Three reasons, in order of importance:

**1. It is a commercial product.** The complete algorithm, verse corpus, and report system
are substantial assets. Open source by definition permits anyone — including competitors —
to use them freely.

**2. We do not have the right.** Some content derives from traditional transmission and internal
collation; we cannot unilaterally publish all of it.

**3. Openness does not prevent copying.** Published source can be repackaged. The real protection
is not hiding code but continuing to build a good product.

We chose **Source Available** — read it, learn from it, comment on it, but do not sell it.

---

### Q4: Then why publish anything?

Full closure helps nobody:

- People seeking reliable introductory material find none
- Researchers cannot check our claims
- The community cannot correct our errors

Publishing a portion buys **credibility, correction, and reach to those who need it.**

---

## About the content

### Q5: Why is there no critical edition of the verses?

That is an **objective fact**, not our failing. The corpus circulated in many manuscripts with
divergent wording, due to: hand-copying error, deliberate editorial changes, mixing of sources,
and the absence of any authoritative collation.

### Q6: Why not publish the complete corpus?

**Commercial**: it is core product asset.
**Rights**: public transcriptions may be protectable compilations, and some forbid commercial use.
**Quality**: with no critical edition, publishing "one school's version" invites the misreading
that it is the standard.

### Q7: I own an old book. Can I contribute it?

Welcome, but check three things first:
1. **Rights**: pre-1912 editions are usually public domain, but **modern collation, annotation,
   and photoreprints** may carry new copyright.
2. **What to send**: bibliographic information is more valuable than uploading a full scan.
3. **Do not upload entire books** — provide index-level information first.

### Q8: What does "traditional account" mean?

It means: **a claim that circulates, which we cannot prove.**

| Claim | Label | Why |
|---|---|---|
| "Tie Buzi revised the corpus in the Qing" | Traditional account | No reliable record of this person |
| "Personally transmitted by Shao Yong" | Traditional account | Challenged in the Ming; no Song record |
| "One ke = 15 minutes" | Classical text | Standard traditional calendrical definition |
| "About 12,000 verses" | Scholarly discussion | A conventional figure; counts differ |

Read it as: **"some say, unproven."**

---

## About the tool

### Q9: What can the demo actually compute?

**Can**: Gregorian year → sexagenary; 60-cycle index lookup both ways; terminology lookup;
verse-number *format* checking; citation skeleton.

**Cannot**: cast a full BaZi chart (multiple school-dependent settings), derive numbers,
perform kaoke, or produce any personal reading.

### Q10: Does the tool upload my data?

**No.** It imports no network library, writes no files (except tests), and asks for no personal
information. You can run it offline and read the source — under 400 lines.

### Q11: Why does `ganzhi 1984` differ from some other program?

Likely one of three causes:
1. **Year boundary**: this tool converts by calendar year. In practice the year pillar changes at
   **Lichun** (立春) — someone born in January 1984 still belongs to 癸亥 (1983).
2. **True solar time vs standard time**: longitude differences shift the hour.
3. **Day boundary at zi hour**: 23:00 or 00:00 — schools differ.

The tool's output already flags cause #1. It is a deliberate boundary note, not a bug.

---

## About the debates

### Q12: Is Tieban Shenshu "real"?

Break it down:

**As a historical text — yes.** The system existed in the Qing, with documents, transmission,
and practitioners.

**As a predictive method — unverifiable.** No reproducible, peer-reviewed study supports accurate
prediction of individual lives.

**As a cultural phenomenon — valuable.** It reflects how traditional Chinese society imagined
fate, family, and ethics.

We **endorse no claim of efficacy**.

### Q13: Why don't you say "we are the authentic one"?

Because it cannot be said. The lineage record is unreliable, every school claims validity, and no
third party has adjudicated. Claiming uniqueness may help commercially but **does not hold factually**.

### Q14: Someone says it can predict life and death. How should I read that?

Be cautious. Such claims typically: report only successes; fail to replicate; rely on repeated
post-hoc adjustment of *kaoke*; and use vague language inviting self-confirmation.

**Key question**: if a method is only accurate *after the fact*, it has no predictive power *before* it.

---

## Contributing

### Q15: What can I do?

| Contribution | Value |
|---|---|
| Point out errors | High |
| Supply bibliographic sources | High |
| Improve translations (esp. regional usage) | High |
| Improve tool code and tests | Medium |
| Ask questions | Medium |

You do not need to be an expert. "This sentence does not parse" or "this link is broken"
is a valid contribution.

### Q16: What should I not do?

Do not submit real birth data, unattributed full verse texts, content copied from
non-commercial-licensed projects, divination advertising, or fabricated citations.

---

## Not answered here?

Open an [issue](https://github.com/tiebanshenshuapp-bot/tiebanshenshu/issues).
We will answer seriously — and tell you when a question is outside our scope.

---

*Last updated: 2026-11-27*