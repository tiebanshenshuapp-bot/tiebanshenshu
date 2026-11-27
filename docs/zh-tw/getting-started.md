# 快速上手

> 5 分鐘了解這個儲存庫能給你甚麼。

---

## 一、你可能是哪一類人

| 你是 | 去哪 |
|---|---|
| 🔍 好奇「鐵板神數是甚麼」 | [第二節](#二如果你只是好奇) |
| 🛠 想動手跑點東西 | [第三節](#三如果你想動手) |
| 📚 想研究文獻與源流 | [第四節](#四如果你想做研究) |
| 🌐 想幫忙翻譯或糾錯 | [第五節](#五如果你想貢獻) |
| 💼 想用商業版 | [第六節](#六如果你想要完整功能) |

---

## 二、如果你只是好奇

**[入門總覽](index.md)** —— 一次講清楚：這是甚麼、跟八字有甚麼不同、源流哪些清楚哪些不清楚。

**[術語表](glossary.md)** —— 看到「考刻」「定分」「條文」這些詞不再懵。

**[常見問題](faq.md)** —— 16 個最常見的問題。

---

## 三、如果你想動手

### 環境要求

**只需 Python 3.9+**。不需要 pip install 任何東西。

```bash
python --version
```

### 跑起來

```bash
git clone https://github.com/tiebanshenshuapp/tiebanshenshu.git
cd tiebanshenshu/demo
```

然後試這五條：

```bash
# 1. 1984 年是甚麼年？
python tieban_open_tools.py ganzhi 1984
# → 1984 年 → 甲子

# 2. 甲子在六十甲子裏排第幾？
python tieban_open_tools.py jiazi 甲子
# → 甲子 是六十甲子第 1 位。

# 3. 「考刻」到底甚麼意思？
python tieban_open_tools.py term 考刻

# 4. 條文編號 4082 格式對不對？
python tieban_open_tools.py check 4082

# 5. 引用《皇極經世》該怎麼寫？
python tieban_open_tools.py cite 皇極經世
```

### 想看全部功能

```bash
python tieban_open_tools.py --help
python tieban_open_tools.py term x --list
```

### 想要機器可讀輸出

```bash
python tieban_open_tools.py --json ganzhi 1984
```

### 自己驗證它沒有偷偷連網

```bash
Select-String -Path tieban_open_tools.py -Pattern "import.*requests|urllib|socket"
```

**應該沒有任何輸出。**

### 跑測試

```bash
python -m unittest discover -s tests -v
```

應該看到 `Ran 26 tests ... OK`。

---

## 四、如果你想做研究

先讀 **[研究方法](research-methods.md)** —— 我們的判斷標準、引用規範。

再看 **[源流與爭議](history.md)** —— 時間線、關鍵證據、哪些問題至今無解。

然後自己核查：

| 你要核查的 | 去哪裏查 |
|---|---|
| 楊慎的批評 | 《升庵集》原文 |
| 邵雍生平 | 《宋史·邵雍傳》 |
| 《皇極經世》內容 | 原書或權威整理本 |
| 條文內容 | 你自己手上的抄本或影印本 |

---

## 五、如果你想貢獻

最易做的三種貢獻：**報告錯誤**、**改進翻譯**（尤其香港／台灣用語差異）、**補充文獻出處**。

先讀 **[貢獻指南](../../CONTRIBUTING.md)**。

**不要提交**：真實生辰、姓名、命書、來源不明的條文全文、
從禁止商用項目複製的內容、算命廣告。

---

## 六、如果你想要完整功能

本儲存庫是**研究社群**，不是商業產品。

| 你需要 | 去哪裏 |
|---|---|
| 完整條文庫 | 官方網站 |
| 排盤、考刻定分 | 官方網站 |
| 生成命書 | 官方網站 |
| 免費試用 | https://tiebanshenshuapp.com/trial |

官方網站：**https://tiebanshenshuapp.com**

---

## 七、常見卡點

### 「`python` 命令找不到」
試 `python3`（macOS/Linux）或 `py`（Windows）。

### 「中文顯示成亂碼」
**Windows PowerShell** 先設置編碼：

```powershell
$env:PYTHONIOENCODING="utf-8"
```

### 「`ganzhi 1984-01-15` 算出來是甲子，但我查別的軟體是癸亥」
**這不是 bug。**

本工具的 `ganzhi` 是按**公曆年份**直接換算。
命理上排年柱應以**立春**為界，1984 年 1 月出生的人，命理年柱仍屬 1983 年（癸亥）。

### 「工具為甚麼不排八字？」
因為排八字涉及多個流派差異：立春分年（精確到分秒，需天文計算）、
真太陽時（需出生地經緯度）、子時換日（23:00 還是 00:00）。

這些差異會導致**排出的結果不同**。我們不提供一個「假裝權威」的排盤，
而是把這個邊界說清楚。

---

## 八、下一步

| 想繼續 | 去 |
|---|---|
| 深入術語 | [術語表](glossary.md) |
| 了解源流 | [源流與爭議](history.md) |
| 了解我們的方法論 | [研究方法](research-methods.md) |
| 參與建設 | [貢獻指南](../../CONTRIBUTING.md) |
| 看計劃 | [路線圖](../../ROADMAP.md) |

---

*最後更新：2026-11-27*