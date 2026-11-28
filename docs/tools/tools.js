/* 铁板神数在线教学工具
 * 与 demo/tieban_open_tools.py 使用同一套规则与数据，结果一致。
 * 纯前端、无网络请求、不采集任何数据。
 * License: PolyForm Noncommercial 1.0.0
 */
(function () {
  "use strict";

  /* ---------------- 公开基础表（公有领域知识） ---------------- */
  var TIANGAN = "甲乙丙丁戊己庚辛壬癸";
  var DIZHI = "子丑寅卯辰巳午未申酉戌亥";

  var TG_WUXING = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
    "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"
  };
  var DZ_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
    "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水"
  };
  var TG_HE = [
    ["甲己", "土"], ["乙庚", "金"], ["丙辛", "水"],
    ["丁壬", "木"], ["戊癸", "火"]
  ];
  var DZ_CHONG = [
    ["子午"], ["丑未"], ["寅申"], ["卯酉"], ["辰戌"], ["巳亥"]
  ];
  var DZ_SANHE = [
    ["申子辰", "水局"], ["亥卯未", "木局"],
    ["寅午戌", "火局"], ["巳酉丑", "金局"]
  ];

  /* 术语表（与 Python 版一致） */
  var GLOSSARY = {
    "铁板神数": {
      also: ["铁版神数", "鐵板神數", "鐵版神數", "Tieban Shenshu"],
      summary: "托名北宋邵雍的清代命理术数体系，以考刻推演著称。",
      detail: "铁板神数在清代乾隆、嘉庆年间兴起，相传由「铁卜子（铁道人）」校订条文。其法以出生年月日时干支配卦，核对六亲生肖，起数后按数取条文断语。",
      level: "scholarly",
      note: "托名邵雍之说缺乏宋代文献支持，学界多认为晚出。",
      sources: ["维基百科「铁版神数」条目（综述性，供入门参考）", "明代杨慎对「大定数、蠢子数托名康节」的批评（见《升庵集》）"]
    },
    "考刻": {
      summary: "把出生时辰细分为刻，再借六亲信息校验，以确定「真刻」。",
      detail: "一个时辰（两小时）可分为八刻，每刻再分十五分。传统做法是先按六亲（父母、兄弟、配偶、子女）生肖等信息反推，在候选刻分中收窄，定位与已知事实相符的那一刻。",
      level: "traditional",
      note: "具体刻分划分法各流派不尽相同，不存在唯一公定标准。",
      sources: ["传统命理文献对「刻」的通用定义（一时辰八刻）"]
    },
    "定分": {
      summary: "在已定的「刻」内再细分十五分，进一步定位出生时刻。",
      detail: "与考刻合称「考刻定分」，是铁板神数最具辨识度的操作环节。",
      level: "traditional",
      note: "分值的具体对应表属各家师传，公开文献记载并不一致。",
      sources: []
    },
    "条文": {
      also: ["條文", "tiaowen"],
      summary: "按编号排列的断语，是铁板神数的输出形态。",
      detail: "传统上通称约一万二千条，按地支分为子集至亥集共十二集。坊间抄本文字互有出入，目前不存在公认的善本定本。",
      level: "scholarly",
      note: "各家转录本的编号范围与分集方式存在差异。",
      sources: ["清代术数文献通例", "公开数字化转录项目的自述"]
    },
    "太玄数": {
      also: ["太玄數"],
      summary: "起数环节使用的一种配数方法。",
      detail: "太玄数与《太玄经》数理相关，被用于把干支转换为数值。不同传承对具体配值有不同说法。",
      level: "traditional",
      note: "本工具不提供具体配值算法，因各家说法不一且部分属师传。",
      sources: ["扬雄《太玄经》相关数理（公版古籍）"]
    },
    "皇极经世": {
      also: ["皇極經世", "Huangji Jingshi"],
      summary: "北宋邵雍所著，以元会运世推演历史周期的著作。",
      detail: "《皇极经世》是邵雍的代表作，属易学与历史哲学范畴。铁板神数常被说成借用其数理概念，但二者并非同一体系。",
      level: "classical",
      note: "把铁板神数直接等同于《皇极经世》推演法，属于过度简化。",
      sources: ["邵雍《皇极经世》（公版古籍）"]
    },
    "邵子神数": {
      also: ["邵子神數"],
      summary: "铁板神数的别称之一，因托名邵雍而得名。",
      detail: "不同地区与流派对该体系的称呼不统一，需按上下文判断。",
      level: "traditional",
      note: "名称混用常见，不宜据此认定传承关系。",
      sources: []
    }
  };

  var LEVEL_LABEL = {
    classical: "古籍原文",
    traditional: "传统说法",
    scholarly: "学术讨论",
    editorial: "编者观点"
  };

  /* ---------------- 核心计算（与 Python 版一致） ---------------- */

  /* Python 语义取模：结果恒为非负 */
  function pyMod(a, n) {
    return ((a % n) + n) % n;
  }

  function ganzhiOfYear(year) {
    if (!Number.isInteger(year) || year < 1) {
      throw new Error("年份需为正整数");
    }
    return TIANGAN.charAt(pyMod(year - 4, 10)) + DIZHI.charAt(pyMod(year - 4, 12));
  }

  function jiaziIndex(term) {
    term = String(term).trim();
    if (term.length !== 2) {
      throw new Error("请输入两个字的干支，例如「甲子」");
    }
    var g = term.charAt(0), z = term.charAt(1);
    var gi = TIANGAN.indexOf(g), zi = DIZHI.indexOf(z);
    if (gi < 0 || zi < 0) {
      throw new Error("「" + term + "」不是合法干支");
    }
    if (gi % 2 !== zi % 2) {
      throw new Error("「" + term + "」在六十甲子中不存在（阴阳不配）");
    }
    for (var n = 1; n <= 60; n++) {
      if (pyMod(n - 1, 10) === gi && pyMod(n - 1, 12) === zi) {
        return n;
      }
    }
    throw new Error("「" + term + "」无解");
  }

  function jiaziAt(n) {
    n = Number(n);
    if (!Number.isInteger(n) || n < 1 || n > 60) {
      throw new Error("序号需在 1-60 之间");
    }
    /* 必须取模：天干 10 循环、地支 12 循环（与 Python 版一致） */
    return TIANGAN.charAt(pyMod(n - 1, 10)) + DIZHI.charAt(pyMod(n - 1, 12));
  }

  function checkVerseNumber(num, lo, hi) {
    lo = lo || 1001;
    hi = hi || 13000;
    num = Number(num);
    if (!Number.isInteger(num)) {
      throw new Error("请输入整数编号");
    }
    var ok = num >= lo && num <= hi;
    var r = { input: num, range: [lo, hi], ok: ok };
    if (ok) {
      var offset = num - lo;
      r.volumeIndex = Math.floor(offset / 1000) + 1;
      r.positionInVolume = (offset % 1000) + 1;
      r.note = "仅为编号格式校验，不包含条文内容。";
    } else {
      r.note = "编号不在 " + lo + "-" + hi + " 区间内。";
    }
    return r;
  }

  var CITE_TEMPLATES = {
    "皇极经世": "邵雍. 皇极经世[M]. 宋. （请补：具体版本、影印或点校本、出版者、页码）",
    "太玄经": "扬雄. 太玄经[M]. 汉. （请补：具体版本、影校者、出版者、页码）",
    "升庵集": "杨慎. 升庵集[M]. 明. （请补：具体版本、卷次、页码）"
  };

  function cite(work) {
    work = String(work).trim();
    if (!work) {
      throw new Error("请输入书名");
    }
    for (var k in CITE_TEMPLATES) {
      if (CITE_TEMPLATES.hasOwnProperty(k)) {
        if (work.indexOf(k) >= 0 || k.indexOf(work) >= 0) {
          return CITE_TEMPLATES[k];
        }
      }
    }
    return "《" + work + "》\n" +
      "请按以下格式补全：\n" +
      "  作者. 书名[M]. 朝代/年代. 版本信息. 出版者, 出版年: 页码.\n" +
      "提示：引用公版古籍时，务必注明你实际使用的版本，因为不同版本的条文文字存在差异。";
  }

  function findTerm(name) {
    name = String(name).trim();
    if (GLOSSARY[name]) {
      return { term: name, entry: GLOSSARY[name] };
    }
    for (var k in GLOSSARY) {
      if (GLOSSARY.hasOwnProperty(k) && GLOSSARY[k].also) {
        if (GLOSSARY[k].also.indexOf(name) >= 0) {
          return { term: k, alias: name, entry: GLOSSARY[k] };
        }
      }
    }
    var suggestions = [];
    for (var t in GLOSSARY) {
      if (GLOSSARY.hasOwnProperty(t) && t.indexOf(name) >= 0) {
        suggestions.push(t);
      }
    }
    if (!suggestions.length) {
      for (var t2 in GLOSSARY) {
        if (GLOSSARY.hasOwnProperty(t2)) { suggestions.push(t2); }
      }
    }
    return { term: null, suggestions: suggestions };
  }

  /* 干支关系：支持完整干支（如「甲子」）或单字（天干/地支自动识别） */
  var DZ_LIUHE = [["子丑"], ["寅亥"], ["卯戌"], ["辰酉"], ["巳申"], ["午未"]];

  function parseGZ(x) {
    x = String(x).trim();
    if (x.length === 2) {
      if (TIANGAN.indexOf(x.charAt(0)) < 0 || DIZHI.indexOf(x.charAt(1)) < 0) {
        throw new Error("「" + x + "」不是合法干支（天干+地支组合）");
      }
      return { ganzhi: x, gan: x.charAt(0), zhi: x.charAt(1) };
    }
    if (x.length === 1) {
      if (TIANGAN.indexOf(x) >= 0) { return { ganzhi: null, gan: x, zhi: null }; }
      if (DIZHI.indexOf(x) >= 0) { return { ganzhi: null, gan: null, zhi: x }; }
      throw new Error("「" + x + "」既不是天干也不是地支");
    }
    throw new Error("请输入两个字（干支，如「甲子」）或一个字（天干/地支）");
  }

  function pairHit(table, x, y) {
    for (var i = 0; i < table.length; i++) {
      var s = table[i][0];
      if ((s.charAt(0) === x && s.charAt(1) === y) ||
          (s.charAt(0) === y && s.charAt(1) === x)) {
        return table[i][1] || true;
      }
    }
    return null;
  }

  function ganzhiRelation(a, b) {
    var A = parseGZ(a), B = parseGZ(b);
    var out = [];

    /* --- 天干 --- */
    var g1 = A.gan, g2 = B.gan;
    if (g1 && g2) {
      var he = pairHit(TG_HE, g1, g2);
      if (he) {
        out.push("天干「" + g1 + g2 + "」→ 五合，化" + he);
      } else if (g1 === g2) {
        out.push("天干「" + g1 + g1 + "」→ 相同，不构成五合");
      } else {
        out.push("天干「" + g1 + g2 + "」→ 不构成五合");
      }
    } else if (g1 || g2) {
      out.push("（只给了一个天干，无法比较；请同时给出两个天干或两个干支）");
    }

    /* --- 地支 --- */
    var z1 = A.zhi, z2 = B.zhi;
    if (z1 && z2) {
      var chong = pairHit(DZ_CHONG, z1, z2);
      var liuhe = pairHit(DZ_LIUHE, z1, z2);
      var sanhe = null, sanheJu = null;
      for (var i = 0; i < DZ_SANHE.length; i++) {
        var s = DZ_SANHE[i][0];
        if (z1 !== z2 && s.indexOf(z1) >= 0 && s.indexOf(z2) >= 0) {
          sanhe = s; sanheJu = DZ_SANHE[i][1];
          break;
        }
      }

      if (chong) { out.push("地支「" + z1 + z2 + "」→ 六冲"); }
      else if (liuhe) { out.push("地支「" + z1 + z2 + "」→ 六合"); }
      else if (sanhe) { out.push("地支「" + z1 + z2 + "」→ 同属" + sanheJu + "（三合：" + sanhe + "）"); }
      else if (z1 === z2) { out.push("地支「" + z1 + z1 + "」→ 相同，不构成冲合"); }
      else { out.push("地支「" + z1 + z2 + "」→ 不构成六冲、六合或三合同局"); }
    } else if (z1 || z2) {
      out.push("（只给了一个地支，无法比较；请同时给出两个地支或两个干支）");
    }

    if (A.ganzhi && B.ganzhi && A.ganzhi === B.ganzhi) {
      out.push("注：两个干支完全相同");
    }

    /* 只给了天干或只给了地支时，明确告知另一半未比较，避免用户误解为结果不完整 */
    if ((g1 && g2) && !(z1 && z2)) {
      out.push("（未提供地支，故未比较冲合关系）");
    }
    if ((z1 && z2) && !(g1 && g2)) {
      out.push("（未提供天干，故未比较五合关系）");
    }

    return out;
  }

  /* 简体 -> 繁体 逐字对照（仅覆盖本领域常见字，非完整转换） */
  var S2T = {
    "铁": "鐵", "板": "板", "数": "數", "神": "神", "软": "軟", "件": "件",
    "术": "術", "条": "條", "文": "文", "书": "書", "经": "經", "世": "世",
    "历": "歷", "史": "史", "研": "研", "究": "究", "方": "方", "法": "法",
    "学": "學", "问": "問", "题": "題", "资": "資", "料": "料", "来": "來",
    "源": "源", "版": "版", "本": "本", "记": "記", "载": "載", "传": "傳",
    "统": "統", "说": "說", "论": "論", "证": "證", "据": "據", "层": "層",
    "级": "級", "义": "義", "释": "釋", "词": "詞", "汇": "匯", "编": "編",
    "号": "號", "集": "集", "卷": "卷", "册": "冊", "页": "頁", "码": "碼",
    "时": "時", "辰": "辰", "刻": "刻", "分": "分", "定": "定", "考": "考",
    "六": "六", "亲": "親", "配": "配", "偶": "偶", "子": "子", "女": "女",
    "父": "父", "母": "母", "兄": "兄", "弟": "弟", "生": "生", "肖": "肖",
    "干": "干", "支": "支", "甲": "甲", "乙": "乙", "丙": "丙", "丁": "丁",
    "戊": "戊", "己": "己", "庚": "庚", "辛": "辛", "壬": "壬", "癸": "癸",
    "太": "太", "玄": "玄", "皇": "皇", "极": "極", "邵": "邵", "雍": "雍",
    "康": "康", "节": "節", "杨": "楊", "慎": "慎", "升": "升", "庵": "庵",
    "清": "清", "代": "代", "乾": "乾", "隆": "隆", "嘉": "嘉", "庆": "慶",
    "铁": "鐵", "道": "道", "人": "人", "校": "校", "订": "訂", "抄": "抄",
    "本": "本", "真": "真", "伪": "偽", "争": "爭", "议": "議", "准": "準",
    "确": "確", "率": "率", "预": "預", "测": "測", "命": "命", "运": "運",
    "书": "書", "软": "軟", "体": "體", "网": "網", "络": "絡", "资": "資",
    "讯": "訊", "设": "設", "计": "計", "计": "計", "算": "算", "机": "機",
    "程": "程", "序": "序", "员": "員", "开": "開", "发": "發", "者": "者",
    "图": "圖", "表": "表", "数": "數", "据": "據", "库": "庫", "索": "索",
    "引": "引", "检": "檢", "查": "查", "输": "輸", "入": "入", "出": "出"
  };

  function toTraditional(text) {
    var out = "";
    for (var i = 0; i < text.length; i++) {
      var ch = text.charAt(i);
      out += (S2T[ch] || ch);
    }
    return out;
  }

  function convCompare(text) {
    var lines = text.split(/\r?\n/);
    var res = [];
    var diffCount = 0;
    lines.forEach(function (line) {
      var trad = toTraditional(line);
      if (trad !== line) {
        var pairs = [];
        for (var i = 0; i < line.length; i++) {
          var a = line.charAt(i), b = trad.charAt(i);
          if (a !== b) {
            pairs.push(a + "→" + b);
            diffCount++;
          }
        }
        res.push("简：" + line);
        res.push("繁：" + trad);
        if (pairs.length) { res.push("差异：" + pairs.join("  ")); }
        res.push("");
      } else if (line.trim()) {
        res.push("简：" + line);
        res.push("繁：" + trad + "（无已知差异）");
        res.push("");
      }
    });
    return {
      text: res.join("\n").replace(/\n+$/, "") || "（无内容）",
      diffCount: diffCount
    };
  }

  /* ---------------- UI ---------------- */

  function $(id) { return document.getElementById(id); }

  function setOut(id, html) {
    var el = $(id);
    if (el) { el.innerHTML = html; }
  }

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function levelBadge(level) {
    var label = LEVEL_LABEL[level] || level;
    return '<span class="badge ' + esc(level) + '">' + esc(label) + "</span>";
  }

  function doGanzhi() {
    var y = Number($("yearInput").value);
    try {
      var gz = ganzhiOfYear(y);
      var html = "<strong>" + y + " 年 → " + esc(gz) + "</strong>\n";
      html += "天干 " + esc(gz.charAt(0)) + "（" + esc(TG_WUXING[gz.charAt(0)]) + "）· ";
      html += "地支 " + esc(gz.charAt(1)) + "（" + esc(DZ_WUXING[gz.charAt(1)]) + "）";
      setOut("yearOut", html);
    } catch (e) {
      setOut("yearOut", '<span class="err">输入有误：' + esc(e.message) + "</span>");
    }
  }

  function doJiazi() {
    var t = $("jiaziInput").value;
    try {
      var n = jiaziIndex(t);
      setOut("jiaziOut", "<strong>「" + esc(String(t).trim()) + "」是六十甲子第 " + n + " 位</strong>（共 60）");
    } catch (e) {
      setOut("jiaziOut", '<span class="err">输入有误：' + esc(e.message) + "</span>");
    }
  }

  function doAt() {
    var n = Number($("indexInput").value);
    try {
      var gz = jiaziAt(n);
      setOut("jiaziOut", "<strong>第 " + n + " 位 → " + esc(gz) + "</strong>");
    } catch (e) {
      setOut("jiaziOut", '<span class="err">输入有误：' + esc(e.message) + "</span>");
    }
  }

  function doTerm() {
    var name = $("termInput").value;
    var r = findTerm(name);
    if (!r.term) {
      setOut("termOut", '<span class="err">未找到「' + esc(name) + "」</span>\n可用术语：" +
        r.suggestions.map(esc).join("、"));
      return;
    }
    var g = r.entry;
    var html = "<strong>【" + esc(r.term) + "】</strong>" + levelBadge(g.level) + "\n";
    if (r.alias) { html += "（由别名「" + esc(r.alias) + "」匹配）\n"; }
    if (g.also) { html += "别名：" + g.also.map(esc).join(" / ") + "\n"; }
    html += "\n释义：" + esc(g.summary) + "\n";
    if (g.detail) { html += "说明：" + esc(g.detail) + "\n"; }
    if (g.note) { html += "\n⚠️ 注意：" + esc(g.note) + "\n"; }
    if (g.sources && g.sources.length) {
      html += "\n来源：\n" + g.sources.map(function (s) { return "  · " + esc(s); }).join("\n");
    }
    setOut("termOut", html);
  }

  function doTermList() {
    var rows = [];
    for (var k in GLOSSARY) {
      if (GLOSSARY.hasOwnProperty(k)) {
        rows.push("【" + k + "】" + LEVEL_LABEL[GLOSSARY[k].level] + " — " + GLOSSARY[k].summary);
      }
    }
    setOut("termOut", rows.join("\n"));
  }

  function doCheck() {
    var n = Number($("verseInput").value);
    try {
      var r = checkVerseNumber(n);
      if (r.ok) {
        setOut("verseOut", '<span class="ok">编号 ' + r.input + "：格式通过</span>\n" +
          "所在集次：第 " + r.volumeIndex + " 集\n" +
          "集内位置：第 " + r.positionInVolume + " 位\n" +
          r.note);
      } else {
        setOut("verseOut", '<span class="err">编号 ' + r.input + "：格式不通过</span>\n" + r.note);
      }
    } catch (e) {
      setOut("verseOut", '<span class="err">输入有误：' + esc(e.message) + "</span>");
    }
  }

  function doCite() {
    try {
      var t = cite($("citeInput").value);
      setOut("citeOut", esc(t));
    } catch (e) {
      setOut("citeOut", '<span class="err">' + esc(e.message) + "</span>");
    }
  }

  function doConv() {
    var t = $("convInput").value;
    if (!t.trim()) {
      setOut("convOut", '<span class="err">请输入要对照的文字</span>');
      return;
    }
    var r = convCompare(t);
    setOut("convOut", esc(r.text) + "\n\n— 共 " + r.diffCount + " 处逐字差异 —");
  }

  function doRelation() {
    try {
      var out = ganzhiRelation($("gz1").value, $("gz2").value);
      setOut("relOut", out.map(esc).join("\n"));
    } catch (e) {
      setOut("relOut", '<span class="err">输入有误：' + esc(e.message) + "</span>");
    }
  }

  function buildJiaziTable() {
    var el = $("jiaziTable");
    if (!el || el.dataset.built) { return; }
    var html = "";
    for (var i = 1; i <= 60; i++) {
      var gz = jiaziAt(i);
      html += '<div class="cell" data-gz="' + gz + '"><span class="n">' + i + "</span>" + gz + "</div>";
    }
    el.innerHTML = html;
    el.dataset.built = "1";
    el.addEventListener("click", function (ev) {
      var cell = ev.target.closest ? ev.target.closest(".cell") : null;
      if (!cell) { return; }
      $("jiaziInput").value = cell.dataset.gz;
      doJiazi();
    });
  }

  var ACTIONS = {
    ganzhi: doGanzhi,
    jiazi: doJiazi,
    at: doAt,
    term: doTerm,
    termList: doTermList,
    check: doCheck,
    cite: doCite,
    conv: doConv,
    convClear: function () { $("convInput").value = ""; setOut("convOut", ""); },
    relation: doRelation
  };

  function init() {
    buildJiaziTable();

    document.addEventListener("click", function (ev) {
      var btn = ev.target.closest ? ev.target.closest("[data-act]") : null;
      if (!btn) { return; }
      var fn = ACTIONS[btn.dataset.act];
      if (fn) { fn(); }
    });

    /* 回车即执行 */
    var map = {
      yearInput: doGanzhi, jiaziInput: doJiazi, indexInput: doAt,
      termInput: doTerm, verseInput: doCheck, citeInput: doCite,
      gz1: doRelation, gz2: doRelation
    };
    Object.keys(map).forEach(function (id) {
      var el = $(id);
      if (!el) { return; }
      el.addEventListener("keydown", function (ev) {
        if (ev.key === "Enter") { ev.preventDefault(); map[id](); }
      });
    });

    /* 首次进入给出示例结果，便于理解 */
    doGanzhi();
    buildJiaziTable();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();