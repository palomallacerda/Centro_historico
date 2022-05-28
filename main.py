import pyglet
import pywavefront
from pywavefront import visualization
from pyglet.gl import *

window = pyglet.window.Window(fullscreen=True)
window.projection = pyglet.window.Projection3D()
scene = pywavefront.Wavefront('model.obj')

@window.event
def on_draw():
    window.clear()
    visualization.draw(scene)


if __name__ == "__main__":
    glEnable(GL_MULTISAMPLE_ARB)
    glEnable(GL_DEPTH_TEST)

    glTranslatef(0, 0, -3)
    pyglet.app.run()