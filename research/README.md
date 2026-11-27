# 研究资料索引 / Research Index

> 本目录收录**可公开的研究资料**：文献索引、公开项目调查、研究问题。
> 所有条目都必须有来源与权利标注。

---

## 目录

| 子目录 | 内容 |
|---|---|
| `bibliography/` | 古籍与文献索引（拟建） |
| `public-repositories/` | 全球公开项目调查（见下） |
| `glossary/` | 术语对照材料（见 [`docs/*/glossary.md`](../docs/)） |
| `research-questions/` | 待研究的问题（拟建） |

---

## 全球公开项目调查

本项目的调查方法与结论如下。

### 我们的立场

> **Public ≠ 可复制。**

GitHub 上公开可见的代码，**不等于**授权你使用。
没有许可声明的仓库，法律上默认「保留所有权利」。

因此本项目：

1. 只**记录**公开项目的存在与许可状态
2. **不复制**任何无许可或禁止商用项目的内容
3. 引用时只提供**链接与客观描述**

---

## 一、铁板神数专项项目

### `xaminxan/tiebanshenshu`

| 项目 | 内容 |
|---|---|
| 地址 | https://github.com/xaminxan/tiebanshenshu |
| 语言 | Python |
| 体量 | 约 272 KB |
| 许可 | **无（保留所有权利）** |
| 状态 | 最后推送 2025-12 |
| 我们的判断 | 仅作研究参考。**无许可 = 不可复制** |

**观察**：多个后续项目（含 `Nanphy/TiebanshenshuOS`、`csdxdn/tiebanshenshu`）
的仓库体量与其**完全一致**（272 KB），呈 fork 关系。
这说明所谓"生态"实际来源集中度很高。

---

### `Nanphy/TiebanshenshuOS`

| 项目 | 内容 |
|---|---|
| 地址 | https://github.com/Nanphy/TiebanshenshuOS |
| 语言 | HTML |
| 体量 | 约 73 MB |
| 许可 | **无（保留所有权利）** |
| 状态 | 最后推送 2026-07 |
| 我们的判断 | 仅作研究参考，**未复制** |

另有 `Nanphy/TiebanshenshuOS_V2`，同样无许可。

---

### `hackninety/tbss-ts-lib`（现 `pyqq4bs4xy-sys/tbss-ts-lib`）

| 项目 | 内容 |
|---|---|
| 地址 | https://github.com/pyqq4bs4xy-sys/tbss-ts-lib |
| 语言 | TypeScript |
| 体量 | 约 587 KB |
| 许可 | **CC BY-NC 4.0（明确禁止商用）** |
| 我们的判断 | **不可用于商业产品**，本项目不采用其数据 |

**它的自我说明**（如实转述）：

- 收录约 12,000 条条文（十二集，号 1001–13000）
- 十四考取数表 15 张
- 明确声明"底本未经与清刊本逐字校勘"
- 明确声明"条文为清代公版古籍之社区数字化转录"

> **关键法律判断**：古籍原文属公有领域，但**"某人整理的那份转录"可能构成汇编作品**，
> 受其自身许可约束。CC BY-NC 意味着**禁止商业使用**，本项目为商业产品的社区，
> 因此不能采用。

---

### `pyqq4bs4xy-sys/tieban-shenshu-skillpack`

| 项目 | 内容 |
|---|---|
| 地址 | https://github.com/pyqq4bs4xy-sys/tieban-shenshu-skillpack |
| 体量 | 约 767 KB |
| 许可 | **无（保留所有权利）** |
| 内容 | SKILL.md（约 50 KB）+ 条文 JSON（约 1 MB）+ 6 份参考资料 |
| 我们的判断 | 仅研究其**公开叙述的方法论**，**未复制数据或代码** |

> 该项目在 README 中公开了部分算法描述（如"若干刻分推导链条"），
> 并注明了其依据的文献（《铁板神数正宗破解钥匙》、张椿来《铁版神数》原书）。
>
> **这些说明属于"思路"，不受版权保护；但其具体数据文件受其许可约束。**
> 本项目因此**只学习方法论，不复制数据**。

---

### 其他相关项目

| 仓库 | 许可 | 判断 |
|---|---|---|
| `csdxdn/react-tieban` | 无 | 仅研究。前端，接入 tbss-ts-lib |
| `regulusab/tieban` | 无 | 仅研究 |
| `wang-er-1-2003/comprehensive-shushu-engine` | **GPL-3.0** | 可商用但**传染开源**，本项目不采用 |
| `luluxinxin-love/TransformerShenShu` | MIT（标称） | **实测为空壳**，见下 |

#### 关于 `TransformerShenShu` 的实测结论

该项目 README 宣称"42M 样本、验证集准确率 99.87%"。

**我们的实测**：

- `checkpoints/` 目录仅含 `.gitkeep`（4 字节）
- `data/processed/` 为空
- **Releases 列表为空**

**结论**：模型权重、数据集、可执行产物**均未发布**。
README 的声明**无法验证**。

> 本项目不接受"仅凭 README 宣称"的技术主张。
> 这是我们的一条方法论原则：**能跑才算数**。

---

## 二、可商用（MIT）但属其他体系

以下项目许可宽松（MIT），**但它们不是铁板神数**，本项目遵循 `TIEBAN_ONLY` 原则不使用：

| 仓库 | 星 | 体系 | 许可 |
|---|---|---|---|
| `Renhuai123/ziwei-doushu` | ~19830 | 紫微斗数 | MIT |
| `SylarLong/iztro` | ~4449 | 紫微斗数 | MIT |
| `Sudo-Biao/Chinese-Metaphysics-Platform` | ~192 | 八字/六爻/奇门/风水/择日 | MIT |

**为什么记录它们**：它们展示了成熟的中文术数工程化做法（结构、测试、文档），
可作**工程质量参考**，但不作内容来源。

---

## 三、从这次调查中学到的

### 1. 公开 ≠ 可用

19 个铁板神数相关仓库中：

| 许可状态 | 数量 | 能否用于商业产品 |
|---|---|---|
| 无许可 | 多数 | ❌ 法律上不可 |
| CC BY-NC | 1 | ❌ 明确禁止 |
| GPL-3.0 | 1 | ⚠️ 传染 |
| MIT | 少数（且非本体系） | ✅ 但内容不对口 |

**结论**：没有可以"直接拿来用"的铁板神数代码。

### 2. 数据比代码更敏感

代码可以重写，但**条文数据的转录质量**无法凭空获得。
而恰恰是数据的许可最严格。

### 3. 唯一可靠的路是自建

我们因此确立策略：

- **算法思路**：学习公开讨论（不受版权保护）
- **条文数据**：从公版底本自行录入（见 [`samples/`](../samples/)）
- **工程质量**：借鉴 MIT 项目的做法

---

## 四、如何验证我们的调查

以上所有数字（星数、体量、许可）都可以自己核对：

```bash
gh api repos/xaminxan/tiebanshenshu --jq '{license:.license.spdx_id, size:.size}'
gh api repos/pyqq4bs4xy-sys/tbss-ts-lib --jq '.license.spdx_id'
gh api repos/luluxinxin-love/TransformerShenShu/releases --jq 'length'
```

**最后一条应返回 `0`** —— 这就是"空壳"的证明。

我们鼓励你去验证。如果我们的数字错了，请开 Issue 指正。

---

## 五、调查时间

本页数据采集于 **2026-11-27**。

星数、体量、推送时间会变化。若你发现数据过时，欢迎更新。

---

*本页证据层级：**编者调查**。所有数字均来自 GitHub API 实测，可复现。*
*引用时请注明采集日期。*