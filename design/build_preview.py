#!/usr/bin/env python3
"""Build a standalone preview (../index.html) from the canvas artboards.

The canvas artboards (project/*.dc.html) need the canvas runtime to render.
This script lifts each artboard's <helmet> styles and markup into one plain
HTML page so the screens can be opened directly from the repository.
"""
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE / "project"
OUT = HERE.parent / "index.html"


def scope_css(css: str, scope: str) -> str:
    out = []
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        sels, body = m.group(1).strip(), m.group(2)
        if sels == "body":
            continue
        parts, depth, cur = [], 0, ""
        for ch in sels:
            depth += ch == "("
            depth -= ch == ")"
            if ch == "," and depth == 0:
                parts.append(cur)
                cur = ""
            else:
                cur += ch
        parts.append(cur)
        scoped = ",".join(f"{scope} {s.strip()}" for s in parts)
        out.append(f"{scoped}{{{body}}}")
    return "\n".join(out)


def extract(path: pathlib.Path, sid: str):
    src = path.read_text(encoding="utf-8")
    helmet = re.search(r"<helmet>(.*?)</helmet>", src, re.S).group(1)
    css = re.search(r"<style>(.*?)</style>", helmet, re.S).group(1)
    body = re.search(r"</helmet>(.*?)</x-dc>", src, re.S).group(1)
    body = re.sub(r'href="([A-Za-z0-9_-]+)\.dc\.html"', r'href="#\1"', body)
    return scope_css(css, f"#{sid}"), body.strip()


def main():
    canvas = json.loads((PROJECT / "canvas.json").read_text(encoding="utf-8"))
    boards = canvas["boards"]
    rows = sorted(canvas["notes"].values(), key=lambda n: n["y"])
    styles, sections = [], []
    for i, note in enumerate(rows):
        lo = note["y"]
        hi = rows[i + 1]["y"] if i + 1 < len(rows) else float("inf")
        names = sorted((n for n, b in boards.items() if lo < b["y"] < hi), key=lambda n: boards[n]["x"])
        cards = []
        for name in names:
            sid = name.removesuffix(".dc.html")
            css, body = extract(PROJECT / name, sid)
            styles.append(css)
            cards.append(
                f'<figure class="scr" id="{sid}"><figcaption>{boards[name].get("title", sid)}</figcaption>'
                f'<div class="frame">{body}</div></figure>'
            )
        sections.append(f'<section class="grp"><h2>{note["text"]}</h2><div class="list">{"".join(cards)}</div></section>')

    html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>청년 금융 실천 앱</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,300..600&amp;family=Noto+Sans+KR:wght@300;400;500&amp;display=swap">
<style>
:root{{color-scheme:dark}}
body{{margin:0;background:#151515;color:#fff;font-family:"Archivo","Noto Sans KR",sans-serif;font-stretch:112%}}
header{{padding:48px 16px 8px;max-width:2400px;margin:0 auto}}
header h1{{font-weight:300;font-size:40px;letter-spacing:-.03em;margin:0;line-height:1.15}}
header p{{opacity:.6;margin:12px 0 0;font-size:14px}}
.grp{{padding:32px 16px;max-width:2400px;margin:0 auto}}
.grp h2{{font-weight:300;font-size:24px;margin:0 0 20px;letter-spacing:-.02em}}
.list{{display:flex;flex-wrap:wrap;gap:40px;align-items:flex-start}}
.scr{{margin:0;width:390px;max-width:100%}}
.scr figcaption{{font-size:13px;opacity:.6;margin-bottom:10px}}
.frame{{border-radius:44px;overflow:hidden;width:390px;max-width:100%;overflow-x:auto}}
</style>
<style>
{chr(10).join(styles)}
</style>
</head>
<body>
<header><h1>청년 금융 실천 앱<br>화면 디자인</h1><p>각 화면의 하단 내비게이션과 버튼은 해당 화면으로 이동해요.</p></header>
{"".join(sections)}
</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.relative_to(HERE.parent)} ({len(html):,} bytes, {len(boards)} screens)")


if __name__ == "__main__":
    main()
