---
title: "铁板神数上手指引"
description: "从零开始了解铁板神数：先读什么、三个必须分清的概念、常见误区，以及可本地运行的教学工具。"
lang: zh-Hans
layout: default
---

# 快速上手 / Getting Started

> 5 分钟了解这个仓库能给你什么。

---

## 一、你可能是哪一类人

选一条，直接跳过去：

| 你是 | 去这里 |
|---|---|
| 🔍 好奇"铁板神数到底是什么" | [第 2 节](#二如果你只是好奇) |
| 🛠 想动手跑点东西 | [第 3 节](#三如果你想动手) |
| 📚 想研究文献与源流 | [第 4 节](#四如果你想做研究) |
| 🌐 想帮忙翻译或纠错 | [第 5 节](#五如果你想贡献) |
| 💼 想用商业版 | [第 6 节](#六如果你想要完整功能) |

---

## 二、如果你只是好奇

### 花 3 分钟读这个

**[入门总览](index.md)** —— 一次讲清楚：
这是什么、跟八字有什么不同、源流哪些清楚哪些不清楚。

### 再花 2 分钟看这个

**[术语表](glossary.md)** —— 看到"考刻""定分""条文"这些词不再懵。

### 如果你只有一个问题

看 **[FAQ](faq.md)**，16 个最常见的问题。

---

## 三、如果你如果想动手

### 环境要求

**只需 Python 3.9+**。不需要 pip install 任何东西。

检查：

```bash
python --version
```

### 跑起来

```bash
git clone https://github.com/tiebanshenshuapp-bot/tiebanshenshu.git
cd tiebanshenshu/demo
```

然后试这五条：

```bash
# 1. 1984 年是什么年？
python tieban_open_tools.py ganzhi 1984
# → 1984 年 → 甲子

# 2. 甲子在六十甲子里排第几？
python tieban_open_tools.py jiazi 甲子
# → 甲子 是六十甲子第 1 位。

# 3. "考刻"到底什么意思？
python tieban_open_tools.py term 考刻

# 4. 条文编号 4082 格式对不对？
python tieban_open_tools.py check 4082

# 5. 引用《皇极经世》该怎么写？
python tieban_open_tools.py cite 皇极经世
```

### 想看全部功能

```bash
python tieban_open_tools.py --help
python tieban_open_tools.py term x --list    # 列出所有术语
```

### 想要机器可读输出

```bash
python tieban_open_tools.py --json ganzhi 1984
```

输出：

```json
{
  "year": 1984,
  "ganzhi": "甲子",
  "tiangan_wuxing": "木",
  "dizhi_wuxing": "水"
}
```

### 自己验证它没有偷偷联网

```bash
# Windows PowerShell
Select-String -Path tieban_open_tools.py -Pattern "import.*requests|urllib|socket"

# macOS / Linux
grep -E "import.*(requests|urllib|socket)" tieban_open_tools.py
```

**应该没有任何输出。** 如果有，说明有问题，请报 Issue。

### 跑测试

```bash
python -m unittest discover -s tests -v
```

应该看到 `Ran 26 tests ... OK`。

---

## 四、如果你想做研究

### 先读方法论

**[研究方法](research-methods.md)** —— 我们的判断标准、引用规范、如何评价可信度。

### 再看源流

**[源流与争议](history.md)** —— 时间线、关键证据、哪些问题至今无解。

### 然后自己核查

我们**强烈建议**你不要只信我们。核查方法：

| 你要核查的 | 去哪里查 |
|---|---|
| 杨慎的批评 | 《升庵集》原文 |
| 邵雍生平 | 《宋史·邵雍传》 |
| 《皇极经世》内容 | 原书或权威整理本 |
| 条文内容 | 你自己手上的抄本或影印本 |

### 欢迎反驳我们

见 [研究方法 · 第八节](research-methods.md#八如果你要反驳我们)。

---

## 五、如果你想贡献

### 最容易的三种贡献

| 类型 | 怎么做 |
|---|---|
| 报告错误 | 开 Issue，说明哪一句、错在哪、依据是什么 |
| 改进翻译 | 特别是香港/台湾用语差异 |
| 补充文献出处 | 书名 + 版本 + 页码 |

### 先读这个

**[贡献指南](../../CONTRIBUTING.md)** —— 10 分钟读完，避免白做。

### 不要提交这些

- ❌ 真实生辰、姓名、命书
- ❌ 来源不明的条文全文
- ❌ 从禁止商用项目复制的内容
- ❌ 算命广告

---

## 六、如果你想要完整功能

本仓库是**研究社区**，不是商业产品。

| 你需要 | 去哪里 |
|---|---|
| 完整条文库 | 官方网站 |
| 排盘、考刻定分 | 官方网站 |
| 生成命书 | 官方网站 |
| 免费试用 | https://tiebanshenshuapp.com/trial |

官方网站：**https://tiebanshenshuapp.com**

---

## 七、常见卡点

### "`python` 命令找不到"

试 `python3`（macOS/Linux）或 `py`（Windows）。

### "中文显示成乱码"

**Windows PowerShell** 先设置编码：

```powershell
$env:PYTHONIOENCODING="utf-8"
```

### "`ganzhi 1984-01-15` 算出来是甲子，但我查别的软件是癸亥"

**这不是 bug。**

本工具的 `ganzhi` 是按**公元年份**直接换算。
命理上排年柱应以**立春**为界，1984 年 1 月出生的人，
命理年柱仍属 1983 年（癸亥）。

工具的说明里已经提示了这一点。见 [FAQ Q11](faq.md)。

### "工具为什么不排八字？"

因为排八字涉及多个流派差异：

- 立春分年（精确到分秒，需天文计算）
- 真太阳时（需出生地经纬度）
- 子时换日（23:00 还是 00:00，各家不同）

这些差异会导致**排出的结果不同**。
我们不提供一个"假装权威"的排盘，而是把这个边界说清楚。

---

## 八、下一步

| 想继续 | 去 |
|---|---|
| 深入术语 | [术语表](glossary.md) |
| 了解源流 | [源流与争议](history.md) |
| 了解我们的方法论 | [研究方法](research-methods.md) |
| 参与建设 | [贡献指南](../../CONTRIBUTING.md) |
| 看计划 | [路线图](../../ROADMAP.md) |

---

*最后更新：2026-11-27*