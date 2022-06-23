# Classe responsável por verificar cada obj e add textura e modela-lo
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import re

from mesh import Loader


def starts_with(string, word):
    regexp = "\A" + word
    return re.search(regexp, string)

class Draw():
    def __init__(self):
        self.mesh = Loader()

        self.colors = {
        "white": [0.9, 0.9, 0.9, 1],
        "light_gray": [0.7, 0.7, 0.7, 1],
        "gray": [0.5, 0.5, 0.5, 1],
        "dark_gray": [0.3, 0.3, 0.3, 1],
        "black": [0.1, 0.1, 0.1, 1],
        "red": [181/255, 38/255, 51/255, 1],
        "green": [15/255, 102/255, 94/255, 1],
        "mustard": [159/255, 133/255, 76/255, 1],
        "walls": [190/255, 182/255, 170/255, 1],
        "outside_frames": [200/255, 205/255, 211/255, 1],
        "brown": [75/255, 54/255, 33/255, 1],
        "doors": [106/255, 77/255, 73/255, 1],
        "window": [128/255, 124/255, 123/255, 1],
        "floor": [137/255, 122/255, 101/255, 1],
        "beige": [200/255, 188/255, 176/255, 1]
        }

    def load_mesh_from_file(self, file_name):
        self.mesh.load_from_file(file_name)

    def draw_ground_flor(self, x:float, y:float, z:float, color:list):
        glColor4fv(color)
        glBegin(GL_QUADS)
        glVertex3f(-x, -y, z)
        glVertex3f(x, -y, z)
        glVertex3f(x, y/3, z)
        glVertex3f(-x, y/3, z)
        glEnd()


# Mudar para cada obj do modelo
    def draw_objects(self, list_of_objects:list, doors_theta:list):
        if "Ground_Floor" not in list_of_objects:
            self.draw_ground_flor(15, 45, -0.01, self.colors["dark_gray"])

        for obj in self.mesh.objects:
            if obj.name not in list_of_objects:
                if obj.name == "Room":
                    glColor4fv(self.colors["walls"])
                    obj.draw()

                elif obj.name == "Room_Upstairs":
                    glColor4fv(self.colors["walls"])
                    obj.draw()

                elif obj.name == "Room_Back_White":
                    glColor4fv(self.colors["walls"])
                    obj.draw()

                elif obj.name == "Room_Back_Red":
                    glColor4fv(self.colors["red"])
                    obj.draw()

                elif starts_with(obj.name, "Door_Frame"):
                    glColor4fv(self.colors["outside_frames"])
                    obj.draw()

                elif obj.name == "Building_Frame":
                    glColor4fv(self.colors["outside_frames"])
                    obj.draw()

                elif obj.name == "Door_One_Right":
                    #0.013333
                    glColor4fv(self.colors["doors"])
                    glPushMatrix()
                    glTranslatef(-0.670, 0, 0)
                    glRotatef(-doors_theta[0], 0, 0, 1)
                    glTranslatef(0.67, 0, 0)
                    obj.draw()
                    glPopMatrix()

                elif obj.name == "Door_One_Left":
                    glColor4fv(self.colors["doors"])
                    glPushMatrix()
                    glTranslatef(0.67, 0, 0)
                    glRotatef(doors_theta[0], 0, 0, 1)
                    glTranslatef(-0.67, 0, 0)
                    obj.draw()
                    glPopMatrix()

                elif obj.name == "Door_Two_Right":
                    glColor4fv(self.colors["doors"])
                    glPushMatrix()
                    glTranslatef(2.946450, 0, 0)
                    glRotatef(-doors_theta[1], 0, 0, 1)
                    glTranslatef(-2.946450, 0, 0)
                    obj.draw()
                    glPopMatrix()

                elif obj.name == "Door_Two_Left":
                    glColor4fv(self.colors["doors"])
                    glPushMatrix()
                    glTranslatef(4.295177, 0, 0)
                    glRotatef(doors_theta[1], 0, 0, 1)
                    glTranslatef(-4.295177, 0, 0)
                    obj.draw()
                    glPopMatrix()

                elif obj.name == "Door_Three_Right":
                    #0.013333
                    glColor4fv(self.colors["doors"])
                    glPushMatrix()
                    glTranslatef(-4.237305, 0, 0)
                    glRotatef(-doors_theta[2], 0, 0, 1)
                    glTranslatef(4.237305, 0, 0)
                    obj.draw()
                    glPopMatrix()

                elif obj.name == "Door_Three_Left":
                    glColor4fv(self.colors["doors"])
                    glPushMatrix()
                    glTranslatef(-2.888578, 0, 0)
                    glRotatef(doors_theta[2], 0, 0, 1)
                    glTranslatef(2.888578, 0, 0)
                    obj.draw()
                    glPopMatrix()

                elif obj.name == "Window_Frame":
                    glColor4fv(self.colors["outside_frames"])
                    obj.draw()

                elif obj.name == "Window_Door":
                    glColor4fv(self.colors["window"])
                    glPushMatrix()
                    glTranslatef(-0.001326, -0.200821, -4.78602)
                    glRotatef(doors_theta[3], 0, 0, 1)
                    glTranslatef(0.001326, 0.200821, 4.78602)
                    obj.draw()
                    glPopMatrix()

                elif obj.name == "Bench":
                    glColor4fv(self.colors["brown"])
                    obj.draw()

                elif obj.name == "Iphan_Frame.001":
                    glColor4fv(self.colors["green"])
                    obj.draw()

                elif obj.name == "Iphan_Frame.002":
                    glColor4fv(self.colors["red"])
                    obj.draw()

                elif obj.name == "Iphan_Frame.003":
                    glColor4fv(self.colors["mustard"])
                    obj.draw()

                elif starts_with(obj.name, "Art_Display"):
                    glColor4fv(self.colors["white"])
                    obj.draw()

                elif starts_with(obj.name, "Frame"):
                    glColor4fv(self.colors["red"])
                    obj.draw()

                elif starts_with(obj.name, "Column"):
                    glColor4fv(self.colors["beige"])
                    obj.draw()

                elif starts_with(obj.name, "Ceiling_Frame"):
                    glColor4fv(self.colors["brown"])
                    obj.draw()

                elif starts_with(obj.name, "Stairs"):
                    glColor4fv(self.colors["beige"])
                    obj.draw()

                elif obj.name == "Floor":
                    glColor4fv(self.colors["floor"])
                    obj.draw()

                elif obj.name == "Ceiling":
                    glColor4fv(self.colors["brown"])
                    obj.draw()

# Precisamos das imagens para add a textura
# def loadTexture():
#     textureSurface = pygame.image.load('texture2.png')
#     textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
#     width = textureSurface.get_width()
#     height = textureSurface.get_height()

#     glEnable(GL_TEXTURE_2D)
#     texid = glGenTextures(1)

#     glBindTexture(GL_TEXTURE_2D, texid)
#     glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
#                  0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

#     return texid