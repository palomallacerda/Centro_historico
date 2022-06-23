import math
import pygame
from pygame.locals import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from enum import Enum

from drawing import Draw

atraso = 1000//60

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640
STEP_DISTANCE = 0.2
STEP_THETA = 0.2

velocidade = 2 

notDraw = []

draw = None

dimensao = (WINDOW_WIDTH, WINDOW_HEIGHT)
center = [WINDOW_WIDTH//2, WINDOW_HEIGHT//2]
display = None
theta_angle_horizontal = 0 # the vertical angle which you are looking at the model
theta_angle_vertical = 0 # the vertical angle which you are looking at the model

camera = [0, 15, 0] # camera position

# variables to control each one of the two doors
doors = [False, False]
doors_theta = [0.0, 0.0]
doors_direction = [-1, -1]

view_matrix = []    # the view matrix, we only keep track of it because we can't
                    # rotate the two axis at the same time without distortion

class Door(Enum):
    center = 0
    left = 1
    right = 2
    window = 3

class Pos(Enum):
    x = 0
    y = 1
    z = 2

class Visibility(Enum):
    hide = 0
    show = 1

def load_mesh(file_name):
    global draw

    draw = Draw()
    draw.load_mesh_from_file(file_name)

def init():
    global display
    global view_matrix

    pygame.init()
    display = pygame.display.set_mode(dimensao, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Elevador_Lacerda')

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.7, 0.7, 0.7, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.9, 0.9, 0.9, 1])
    glLightfv(GL_LIGHT1, GL_POSITION, [1, 1, 0, 1])

    glShadeModel(GL_SMOOTH)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 60.0)

    glMatrixMode(GL_MODELVIEW)
    gluLookAt(camera[Pos.x.value], camera[Pos.y.value], camera[Pos.z.value],
    0, 0, 0, 0, 0, 1)

    view_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    glLoadIdentity()

    pygame.mouse.set_pos(center)

def move_camera_with_keypress(keypress):
    global camera
    global velocidade

    moving_distance = STEP_DISTANCE * velocidade

    if keypress[pygame.K_m]:
        velocidade += 1
    if keypress[pygame.K_n]:
        if velocidade > 1:
            velocidade -= 1

    if keypress[pygame.K_w]:
        camera[Pos.z.value] += moving_distance
        glTranslatef(0, 0, moving_distance)
    if keypress[pygame.K_s]:
        camera[Pos.z.value] -= moving_distance
        glTranslatef(0, 0,-moving_distance)
    if keypress[pygame.K_d]:
        camera[Pos.x.value] -= moving_distance
        glTranslatef(-moving_distance, 0, 0)
    if keypress[pygame.K_a]:
        camera[Pos.x.value] += moving_distance
        glTranslatef(moving_distance, 0, 0)
    if keypress[pygame.K_q]:
        camera[Pos.y.value] -= moving_distance
        glTranslatef(0, -moving_distance, 0)
    if keypress[pygame.K_e]:
        camera[Pos.y.value] += moving_distance
        glTranslatef(0, moving_distance, 0)

    global theta_angle_vertical, theta_angle_horizontal
def view_update(mouse_pos, keypress):
    global view_matrix

    glLoadIdentity()

    theta_angle_vertical += mouse_pos[1] * STEP_THETA
    glRotatef(theta_angle_vertical, 1, 0, 0)

    glPushMatrix()
    glLoadIdentity()

    theta_angle_horizontal += STEP_THETA
    move_camera_with_keypess(keypress)

    glRotatef(mouse_pos[0] * STEP_THETA, 0, 1, 0)

    glMultMatrixf(view_matrix)
    view_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    glPopMatrix()
    glMultMatrixf(view_matrix)

def change_obj_visibility(name, allow_see=None):
    global notDraw

    if allow_see is None:
        if name not in notDraw:
            notDraw.append(name)
        else:
            notDraw.remove(name)

    elif allow_see == Visibility.hide and \
    name not in notDraw:
        notDraw.append(name)

    elif allow_see == Visibility.show and \
    name in notDraw:
        notDraw.remove(name)

def visibility_update(keypress):
    global allow_see

    if keypress[pygame.K_g]:
        change_obj_visibility("o Morro_Cube.010")
        change_obj_visibility("Torre_B_Elevador_Cube.002")
        change_obj_visibility("Corredor_Cube.006")
        change_obj_visibility("Torre_A_Predio_Cube")
        change_obj_visibility("Base_Cube.005")
        change_obj_visibility("Adorno_Colunas_Cube.012")
        change_obj_visibility("Grades_Plane")
        change_obj_visibility("Torre_B_Elevador_topo_Cube.001")
        change_obj_visibility("Sacada_Sketchup.005")

    # if keypress[pygame.K_b]:
    #     change_obj_visibility("Room")
    #     change_obj_visibility("Room_Upstairs")
    #     change_obj_visibility("Iphan_Frame.001")
    #     change_obj_visibility("Iphan_Frame.002")
    #     change_obj_visibility("Iphan_Frame.003")

    # if keypress[pygame.K_u]:
    #     change_obj_visibility("Stairs_Base")
    #     change_obj_visibility("Stairs.001")
    #     change_obj_visibility("Stairs.002")

    # if keypress[pygame.K_h]:
    #     change_obj_visibility("Ceiling", Visibility.hide)
    #     change_obj_visibility("Ceiling_Frame.001", Visibility.hide)
    #     change_obj_visibility("Ceiling_Frame.002", Visibility.hide)
    #     change_obj_visibility("Ceiling_Frame.003", Visibility.hide)
    #     change_obj_visibility("Door_Frame.001", Visibility.hide)
    #     change_obj_visibility("Door_Frame.002", Visibility.hide)
    #     change_obj_visibility("Door_Frame.003", Visibility.hide)
    #     change_obj_visibility("Building_Frame", Visibility.hide)
    #     change_obj_visibility("Room", Visibility.hide)
    #     change_obj_visibility("Room_Upstairs", Visibility.hide)
    #     change_obj_visibility("Stairs_Base", Visibility.hide)
    #     change_obj_visibility("Stairs.001", Visibility.hide)
    #     change_obj_visibility("Stairs.002", Visibility.hide)
    #     change_obj_visibility("Iphan_Frame.001", Visibility.hide)
    #     change_obj_visibility("Iphan_Frame.002", Visibility.hide)
    #     change_obj_visibility("Iphan_Frame.003", Visibility.hide)

    # if keypress[pygame.K_j]:
    #     change_obj_visibility("Ceiling", Visibility.show)
    #     change_obj_visibility("Ceiling_Frame.001",  Visibility.show)
    #     change_obj_visibility("Ceiling_Frame.002",  Visibility.show)
    #     change_obj_visibility("Ceiling_Frame.003",  Visibility.show)
    #     change_obj_visibility("Door_Frame.001",  Visibility.show)
    #     change_obj_visibility("Door_Frame.002",  Visibility.show)
    #     change_obj_visibility("Door_Frame.003",  Visibility.show)
    #     change_obj_visibility("Building_Frame",  Visibility.show)
    #     change_obj_visibility("Room", Visibility.show)
    #     change_obj_visibility("Room_Upstairs",  Visibility.show)
    #     change_obj_visibility("Stairs_Base",  Visibility.show)
    #     change_obj_visibility("Stairs.001",  Visibility.show)
    #     change_obj_visibility("Stairs.002",  Visibility.show)
    #     change_obj_visibility("Iphan_Frame.001",  Visibility.show)
    #     change_obj_visibility("Iphan_Frame.002",  Visibility.show)
    #     change_obj_visibility("Iphan_Frame.003",  Visibility.show)

def change_state_door(door:int):
    global doors

    doors[door] = not doors[door]

def open_door(door:int):
    global doors
    global doors_theta
    global doors_direction

    if 0 < doors_theta[door] < 90:
        doors_theta[door] += doors_direction[door] * velocidade
        if doors_theta[door] > 90:
            doors_theta[door] = 90
            change_state_door(door)
        elif doors_theta[door] < 0:
            doors_theta[door] = 0
            change_state_door(door)

    elif doors_theta[door] == 0 or doors_theta[door] == 90:
        doors_direction[door] *= -1
        doors_theta[door] += doors_direction[door] * 0.00001

def main():
    global display

    is_paused = False
    is_set_to_close = False
    mouse_pos = [0, 0]

    load_mesh("Objects/torre_a.obj")
    # load_mesh(".obj")
    init()

    while not is_set_to_close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_set_to_close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_set_to_close = True
                elif event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                    is_paused = not is_paused
                    pygame.mouse.set_pos(center)
                elif event.key == pygame.K_1:
                    change_state_door(Door.center.value)
                elif event.key == pygame.K_2:
                    change_state_door(Door.left.value)
                elif event.key == pygame.K_3:
                    change_state_door(Door.right.value)
                elif event.key == pygame.K_4:
                    change_state_door(Door.window.value)
                else:
                    visibility_update(pygame.key.get_pressed())

            if not is_paused:
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = [event.pos[i] - center[i] for i in \
                        range(2)]
                pygame.mouse.set_pos(center)

        if not is_paused:
            keypress = pygame.key.get_pressed()

            view_update(mouse_pos, keypress)

            for door in Door:
                if doors[door.value]:
                    open_door(door.value)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glPushMatrix()
            draw.draw_objects(notDraw, doors_theta)
            glPopMatrix()

            pygame.display.flip()
            pygame.time.wait(atraso)

    pygame.quit()

if __name__ == "__main__":
    main()
