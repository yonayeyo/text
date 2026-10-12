"""index.html → dist/slip-mobile.html

한 파일만 보내도 열리도록 배경 이미지를 data URI로 넣은 사용성 테스트용 HTML을 만든다.
사용: python3 tools/build_mobile.py
"""
import base64, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
html = (root / 'index.html').read_text(encoding='utf-8')
img = base64.b64encode((root / 'assets/home-bg.webp').read_bytes()).decode()
html = html.replace('url("assets/home-bg.webp")', f'url("data:image/webp;base64,{img}")')
assert 'assets/home-bg.webp' not in html
out = root / 'dist/slip-mobile.html'
out.write_text(html, encoding='utf-8')
print(out, f'{out.stat().st_size / 1024:.0f} KB')
