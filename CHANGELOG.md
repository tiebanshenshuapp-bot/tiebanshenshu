# Changelog

本文件记录本仓库的公开变更。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

## [Unreleased]

### 计划中
- 补充香港 / 台湾地区术语对照表
- 增加古籍文献索引条目
- Pages 静态文档站可行性评估

---

## [0.1.0] - 2026-11-27

首次公开候选版本（本地构建，等待写入权限后发布）。

### Added
- 四语 README：简体中文、繁體中文（香港／澳門）、正體中文（台灣）、English
- `demo/tieban_open_tools.py` — 零依赖教学工具
  - `ganzhi` 公历年 → 干支换算
  - `jiazi` / `at` 六十甲子序号双向查询
  - `term` 传统术语查询（带证据层级标注）
  - `check` 条文编号格式校验（不含条文内容）
  - `cite` 文献引用骨架生成
  - `--json` 机器可读输出
- `demo/tests/test_tools.py` — 26 项单元测试，全部通过
- `LICENSE` — PolyForm Noncommercial 1.0.0（官方原文）
- `LICENSE-DOCS` — CC BY-NC 4.0
- `NOTICE.md` — 品牌与开源状态声明
- `THIRD_PARTY_NOTICES.md` — 第三方项目研究记录（声明未复制）
- `CONTRIBUTING.md` — 贡献指南（含证据层级要求）
- `CODE_OF_CONDUCT.md` — 社区行为规范
- `SECURITY.md` — 安全策略
- `ROADMAP.md` — 公开路线图
- `CITATION.cff` — 引用格式
- 四语 `docs/` 文档目录骨架

### Changed
- 原 208 字节占位 README 由完整四语版本取代

### Security
- 教学工具经检查无网络调用、无文件写入、无个人信息采集
- 明确排除：私有引擎、完整条文库、客户数据、任何密钥

### Fixed
- 修正测试用例中的干支周期断言错误（+10 年为天干不变，非地支）

---

## 关于版本号

本仓库使用独立的社区版版本号 `0.x.y`，
**与商业软件的版本号完全无关**，不可互相引用。

---

[Unreleased]: https://github.com/tiebanshenshuapp-bot/tiebanshenshu/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/tiebanshenshuapp-bot/tiebanshenshu/releases/tag/v0.1.0