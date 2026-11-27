#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 GitHub 风格的本地 HTML 预览，用于渲染/可访问性验证。

用法：
    python scripts/build_preview.py [输出目录]

注意：这是【验证用】工具，产物不进公开仓库。
"""

import os
import sys
import markdown

GH_CSS = """
:root { --fg:#1f2328; --muted:#59636e; --border:#d1d9e0; --bg:#ffffff;
        --code-bg:#f6f8fa; --link:#0969da; --accent:#bf3a2b; }
* { box-sizing: border-box; }
body { margin:0; padding:24px 16px; background:var(--bg); color:var(--fg);
       font: 16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC",
             "Noto Sans TC","PingFang SC","Microsoft YaHei",Helvetica,Arial,sans-serif;
       -webkit-font-smoothing: antialiased; }
.markdown-body { max-width: 980px; margin: 0 auto; word-wrap: break-word; }
h1,h2,h3,h4 { margin-top:24px; margin-bottom:16px; font-weight:600; line-height:1.25; }
h1 { font-size:2em; padding-bottom:.3em; border-bottom:1px solid var(--border); }
h2 { font-size:1.5em; padding-bottom:.3em; border-bottom:1px solid var(--border); }
h3 { font-size:1.25em; }
a { color:var(--link); text-decoration:none; }
a:hover { text-decoration:underline; }
code { background:var(--code-bg); padding:.2em .4em; border-radius:6px;
       font-size:85%; font-family:ui-monospace,SFMono-Regular,"SF Mono",Menlo,monospace; }
pre { background:var(--code-bg); padding:16px; overflow:auto; border-radius:6px; }
pre code { background:none; padding:0; font-size:100%; }
table { border-collapse:collapse; display:block; width:max-content; max-width:100%;
        overflow:auto; margin:16px 0; }
th,td { border:1px solid var(--border); padding:6px 13px; }
th { background:var(--code-bg); font-weight:600; }
tr:nth-child(2n) { background:#f6f8fa; }
blockquote { margin:0 0 16px; padding:0 1em; color:var(--muted);
             border-left:.25em solid var(--border); }
hr { height:.25em; padding:0; margin:24px 0; background:var(--border); border:0; }
img { max-width:100%; }
ul,ol { padding-left:2em; }
@media (max-width: 480px) {
  body { padding: 16px 12px; font-size:15px; }
  h1 { font-size:1.6em; } h2 { font-size:1.3em; }
  table { font-size:14px; }
}
"""

def convert(src, dst):
    text = open(src, encoding="utf-8").read()
    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "toc", "attr_list", "sane_lists"],
    )
    lang = "zh-Hans"
    if ".en." in os.path.basename(src) or "/en/" in src.replace("\\", "/"):
        lang = "en"
    elif ".zh-HK." in os.path.basename(src) or "/zh-hk/" in src.replace("\\", "/"):
        lang = "zh-Hant-HK"
    elif ".zh-TW." in os.path.basename(src) or "/zh-tw/" in src.replace("\\", "/"):
        lang = "zh-Hant-TW"

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{os.path.basename(src)}</title>
<style>{GH_CSS}</style>
</head>
<body>
<article class="markdown-body">
{body}
</article>
</body>
</html>"""
    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    open(dst, "w", encoding="utf-8").write(html)
    return len(html)


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, "_preview")
    out = os.path.abspath(out)

    targets = []
    for fn in ["README.md", "README.zh-HK.md", "README.zh-TW.md", "README.en.md"]:
        targets.append((fn, fn.replace(".md", ".html")))
    for lang in ["zh-hans", "zh-hk", "zh-tw", "en"]:
        for fn in ["index.md", "glossary.md"]:
            targets.append((os.path.join("docs", lang, fn),
                            f"{lang}_{fn.replace('.md', '.html')}"))

    total = 0
    for src_rel, dst_rel in targets:
        src = os.path.join(root, src_rel)
        if not os.path.exists(src):
            print(f"SKIP (missing): {src_rel}")
            continue
        n = convert(src, os.path.join(out, dst_rel))
        print(f"OK {src_rel:32s} -> {dst_rel:28s} {n:>7d} bytes")
        total += n

    print(f"\n共生成 {len(targets)} 个预览页，输出目录：{out}")
    print(f"总字节：{total}")


if __name__ == "__main__":
    main()