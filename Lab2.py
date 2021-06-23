#!/usr/bin/env python3

# program domyślnie uruchamia dywan sierpińskiego (algorytm iteracyjny)

# aby program rysował śnieżynkę kocha, należy w funkcji render zmienić draw_sierpinski_carpet na draw_koch_snowflake

# aby uruchomić rysowanie prostokąta z losowymi kolorami, należy zakomentować w mainie render,
# a odkomentować render random oraz przypisanie colors

import math
import random
import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0, 0, 0, 1.0)


def shutdown():
    pass


def draw_rectangle(x, y, a, b, d=0.0):
    """x, y - lewy dolny wierzchołek prostokąta
    a - szerokość
    b - wysokość"""

    # d == True <=> d != 0
    if d:
        a, b = a * d, b * d

    glBegin(GL_TRIANGLES)
    # trójkąt 1 - lewy dolny, lewy górny, prawy górny
    glVertex2f(x, y)
    glVertex2f(x, y + b)
    glVertex2f(x + a, y + b)
    # trójkąt 2 - lewy dolny, prawy górny, prawy dolny
    glVertex2f(x, y)
    glVertex2f(x + a, y + b)
    glVertex2f(x + a, y)
    glEnd()


def draw_rectangle_list(li):
    draw_rectangle(li[0], li[1], li[2], li[3])


def generate_random_colors() -> list:
    colors = []
    for i in range(4):
        colors.append((random.random(), random.random(), random.random()))
    return colors


def draw_random_rectangle(x, y, a, b, colors: list, d=0.0):
    """x, y - lewy dolny wierzchołek prostokąta
    a - szerokość
    b - wysokość
    colors - lista 4 krotek, każda krotka zawiera 3 floaty w przedziale [0, 1]"""

    # d == True <=> d != 0
    if d:
        a, b = a * d, b * d

    glBegin(GL_TRIANGLES)
    # trójkąt 1 - lewy dolny, lewy górny, prawy górny
    glColor3fv(colors[0])
    glVertex2f(x, y)
    glColor3fv(colors[1])
    glVertex2f(x, y + b)
    glColor3fv(colors[2])
    glVertex2f(x + a, y + b)
    # trójkąt 2 - lewy dolny, prawy górny, prawy dolny
    glColor3fv(colors[0])
    glVertex2f(x, y)
    glColor3fv(colors[2])
    glVertex2f(x + a, y + b)
    glColor3fv(colors[3])
    glVertex2f(x + a, y)
    glEnd()


def draw_sierpinski_carpet(x, y, a, b, level: int):
    glColor3f(1, 1, 1)
    rectangles = [(x, y, a, b)]
    draw_rectangle(x, y, a, b)
    glColor3f(0, 0, 0)
    for i in range(level):
        new_rectangles = []
        for rect in rectangles:
            x = rect[0]
            y = rect[1]
            a = rect[2] / 3
            b = rect[3] / 3
            # dzielimy prostokąt na 9 części
            # "wytnij" środkowy prostokąt
            draw_rectangle(x + a, y + b, a, b)
            # pozostałe 8 prostokątów dodajemy do listy
            new_rectangles.append((x, y, a, b))
            new_rectangles.append((x + a, y, a, b))
            new_rectangles.append((x + 2 * a, y, a, b))
            new_rectangles.append((x, y + b, a, b))
            new_rectangles.append((x + 2 * a, y + b, a, b))
            new_rectangles.append((x, y + 2 * b, a, b))
            new_rectangles.append((x + a, y + 2 * b, a, b))
            new_rectangles.append((x + 2 * a, y + 2 * b, a, b))
        rectangles = new_rectangles


def draw_koch_snowflake(x, y, a, level: int):
    """x, y - lewy dolny wierzchołek początkowego trójkąta
    a - długość boku początkowego trójkąta"""
    glColor3f(1, 1, 1)
    sqrt3 = math.sqrt(3)
    points = [(x, y), (x + a / 2, y + a * sqrt3 / 2), (x + a, y), (x, y)]
    for lev in range(level):
        i = 0
        while i < len(points) - 1:
            point1 = points[i]
            if i == len(points) - 2:
                point2 = points[0]
            else:
                point2 = points[i + 1]

            midpoint = ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)
            point_to_add1 = (point1[0] * 2 / 3 + point2[0] * 1 / 3, point1[1] * 2 / 3 + point2[1] * 1 / 3)
            point_to_add3 = (point1[0] * 1 / 3 + point2[0] * 2 / 3, point1[1] * 1 / 3 + point2[1] * 2 / 3)

            vx = point_to_add3[0] - point_to_add1[0]
            vy = point_to_add3[1] - point_to_add1[1]
            # vx, vy = vx * cos60 - vy * sin60, vx * sin60 + vy * cos60
            vx, vy = -vy, vx
            # point_to_add2 = (point_to_add1[0] + vx, point_to_add1[1] + vy)
            point_to_add2 = (midpoint[0] + vx, midpoint[1] + vy)
            points.insert(i + 1, point_to_add1)
            points.insert(i + 2, point_to_add2)
            points.insert(i + 3, point_to_add3)
            i += 4

    glBegin(GL_LINE_LOOP)
    for point in points:
        glVertex2fv(point)
    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    # draw_sierpinski_carpet(-75, -90, 150, 180, 5)
    draw_koch_snowflake(-50, -50, 100, 4)
    glFlush()


def render_random_rectangle(colors, time):
    glClear(GL_COLOR_BUFFER_BIT)
    draw_random_rectangle(-25, -25, 50, 50, colors, 0)
    glFlush()


def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

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

    # do rysowania prostokąta z losowymi kolorami
    # colors = generate_random_colors()

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        # rysowanie prostokąta z losowymi kolorami (zakomentować render, odkomentować render random i wcześniej colors)
        # render_random_rectangle(colors, glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
