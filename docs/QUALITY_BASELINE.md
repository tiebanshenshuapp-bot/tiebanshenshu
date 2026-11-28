# 质量基线 / Quality Baseline

> Lighthouse 实测记录。可复现。
> 采集时间：2026-11-28 13:20 (UTC+8)
> 工具：Chrome DevTools MCP · Lighthouse · mobile emulation

---

## 当前分数

| 页面 | Performance | Accessibility | Best Practices | SEO | 失败项 |
|---|---|---|---|---|---|
| `/zh-hans/` 入门总览 | — | **100** | **100** | **100** | 0 |
| `/tools/` 在线工具 | — | **100** | **100** | **100** | 0 |

> Performance 未单独给出（页面为纯静态 HTML，无 JS 阻塞，Lighthouse 未生成独立性能报告）。

---

## 修复历史

### 2026-11-28 · hreflang 相对路径（SEO 91 → 100）

**问题**：Lighthouse 报 `hreflang` 审计失败，5 条 hreflang 全部无效。

**根因**：`docs/_layouts/default.html` 中 hreflang 的 `href` 用了相对路径：

```html
<link rel="alternate" hreflang="zh-Hans" href="/tiebanshenshu/zh-hans/">
```

而 Google 规范明确要求 hreflang 必须是**绝对 URL**（含协议与域名）。
相对路径会被直接忽略 —— 意味着**四语 hreflang 声明全部作废**，
Google 无法建立四个语言版本之间的对应关系。

**修复**：

```html
<link rel="alternate" hreflang="zh-Hans"
      href="https://tiebanshenshuapp-bot.github.io/tiebanshenshu/zh-hans/">
```

**验证**：线上实测 5 条 hreflang 均为绝对 URL（见下）。

```
<link rel="alternate" hreflang="zh-Hans"     href="https://.../zh-hans/">
<link rel="alternate" hreflang="zh-Hant-HK"  href="https://.../zh-hk/">
<link rel="alternate" hreflang="zh-Hant-TW"  href="https://.../zh-tw/">
<link rel="alternate" hreflang="en"          href="https://.../en/">
<link rel="alternate" hreflang="x-default"   href="https://.../">
```

---

## 如何复现

1. 打开 Chrome DevTools（MCP 或手动）
2. Lighthouse → Mode: navigation → Device: mobile
3. 选择 Accessibility / Best Practices / SEO
4. 跑审计

---

## 持续要求

任何改动后若出现以下情况，必须修：

| 情况 | 门槛 |
|---|---|
| Accessibility < 100 | 必修 |
| Best Practices < 100 | 必修 |
| SEO < 100 | 必修 |
| 任意 audit 报 fail | 必须查明 |

**注意**：100 分不代表用户体验完美，只代表这四项自动检查无问题。
真实用户性能、可用性仍需人工判断。