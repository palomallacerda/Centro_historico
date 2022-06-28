# Basic OBJ file viewer. needs objloader from:
#  http://www.pygame.org/wiki/OBJFileLoader
# LMB + move: rotate
# RMB + move: pan
# Scroll wheel: zoom in/out
import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *

# IMPORT OBJECT LOADER
from OBJLoader import *

pygame.init()
pygame.display.set_caption('Elevador Lacerda - UFAL2022')
viewport = (800,600)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
LIGHT_SIZE = 7
LIGHT_COUNT = 3

glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 100.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (1.2, 1.2, 1.2, 100.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (30.5, 30.5, 30.5, 100.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded

rx, ry= (0,0)
tx, ty = (0,0)
zpos = 0 
rotate = move = False

# LOAD OBJECT AFTER PYGAME INIT
obj = OBJ(sys.argv[1], swapyz=True)

clock = pygame.time.Clock()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width/float(height), 1, 100.0)
gluLookAt(rx, ry, zpos, 0, 0, -5, 0, 1, 0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)



while 1:
    clock.tick(30)
    glEnable(GL_TEXTURE_3D)
    pressed_keyboard = pygame.key.get_pressed()
    
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()
        elif e.type == MOUSEBUTTONDOWN: #Enable mouse operations
            if e.button == 4: zpos = max(1, zpos-1)
            elif e.button == 5: zpos += 1
            elif e.button == 1: rotate = True
            elif e.button == 3: move = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1: rotate = False
            elif e.button == 3: move = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                rx += i
                ry += j
            if move:
                tx += i
                ty -= j
        if e.type == pygame.KEYDOWN: #Enable keyborads operations
            if e.key == pygame.K_d:
                rx +=10
            if e.key == pygame.K_a:
                rx -=10
            if e.key == pygame.K_e:
                ry += 10
            if e.key == pygame.K_s:
                ry -= 10
        


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # RENDER OBJECT
    glTranslate(tx/20., ty/20., - zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    glCallList(obj.gl_list)



    pygame.display.flip()
