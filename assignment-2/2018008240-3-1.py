import numpy as np
import glfw
from OpenGL.GL import *


def KeyCallback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window=window, value=glfw.TRUE)


def Render(T):
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
        t = glfw.get_time()
        d = 0.5
        th = np.radians(t)
        s = np.sin(t)
        c = np.cos(t)
        S = np.array([[1., 0., 0.],
                     [0., 1., 0.],
                     [0., 0., 1.]])
        R = np.array([[c, -s, 0.],
                      [s, c, 0.],
                      [0, 0, 1.]])
        T = np.array([[1., 0., 0.4],
                      [0.,  1., 0.4],
                      [0., 0., 1.]])

        # Render(R)
        Render(R@T)
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
