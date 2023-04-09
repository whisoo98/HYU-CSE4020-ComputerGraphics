import glfw
import numpy as np
from OpenGL.GL import *

draw_type = GL_LINE_LOOP
vertexs = np.array([])

def KeyCallback(window, key, scancode, action, mods):
    global draw_type
    if key == glfw.KEY_0 and action == glfw.PRESS:
        draw_type = GL_POLYGON
    elif key == glfw.KEY_1 and action == glfw.PRESS:
        draw_type = GL_POINTS
    elif key == glfw.KEY_2 and action == glfw.PRESS:
        draw_type = GL_LINES
    elif key == glfw.KEY_3 and action == glfw.PRESS:
        draw_type = GL_LINE_STRIP
    elif key == glfw.KEY_4 and action == glfw.PRESS:
        draw_type = GL_LINE_LOOP
    elif key == glfw.KEY_5 and action == glfw.PRESS:
        draw_type = GL_TRIANGLES
    elif key == glfw.KEY_6 and action == glfw.PRESS:
        draw_type = GL_TRIANGLE_STRIP
    elif key == glfw.KEY_7 and action == glfw.PRESS:
        draw_type = GL_TRIANGLE_FAN
    elif key == glfw.KEY_8 and action == glfw.PRESS:
        draw_type = GL_QUADS
    elif key == glfw.KEY_9 and action == glfw.PRESS:
        draw_type = GL_QUAD_STRIP
    elif key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window = window, value = glfw.TRUE)
        
def makeVertexs():
    global vertexs
    radians = np.linspace(start = 0, stop = np.pi*2, num=13)
    vertex_list = []
    # 1st quater
    for radian in radians:
        
        vertex_list.append((np.cos(radian),np.sin(radian)))
    # 2nd quater
    vertex_list.pop()
    vertexs = np.array(vertex_list)
        
def Render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(draw_type)
    for vertex in vertexs:
        glVertex2fv(vertex)
    glEnd()
    

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(480,480,"2018008240-2-2",None,None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    
    glfw.set_key_callback(window,KeyCallback)
    glfw.swap_interval(1)
    makeVertexs()
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        Render()
        glfw.swap_buffers(window)
    
    glfw.terminate()

if __name__ == "__main__":
    main()