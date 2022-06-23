from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Object:

    def __init__(self, name):
        self.name = name
        self.faces = []

    def draw(self):
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for i in range(len(face)):
                glNormal3fv(face[2][i])
                if face[1][i] is not None:
                    glTexCoord2fv(face[1][i])
                glVertex3fv(face[0][i])
        glEnd()
