#!/usr/bin/env python3

# domyślnie włącza się program na 4.5 - jajko narysowane za pomocą triangle_strip
# aby narysować jajko innym sposobem, należy odkomentować odpowiednią funkcję w render
# aby narysować torus należy w mainie zakomentować obliczanie wierzchołków dla jajka
# i odkomentować obliczanie pozycji wierzchołków dla torusa

import sys
import math
import random

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

number_of_samples = 15
big_r = 10
small_r = 2

vertices = []
colors = []


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def spin(angle):
    angle *= 20
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def egg_calc_x(u, v):
    return (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.cos(math.pi * v)


def egg_calc_y(u):
    return 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2


def egg_calc_z(u, v):
    return (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.sin(math.pi * v)


def egg_define_vertices_and_colors():
    for v in range(number_of_samples - 1):
        new_list_vertices = []
        vertices.append(new_list_vertices)
        new_list_colors = []
        colors.append(new_list_colors)
        for u in range(number_of_samples):
            new_u = u / (number_of_samples - 1)
            new_v = v / (number_of_samples - 1)
            new_list_vertices.append([egg_calc_x(new_u, new_v), egg_calc_y(new_u), egg_calc_z(new_u, new_v)])
            new_list_colors.append([random.random(), random.random(), random.random()])

    # ostatnie przejście przez pętle jest nieco inne
    new_list_vertices = []
    vertices.append(new_list_vertices)
    new_list_colors = []
    colors.append(new_list_colors)
    for u in range(number_of_samples):
        new_u = u / (number_of_samples - 1)
        new_v = 1
        new_list_vertices.append([egg_calc_x(new_u, new_v), egg_calc_y(new_u), egg_calc_z(new_u, new_v)])
        new_list_colors.append(colors[0][number_of_samples - 1 - u])


def draw_points():
    glBegin(GL_POINTS)
    for i in range(number_of_samples):
        for j in range(number_of_samples):
            glVertex3fv(vertices[i][j])
    glEnd()


def draw_lines():
    glBegin(GL_LINES)
    for i in range(number_of_samples - 1):
        for j in range(number_of_samples - 1):
            glVertex3fv(vertices[i][j])
            glVertex3fv(vertices[i + 1][j])
            glVertex3fv(vertices[i][j])
            glVertex3fv(vertices[i][j + 1])
    glEnd()


def draw_triangles():
    glBegin(GL_TRIANGLES)
    for i in range(number_of_samples - 1):
        for j in range(number_of_samples - 1):
            glColor3fv(colors[i][j])
            glVertex3fv(vertices[i][j])

            glColor3fv(colors[i + 1][j])
            glVertex3fv(vertices[i + 1][j])

            glColor3fv(colors[i][j + 1])
            glVertex3fv(vertices[i][j + 1])

            glVertex3fv(vertices[i][j + 1])

            glColor3fv(colors[i + 1][j])
            glVertex3fv(vertices[i + 1][j])

            glColor3fv(colors[i + 1][j + 1])
            glVertex3fv(vertices[i + 1][j + 1])
    glEnd()


def draw_triangle_strip():
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(number_of_samples - 1):
        glColor3fv(colors[i][0])
        glVertex3fv(vertices[i][0])

        glColor3fv(colors[i + 1][0])
        glVertex3fv(vertices[i + 1][0])
        for j in range(1, number_of_samples):
            glColor3fv(colors[i][j])
            glVertex3fv(vertices[i][j])

            glColor3fv(colors[i + 1][j])
            glVertex3fv(vertices[i + 1][j])
    glEnd()


def torus_calc_x(u, v):
    return (big_r + small_r * math.cos(2 * math.pi * v)) * math.cos(2 * math.pi * u)


def torus_calc_y(u, v):
    return (big_r + small_r * math.cos(2 * math.pi * v)) * math.sin(2 * math.pi * u)


def torus_calc_z(v):
    return small_r * math.sin(2 * math.pi * v)


def torus_define_vertices_and_colors():
    # nie udało mi się wyeliminować artefaktów łączeń dla torusa
    for v in range(number_of_samples):
        new_list_vertices = []
        vertices.append(new_list_vertices)
        new_list_colors = []
        colors.append(new_list_colors)
        for u in range(number_of_samples):
            new_u = u / (number_of_samples - 1)
            new_v = v / (number_of_samples - 1)
            new_list_vertices.append([torus_calc_x(new_u, new_v), torus_calc_y(new_u, new_v), torus_calc_z(new_v)])
            new_list_colors.append([random.random(), random.random(), random.random()])


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time)
    glColor3f(1, 1, 1)

    # odkomentowana tylko jedna metoda rysowania
    # draw_points()
    # draw_lines()
    # draw_triangles()
    draw_triangle_strip()
    axes()

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-15, 15, -15 / aspect_ratio, 15 / aspect_ratio, 15, -15)
    else:
        glOrtho(-15 * aspect_ratio, 15 * aspect_ratio, -15, 15, 15, -15)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    # tylko jedna z poniższych funkcji powinna być odkomentowana

    egg_define_vertices_and_colors()
    # torus_define_vertices_and_colors()

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
