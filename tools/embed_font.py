"""Pretendard Variable을 페이지에 쓰인 글자만 남겨 index.html에 base64로 넣는다.

사용법: python3 tools/embed_font.py <PretendardVariable.woff2 경로>
(npm pack pretendard 로 받은 패키지의 dist/web/variable/woff2/ 안에 있음)
"""
import base64, re, subprocess, sys, tempfile, pathlib

html_path = pathlib.Path(__file__).resolve().parent.parent / "index.html"
src_font = sys.argv[1]
html = html_path.read_text(encoding="utf-8")
body = re.sub(r"/\*FONT:START\*/.*?/\*FONT:END\*/", "", html, flags=re.S)
chars = set(body) | set(map(chr, range(0x20, 0x7F))) | set("₩−·…→←↑↓✓✕▲▼")
with tempfile.TemporaryDirectory() as d:
    txt = pathlib.Path(d, "chars.txt"); txt.write_text("".join(sorted(chars)), encoding="utf-8")
    out = pathlib.Path(d, "sub.woff2")
    subprocess.run(["pyftsubset", src_font, f"--text-file={txt}", "--flavor=woff2",
                    "--layout-features=*", f"--output-file={out}"], check=True)
    b64 = base64.b64encode(out.read_bytes()).decode()
face = ("/*FONT:START*/\n@font-face{font-family:\"Pretendard Variable\";font-weight:45 920;font-style:normal;"
        f"font-display:swap;src:url(data:font/woff2;base64,{b64}) format(\"woff2-variations\")}}\n/*FONT:END*/")
html = re.sub(r"/\*FONT:START\*/.*?/\*FONT:END\*/", lambda _: face, html, flags=re.S)
html_path.write_text(html, encoding="utf-8")
print(f"embedded {len(b64)//1024} KB, {len(chars)} chars")
