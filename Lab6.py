#!/usr/bin/env python3
"""klawisz T - wł./wył. ściany
klawisz B - przełączanie tekstur
klawisze 1-4 - przełączanie kształtów
1 - kwadrat, 2 - ostrosłup, 3 - jajo"""
import math
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image

image1 = Image.open("biernat.tga")
image2 = Image.open("kitku.tga")

showing_image1 = True
see_wall = True
shape = 1  # kwadrat - 1, ostrosłup - 2, jajo - 3
number_of_samples = 64  # do jajka
vertices = []

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


def load_texture(image):
    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    )


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    load_texture(image1)


def shutdown():
    pass


def egg_calc_x(u, v):
    return (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.cos(math.pi * v)


def egg_calc_y(u):
    return 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5


def egg_calc_z(u, v):
    return (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.sin(math.pi * v)


def egg_define_vertices():
    for v in range(number_of_samples):
        new_list_vertices = []
        vertices.append(new_list_vertices)
        for u in range(number_of_samples):
            new_u = u / (number_of_samples - 1)
            new_v = v / (number_of_samples - 1)
            new_list_vertices.append([egg_calc_x(new_u, new_v), egg_calc_y(new_u), egg_calc_z(new_u, new_v)])


def square():
    glBegin(GL_TRIANGLE_STRIP)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, -5.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-5.0, 5.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(5.0, 5.0, 0.0)
    glEnd()


def pyramid():
    glBegin(GL_TRIANGLE_STRIP)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, 0.0, -5.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, 0.0, -5.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-5.0, 0.0, 5.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(5.0, 0.0, 5.0)
    glEnd()

    glBegin(GL_TRIANGLE_FAN)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 5.0, 0.0)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(-5.0, 0.0, -5.0)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, 0.0, 5.0)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, 0.0, 5.0)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(5.0, 0.0, -5.0)

    if see_wall:
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-5.0, 0.0, -5.0)
    glEnd()


def egg():
    """tekstura na jaju niezbyt dobrze się nałożyła, próbowałem lepiej ją nałożyć ale nie wychodziło :c"""
    glBegin(GL_TRIANGLE_STRIP)
    for v in range(number_of_samples - 1):
        new_v = 1 - v / number_of_samples
        glTexCoord2f(new_v, 0)
        glVertex3fv(vertices[v][0])

        glTexCoord2f(new_v, 0)
        glVertex3fv(vertices[v + 1][0])
        for u in range(1, number_of_samples):
            new_u = 1 - u / number_of_samples
            if new_u < 0.5:
                glTexCoord2f(new_v, new_u)
                glVertex3fv(vertices[v][u])

                glTexCoord2f(new_v, new_u)
                glVertex3fv(vertices[v + 1][u])
            else:
                # bez ifa te trójkąty byłyby widoczne z wewnątrz jajka, zamiast na zewnątrz,
                # kolejność rysowania wierzchołków
                glTexCoord2f(new_v, new_u)
                glVertex3fv(vertices[v + 1][u])

                glTexCoord2f(new_v, new_u)
                glVertex3fv(vertices[v][u])
    glEnd()


def render(time):
    global theta
    global phi

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    if shape == 1:
        square()
    elif shape == 2:
        pyramid()
    elif shape == 3:
        egg()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global see_wall, showing_image1, shape
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    elif key == GLFW_KEY_T and action == GLFW_PRESS:
        see_wall = not see_wall
    elif key == GLFW_KEY_B and action == GLFW_PRESS:
        showing_image1 = not showing_image1
        if showing_image1:
            load_texture(image1)
        else:
            load_texture(image2)
    elif key == GLFW_KEY_1 and action == GLFW_PRESS:
        shape = 1
    elif key == GLFW_KEY_2 and action == GLFW_PRESS:
        shape = 2
    elif key == GLFW_KEY_3 and action == GLFW_PRESS:
        shape = 3


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global delta_y
    global mouse_x_pos_old
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    delta_y = y_pos - mouse_y_pos_old
    mouse_x_pos_old = x_pos
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    egg_define_vertices()

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
