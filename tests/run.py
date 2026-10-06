import sys

sys.path.insert(0, ".test-tools")
from lupa import LuaRuntime

LuaRuntime().execute("dofile('tests/smoke.lua')")
