import bpy
import threading
from time import sleep
from random import randint

def makecubes():
    for i in range(1000):
        bpy.ops.mesh.primitive_cube_add(location=(randint(-10,10),randint(-10,10),randint(-10,10)))
        # bpy.context.scene.update()
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        # sleep(2)
    print('done')

t = threading.Thread(target=makecubes)
t.start()
