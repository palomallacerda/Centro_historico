import pyglet
import pywavefront
from pywavefront import visualization
from pyglet.gl import *
from pyglet.window import key
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

window = pyglet.window.Window(resizable=True)
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
    if symbol == key.RIGHT or symbol == key.D:
        glRotated(-25,0,1,0)
        glTranslated(-25, 0, 0)
    if symbol == key.UP or symbol == key.W:
        glRotated(25,1,0,0)
        glTranslated(0, -25, 0)     
    if symbol == key.DOWN or symbol == key.S:
        glRotated(-25,1,0,0)
        glTranslated(0, 25, 0)      

if __name__ == "__main__":
    # Setando estados para visualização da câmera
    glViewport(0, 0, 500,500)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)

    # Mudando a posição inicial do centro
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
    for _ in range(4):
        glRotated(25,0,1,0)
        glTranslated(35, 0, 0)

    pyglet.app.run()