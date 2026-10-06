import pathlib
import sys

sys.path.insert(0, ".test-tools")
from lupa.lua51 import LuaRuntime

root = pathlib.Path(__file__).resolve().parents[1]
LuaRuntime().execute((root / 'tests/smoke.lua').read_text(encoding='utf-8'))
