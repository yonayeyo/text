"""index.html → dist/slip-mobile.html

사용성 테스트용으로 보낼 단일 HTML을 만든다. (외부 이미지 없이 index.html 하나로 동작)
사용: python3 tools/build_mobile.py
"""
import pathlib, shutil

root = pathlib.Path(__file__).resolve().parent.parent
out = root / 'dist/slip-mobile.html'
shutil.copyfile(root / 'index.html', out)
print(out, f'{out.stat().st_size / 1024:.0f} KB')
