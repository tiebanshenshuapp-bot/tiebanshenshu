# 教学工具 / Educational Tools

> **零依赖、纯本地、不含任何私有算法。**

---

## 这是什么

一个用 Python 标准库写的命令行教学工具，演示铁板神数相关的**公开基础概念**。

**它不做什么**（很重要）：

| 不做 | 原因 |
|---|---|
| 不排八字 | 涉及立春分年、真太阳时、子时换日等多个流派差异 |
| 不实现起数 | 起数公式属私有/师传 |
| 不做考刻定分 | 同上 |
| 不生成命书 | 这不是算命工具 |
| 不联网 | 你的数据不出你的电脑 |
| 不采集个人信息 | 从不询问姓名、生辰、位置 |

---

## 环境要求

- Python 3.9 或更高
- **不需要** `pip install` 任何东西

检查版本：

```bash
python --version
```

---

## 快速开始

```bash
cd demo
python tieban_open_tools.py ganzhi 1984
```

输出：

```
1984 年 → 甲子
  天干 甲（木）· 地支 子（水）
  注：此处按公元 4 年为甲子年的通用算法换算；若用于命理，还需按立春分年。
```

---

## 全部命令

### `ganzhi <年份>`
公历年 → 干支。

```bash
python tieban_open_tools.py ganzhi 2026
# → 2026 年 → 丙午
```

> ⚠️ **注意边界**：本命令按公元年份直接换算。
> 命理上排年柱应以**立春**为界——1984 年 1 月出生的人，命理年柱仍属 1983 年（癸亥）。

---

### `jiazi <干支>`
查六十甲子序号。

```bash
python tieban_open_tools.py jiazi 甲子    # → 第 1 位
python tieban_open_tools.py jiazi 癸亥    # → 第 60 位
```

**会校验合法性**：

```bash
python tieban_open_tools.py jiazi 甲丑
# → 输入有误：「甲丑」在六十甲子中不存在（阴阳不配）
# 退出码 2
```

---

### `at <序号>`
按序号取干支（1-60）。

```bash
python tieban_open_tools.py at 1     # → 甲子
python tieban_open_tools.py at 60    # → 癸亥
```

---

### `term <术语>`
查询传统术语，**带证据层级标注**。

```bash
python tieban_open_tools.py term 考刻
```

输出包括：释义、说明、证据层级、注意事项、来源。

列出全部术语：

```bash
python tieban_open_tools.py term x --list
```

当前收录：铁板神数、考刻、定分、条文、太玄数、皇极经世、邵子神数

---

### `check <编号>`
条文编号**格式**校验。

```bash
python tieban_open_tools.py check 4082
# → 编号 4082：格式 通过
#     所在集次：第 4 集
#     集内位置：第 82 位
#     仅为编号格式校验，不包含条文内容。
```

> **重要**：此命令**只校验编号格式**，**不返回任何条文内容**。
> 它演示的是"编号如何分段"这一纯格式问题，不涉及任何私有映射。
> 默认区间 1001–13000 仅为演示参数，不代表任何特定抄本的权威映射。

---

### `cite <书名>`
生成文献引用骨架。

```bash
python tieban_open_tools.py cite 皇极经世
# → 邵雍. 皇极经世[M]. 宋. （请补：具体版本、影印或点校本、出版者、页码）
```

**为什么强调要补版本？**

因为同一部书的不同版本内容可能不同。不写版本，等于没写来源。

---

### `--json`
机器可读输出，便于脚本调用。

```bash
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

---

## 测试

```bash
cd demo
python -m unittest discover -s tests -v
```

预期结果：

```
Ran 26 tests in 0.0XXs

OK
```

### 测试覆盖了什么

| 测试类 | 覆盖内容 |
|---|---|
| `TestGanzhi` | 5 个历史锚点年份、60 年周期、天干/地支周期、非法输入 |
| `TestJiazi` | 边界值、全部 60 位双向 roundtrip、非法干支、阴阳不配 |
| `TestVerseNumberCheck` | 边界、越界、**确认不泄露条文内容** |
| `TestGlossary` | 结构完整性、证据层级合法性、别名匹配、**确认不含私有算法线索** |
| `TestCite` | 已知/未知书名 |
| `TestCli` | 各子命令、JSON 输出、错误退出码 |

---

## 安全说明

### 验证它不联网

```bash
# Windows PowerShell
Select-String -Path tieban_open_tools.py -Pattern "import.*(requests|urllib|socket)"

# macOS / Linux
grep -E "import.*(requests|urllib|socket)" tieban_open_tools.py
```

**应该没有任何输出。**

### 验证它不写文件

工具中唯一的文件操作是**无**（测试文件除外）。
它不读配置、不写日志、不建缓存。

### 验证它不采集数据

它唯一的输入是命令行参数。不询问姓名、生辰、位置。

---

## 文件结构

```
demo/
├── README.md              # 本文件
├── tieban_open_tools.py   # 主工具（约 400 行，可完整阅读）
├── data/                  # 数据目录（当前为空，术语表内嵌于代码）
└── tests/
    └── test_tools.py      # 26 项测试
```

---

## 为什么代码量这么小

**刻意的。**

我们希望你能**在一小时内读完全部代码**，确认它：
- 没做你别的事
- 没藏后门
- 算法是公开可查的

一个你看不懂的工具，就算功能再强，也不该信任。

---

## 许可

本目录代码采用 [PolyForm Noncommercial 1.0.0](../LICENSE)。

**这是 Source Available，不是 OSI 开源。** 可以读、可以学、可以改、可以分享，
但**不能用于商业目的**。

---

## 想贡献

见 [CONTRIBUTING.md](../CONTRIBUTING.md)。

工具层面的贡献，请确保：

1. 不引入第三方依赖（保持零依赖）
2. 不引入网络调用
3. 不采集个人信息
4. 有对应测试
5. 测试全部通过

---

*最后更新：2026-11-27*