import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.test-tools'))
from lupa.lua51 import LuaRuntime

runtime = LuaRuntime()
compile_lua = runtime.eval('function(source, name) local fn, err = loadstring(source, name); assert(fn, err) end')
for path in (ROOT / 'mod').rglob('*.lua'):
    compile_lua(path.read_text(encoding='utf-8'), str(path))
print('PASS: all runtime Lua files compile under Lua 5.1')
runtime.execute((ROOT / 'tests/loot_extensions.lua').read_text(encoding='utf-8'))
