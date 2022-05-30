import pyglet
import pywavefront
from pywavefront import visualization
from pyglet.gl import *
from pyglet.window import key
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

window = pyglet.window.Window(fullscreen=True)
window.projection = pyglet.window.Projection3D()
scene = pywavefront.Wavefront('Objects/model.obj')

@window.event
def on_draw():
    window.clear()
    visualization.draw(scene)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.LEFT or symbol == key.A:
        glRotated(25,0,1,0)
        glTranslated(25, 0, 0)

if __name__ == "__main__":
    glViewport(0, 0, 500,500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
    for _ in range(4):
        glRotated(25,0,1,0)
        glTranslated(35, 0, 0)

    pyglet.app.run()