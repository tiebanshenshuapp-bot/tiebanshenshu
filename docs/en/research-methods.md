---
title: "Tieban Shenshu Research Methods"
description: "Our evidence-grading standard and citation conventions: how to weigh a claim and how to verify anything we publish."
lang: en
layout: default
---

# Research Methods

> How we judge, how we cite, and how we handle disagreement.
> If you want to assess whether we are trustworthy, read this page.

---

## 1. Three hard rules

### Rule 1: Label every claim's evidence level

| Level | Test | Handling |
|---|---|---|
| **Classical text** | Traceable to a Qing-era or earlier edition | Quote with edition, juan, page |
| **Traditional account** | Lineage claim, school self-description, folklore | Label as such; **never state as fact** |
| **Scholarly discussion** | Supported by philological research, contested | Cite sources; allow multiple views |
| **Editorial note** | Our own arrangement or inference | Mark as ours |
| **Synthetic sample** | Fabricated for demonstration | **Prominently labelled fictitious** |

**Why this matters most**: the central failure mode in this field is not being wrong —
it is **mistaking "I heard" for "it is recorded."** Mix the levels and the whole text becomes untrustworthy.

### Rule 2: No claim of orthodoxy

We avoid these formulations unless hard evidence appears (none has):

| Forbidden | Reason |
|---|---|
| "the only authentic lineage" | The transmission record does not exist |
| "personally transmitted by Shao Yong" | Challenged since the Ming; no Song evidence |
| "an imperially guarded secret" | No historical basis |
| "Hong Kong is the true origin" | A transmission hub, not a birthplace |
| "our algorithm is the most accurate" | Not verifiable by any reproducible method |

### Rule 3: No fate claims

We discuss **texts and culture**. We do not provide readings.

Prohibited: personal predictions, accuracy percentages, "change your fate", or any medical,
financial, or legal advice.

---

## 2. Citation format

```text
Author. Title[M]. Dynasty. Edition information. Juan: page.

Example:
Shao Yong. Huangji Jingshi[M]. Song. Qing Qianlong XX edition
(or: XX Press, 19XX photoreprint). Juan X: p. XX.
```

**Hard requirements**:

1. **Always name the edition** — "according to an ancient text" is not a citation
2. **Give a page number** where possible; if unavailable, explain why
3. **Distinguish quotation from secondary citation** — if you took it from a modern work, say so

### Why editions matter

Different editions of the same work can differ in content. This is acute for Tieban Shenshu:
manuscripts diverge, editors made different changes, and modern reprints use different base texts.

**An edition-less citation is not a citation.**

---

## 3. Handling disagreement

We present the **structure** of a dispute rather than picking a side:

```markdown
On X, there are two positions:

**Position A** (held by …)
Argument: …
Source: …

**Position B** (held by …)
Argument: …
Source: …

**Our assessment**: lean A / lean B / withhold judgement
Because: …
```

### When we do take a side

Only when the evidence is markedly asymmetric:

| Dispute | Our position | Reason |
|---|---|---|
| Composed by Shao Yong? | Lean "no" | No Song record + explicit Ming criticism |
| Did Tie Buzi exist? | Lean "doubtful" | Zero contemporaneous trace |
| Which manuscript is most reliable? | **No position** | No collation study exists |
| Exact number of verses | **No position** | Versions differ; no authoritative count |

---

## 4. What we will and will not publish

**Rights status:**

| Category | Publish? |
|---|---|
| A. Clearly public domain (pre-1912 text) | ✅ |
| B. Our own work, cleared to publish | ✅ |
| C. Third-party, licensed for quotation | ✅ limited |
| D. Rights unknown | ❌ |
| E. Commercial private asset | ❌ |
| F. Personal data / credentials | ❌ |

**Plus**: traceable source required, and genuine research or educational value.

We do not publish to fill space. Fewer, better items.

---

## 5. Research we do not do

| Not done | Why |
|---|---|
| Statistically "proving" accuracy | Requires personal data and a control design we cannot construct ethically |
| Endorsing commercial efficacy | Conflict of interest |
| Collecting users' birth data | Privacy risk, unnecessary |
| Building a case database | High risk even anonymised |
| Adjudicating other schools' authenticity | Beyond our competence and remit |

---

## 6. How to evaluate our credibility

Five practical checks:

**1. Are claims labelled by evidence level?**
A text that never distinguishes record from rumour has low credibility.

**2. Are editions cited?**
Citing classical texts without editions suggests the author never saw the book.

**3. Does it admit uncertainty?**
Good research says "this is unclear." **Uniform confidence is a warning sign.**

**4. Can the tools be reproduced?**
Ours can — you can run them, read them, change them, and verify behaviour.
A claim that can only be taken on trust is unverifiable.

**5. How does it respond to criticism?**
If we fix errors when you point them out, the project is serious.
If we delete comments and dodge questions, it is not.

**We invite you to test #5.**

---

## 7. Tool auditability

| Property | Benefit |
|---|---|
| Zero dependencies (stdlib only) | You see all the code; no hidden layers |
| Under 400 lines | You can read it in an hour |
| 26 unit tests | You can verify behaviour yourself |
| No network access | You can confirm no data leaves your machine |
| Explicit limits | It does not pretend to do what it cannot |

Verify yourself:

```bash
cd demo
python -m unittest discover -s tests -v
grep -E "import.*(requests|urllib|socket)" tieban_open_tools.py   # should output nothing
```

---

## 8. If you want to rebut us

We welcome it. Please include:

1. **Which sentence** (quote it)
2. **What you think is wrong**
3. **Your source** (title, edition, page, link)
4. **Suggested correction**

With a source, we will change it. If we ultimately disagree, we will record that a
dissenting view exists.

---

## 9. Our own limitations

| Limitation | Consequence |
|---|---|
| We only have public sources | We may miss privately held manuscripts |
| We are not professional historians | Our philology may err |
| We have a commercial interest | We try to be objective; we cannot be neutral |
| Limited sample | We have seen only a few public transcriptions |

**Treat this project as an honest introduction, not an authoritative scholarly work.**

---

*Last updated: 2026-11-27*