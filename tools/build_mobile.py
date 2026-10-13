"""index.html → dist/finpick-mobile.html (+ 예전 주소 호환용 dist/slip-mobile.html)

사용성 테스트용으로 보낼 단일 HTML을 만든다. (외부 이미지 없이 index.html 하나로 동작)
사용: python3 tools/build_mobile.py
"""
import pathlib, shutil

root = pathlib.Path(__file__).resolve().parent.parent
for name in ('finpick-mobile.html', 'slip-mobile.html'):
    out = root / 'dist' / name
    shutil.copyfile(root / 'index.html', out)
    print(out, f'{out.stat().st_size / 1024:.0f} KB')
