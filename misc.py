from numpy import *

from inspect import getsourcefile, getsource, getmodule
import dis

getsource(sum)
getsourcefile(sum)

def f(x, y):
    x,y = y,x

dis.dis(f)
dis.disassemble(f)
dis.show_code(f)
dis.code_info(f)

f(1,2)

help(dis)


str(getmodule(sum)).split('\\')[-3]


import sympy as sp

x, y, z, t = sp.symbols('x y z t')
sp.init_printing()
print(sp.Integral(sp.sqrt(1/x), x))
