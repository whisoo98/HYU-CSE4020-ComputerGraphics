import glfw
import numpy as np
from OpenGL.GL import *

draw_type = GL_LINE_LOOP
vertexs = np.array([])
degreeTx = 0
degreeGR = 0
degreeLR = 0
degreeSx = 1.0


def KeyCallback(window, key, scancode, action, mods):
    global degreeTx
    global degreeGR
    global degreeLR
    global degreeSx
    if key == glfw.KEY_Q and action == glfw.PRESS:
        degreeTx = degreeTx - 0.1
    elif key == glfw.KEY_E and action == glfw.PRESS:
        degreeTx = degreeTx + 0.1
    elif key == glfw.KEY_A and action == glfw.PRESS:
        degreeLR = degreeLR + 10
    elif key == glfw.KEY_D and action == glfw.PRESS:
        degreeLR = degreeLR - 10
    elif key == glfw.KEY_1 and action == glfw.PRESS:
        degreeTx = 0
        degreeGR = 0
        degreeLR = 0
        degreeSx = 1.0
    elif key == glfw.KEY_W and action == glfw.PRESS:
        degreeSx = degreeSx * 0.9
    elif key == glfw.KEY_S and action == glfw.PRESS:
        degreeGR = degreeGR + 10
    elif key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window=window, value=glfw.TRUE)


def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([1., 0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([0., 1.]))
    glEnd()

    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv((T @ np.array([.0, .5, 1.]))[:-1])
    glVertex2fv((T @ np.array([.0, .0, 1.]))[:-1])
    glVertex2fv((T @ np.array([.5, .0, 1.]))[:-1])
    glEnd()


def main():
    if not glfw.init():
        return

    window = glfw.create_window(480, 480, "2018008240-3-1", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glfw.set_key_callback(window, KeyCallback)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        cl = np.cos(degreeLR*np.pi/180)
        sl = np.sin(degreeLR*np.pi/180)
        c = np.cos(degreeGR*np.pi/180)
        s = np.sin(degreeGR*np.pi/180)
        GR = np.array([[c, -s, 0.],
                      [s, c, 0.],
                      [0., 0., 1.]])
        T = np.array([[1., 0., degreeTx],
                      [0., 1., 0.],
                      [0., 0., 1.]])
        LR = np.array([[cl, -sl, 0.],
                      [sl, cl, 0.],
                      [0., 0., 1.]])
        S = np.array([[degreeSx, 0., 0.],
                      [0., degreeSx, 0.],
                      [0., 0., 1.]])

        render(GR@T@LR@S)
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
