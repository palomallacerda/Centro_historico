import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from TextureLoader import load_texture
from ObjLoader import ObjLoader


vertex_src = """
# version 330
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;
uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;
out vec2 v_texture;
void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

fragment_src = """
# version 330
in vec2 v_texture;
out vec4 out_color;
uniform sampler2D s_texture;
void main()
{
    out_color = texture(s_texture, v_texture);
}
"""


# glfw callback functions
def window_resize(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)


# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# creating the window
window = glfw.create_window(1280, 720, "Elevador_Lacerda", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# set window's position
glfw.set_window_pos(window, 400, 200)

# set the callback function for window resize
glfw.set_window_size_callback(window, window_resize)

# make the context current
glfw.make_context_current(window)

# load here the 3d meshes
ele_indices, ele_buffers = ObjLoader.load_model("Objects/Elevador.obj")

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

# VAO and VBO
VAO = glGenVertexArrays(2)
VBO = glGenBuffers(2)
# EBO = glGenBuffers(1)

# Elevador VAO
glBindVertexArray(VAO[0])
# Elevador Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
glBufferData(GL_ARRAY_BUFFER, ele_buffers.nbytes, ele_buffers, GL_STATIC_DRAW)

# Ele vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, ele_buffers.itemsize * 8, ctypes.c_void_p(0))
# Ele textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, ele_buffers.itemsize * 8, ctypes.c_void_p(12))
# Ele normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, ele_buffers.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

textures = glGenTextures(8)
load_texture("Objects/Material2_extractedTex8168.jpg", textures[0])
load_texture("Objects/Material3_extractedTex818.jpg", textures[1])
load_texture("Objects/Material4_extractedTex5027.jpg", textures[2])
load_texture("Objects/Material5_extractedTex5941.jpg", textures[3])
load_texture("Objects/Material6_extractedTex2490.jpg", textures[4])
load_texture("Objects/Material9_extractedTex2972.jpg", textures[5])
load_texture("Objects/Material29_extractedTex4581.png", textures[6])
load_texture("Objects/Material30_extractedTex2346.jpg", textures[7])

glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
Ele_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -5, -10]))
# monkey_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-4, 0, 0]))

# eye, target, up
view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 8]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, Ele_pos)

    # draw the Ele character
    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glBindTexture(GL_TEXTURE_2D, textures[2])
    glBindTexture(GL_TEXTURE_2D, textures[3])
    glBindTexture(GL_TEXTURE_2D, textures[4])
    glBindTexture(GL_TEXTURE_2D, textures[5])
    glBindTexture(GL_TEXTURE_2D, textures[6])
    glBindTexture(GL_TEXTURE_2D, textures[7])

    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(ele_indices))


    rot_y = pyrr.Matrix44.from_y_rotation(-0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(rot_y, Ele_pos)

# terminate glfw, free up allocated resources
glfw.terminate()