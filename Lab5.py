#!/usr/bin/env python3
"""
opis klawiszy

klawisze 1-9 - ustawienie zmienianego parametru:
R(1), G(2), B(3) ambient
R(4), G(5), B(6) diffuse
R(7), G(8), B(9) specular

klawisze A i Z - zmiana wybranego parametru odpowiednio o 0.1 więcej lub mniej

klawisz N - toggle wektorów normalnych

"""
import sys
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 10.0]

number_of_samples = 15
vertices = []
normals = []

theta = 0.0
phi = 0.0
pix2radian = 1.0

key_pressed = 0
drawing_normals = True

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light0_ambient = [0.1, 0.1, 0.0, 1.0]
light0_diffuse = [0.8, 0.8, 0.0, 1.0]
light0_specular = [1.0, 1.0, 1.0, 1.0]
light0_position = [0.0, 0.0, 10.0, 1.0]

light1_ambient = [0.0, 0.0, 0.1, 1.0]
light1_diffuse = [0.0, 0.0, 0.8, 1.0]
light1_specular = [1.0, 1.0, 1.0, 1.0]
light1_position = [10.0, 0.0, 0.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light0_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light0_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light0_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light0_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, light1_position)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)


def egg_calc_x(u, v):
    return (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.cos(math.pi * v)


def egg_calc_y(u):
    return 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5  # -5 by mieć jajo niżej


def egg_calc_z(u, v):
    return (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.sin(math.pi * v)


def partial_x_u(u, v):
    return (-450 * u ** 4 + 900 * u ** 3 - 810 * u ** 2 + 360 * u - 45) * math.cos(math.pi * v)


def partial_x_v(u, v):
    return math.pi * (90 * u ** 5 - 225 * u ** 4 + 270 * u ** 3 - 180 * u ** 2 + 45 * u) * math.sin(math.pi * v)


def partial_y_u(u):
    return 640 * u ** 3 - 960 * u ** 2 + 320 * u


def partial_y_v():
    return 0


def partial_z_u(u, v):
    return (-450 * u ** 4 + 900 * u ** 3 - 810 * u ** 2 + 360 * u - 45) * math.sin(math.pi * v)


def partial_z_v(u, v):
    return -math.pi * (90 * u ** 5 - 225 * u ** 4 + 270 * u ** 3 - 180 * u ** 2 + 45 * u) * math.cos(math.pi * v)


def egg_calc_normal(u, v):
    x = partial_y_u(u) * partial_z_v(u, v) - partial_z_u(u, v) * partial_y_v()
    y = partial_z_u(u, v) * partial_x_v(u, v) - partial_x_u(u, v) * partial_z_v(u, v)
    z = partial_x_u(u, v) * partial_y_v() - partial_y_u(u) * partial_x_v(u, v)
    length = math.sqrt(x * x + y * y + z * z)
    if length != 0:
        x /= length
        y /= length
        z /= length
    elif u == 0 or u == 1:
        return [0, 1, 0]
    else:
        return [0, -1, 0]
    if u <= 0.5:
        x = -x
        y = -y
        z = -z
    return [x, y, z]


def egg_define_vertices_and_normals():
    for v in range(number_of_samples):
        new_list_vertices = []
        vertices.append(new_list_vertices)
        new_list_normals = []
        normals.append(new_list_normals)
        for u in range(number_of_samples):
            new_u = u / (number_of_samples - 1)
            new_v = v / (number_of_samples - 1)
            new_list_vertices.append([egg_calc_x(new_u, new_v), egg_calc_y(new_u), egg_calc_z(new_u, new_v)])
            new_list_normals.append(egg_calc_normal(new_u, new_v))


def egg_draw_triangle_strip():
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(number_of_samples - 1):
        glNormal3fv(normals[i][0])
        glVertex3fv(vertices[i][0])

        glNormal3fv(normals[i + 1][0])
        glVertex3fv(vertices[i + 1][0])
        for j in range(1, number_of_samples):
            glNormal3fv(normals[i][j])
            glVertex3fv(vertices[i][j])

            glNormal3fv(normals[i + 1][j])
            glVertex3fv(vertices[i + 1][j])
    glEnd()


def point_plus_vector(point, vector):
    new_x = point[0] - vector[0]
    new_y = point[1] - vector[1]
    new_z = point[2] - vector[2]
    return [new_x, new_y, new_z]


def draw_normals():
    glBegin(GL_LINES)
    for i in range(number_of_samples - 1):
        glVertex3fv(vertices[i][0])
        glVertex3fv(point_plus_vector(vertices[i][0], normals[i][0]))

        glVertex3fv(vertices[i + 1][0])
        glVertex3fv(point_plus_vector(vertices[i + 1][0], normals[i + 1][0]))
        for j in range(1, number_of_samples):
            glVertex3fv(vertices[i][j])
            glVertex3fv(point_plus_vector(vertices[i][j], normals[i][j]))

            glVertex3fv(vertices[i + 1][j])
            glVertex3fv(point_plus_vector(vertices[i + 1][j], normals[i + 1][j]))
    glEnd()


def shutdown():
    pass


def render(time):
    global theta
    global phi

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2radian
        phi += delta_y * pix2radian

    theta = theta % (2 * math.pi)
    phi = phi % (2 * math.pi)

    # print(f"phi={phi}, theta={theta}\n")

    r = 5
    light0_position[0] = r * math.cos(theta) * math.cos(phi)
    light0_position[1] = r * math.sin(phi)
    light0_position[2] = r * math.sin(theta) * math.cos(phi)
    light1_position[0] = -r * math.cos(theta) * math.cos(phi)
    light1_position[1] = -r * math.sin(phi)
    light1_position[2] = -r * math.sin(theta) * math.cos(phi)
    glLightfv(GL_LIGHT0, GL_POSITION, light0_position)
    glLightfv(GL_LIGHT1, GL_POSITION, light1_position)

    glTranslate(-light0_position[0], -light0_position[1], -light0_position[2])
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)
    glTranslate(light0_position[0], light0_position[1], light0_position[2])

    glTranslate(-light1_position[0], -light1_position[1], -light1_position[2])
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)
    glTranslate(light1_position[0], light1_position[1], light1_position[2])

    glRotatef(math.degrees(theta), 0.0, 1.0, 0.0)
    glRotatef(math.degrees(phi), 1.0, 0.0, 0.0)

    egg_draw_triangle_strip()

    if drawing_normals:
        draw_normals()

    glFlush()


def update_viewport(window, width, height):
    global pix2radian
    pix2radian = 2 * math.pi / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def set_value_between_0_and_1(value):
    if value > 1:
        return 1
    elif value < 0:
        return 0
    else:
        return value


def change_color(delta):
    if key_pressed == 1:
        light0_ambient[0] += delta
        light0_ambient[0] = set_value_between_0_and_1(light0_ambient[0])
    elif key_pressed == 2:
        light0_ambient[1] += delta
        light0_ambient[1] = set_value_between_0_and_1(light0_ambient[1])
    elif key_pressed == 3:
        light0_ambient[2] += delta
        light0_ambient[2] = set_value_between_0_and_1(light0_ambient[2])
    elif key_pressed == 4:
        light0_diffuse[0] += delta
        light0_diffuse[0] = set_value_between_0_and_1(light0_diffuse[0])
    elif key_pressed == 5:
        light0_diffuse[1] += delta
        light0_diffuse[1] = set_value_between_0_and_1(light0_diffuse[1])
    elif key_pressed == 6:
        light0_diffuse[2] += delta
        light0_diffuse[2] = set_value_between_0_and_1(light0_diffuse[2])
    elif key_pressed == 7:
        light0_specular[0] += delta
        light0_specular[0] = set_value_between_0_and_1(light0_specular[0])
    elif key_pressed == 8:
        light0_specular[1] += delta
        light0_specular[1] = set_value_between_0_and_1(light0_specular[1])
    elif key_pressed == 9:
        light0_specular[2] += delta
        light0_specular[2] = set_value_between_0_and_1(light0_specular[2])

    glLightfv(GL_LIGHT0, GL_AMBIENT, light0_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light0_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light0_specular)

    print(f"Ambient: {light0_ambient}\nDiffuse: {light0_diffuse}\nSpecular: {light0_specular}\n")


def keyboard_key_callback(window, key, scancode, action, mods):
    global key_pressed
    global drawing_normals
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    elif key == GLFW_KEY_1 and action == GLFW_PRESS:
        key_pressed = 1
    elif key == GLFW_KEY_2 and action == GLFW_PRESS:
        key_pressed = 2
    elif key == GLFW_KEY_3 and action == GLFW_PRESS:
        key_pressed = 3
    elif key == GLFW_KEY_4 and action == GLFW_PRESS:
        key_pressed = 4
    elif key == GLFW_KEY_5 and action == GLFW_PRESS:
        key_pressed = 5
    elif key == GLFW_KEY_6 and action == GLFW_PRESS:
        key_pressed = 6
    elif key == GLFW_KEY_7 and action == GLFW_PRESS:
        key_pressed = 7
    elif key == GLFW_KEY_8 and action == GLFW_PRESS:
        key_pressed = 8
    elif key == GLFW_KEY_9 and action == GLFW_PRESS:
        key_pressed = 9
    elif key == GLFW_KEY_A and action == GLFW_PRESS:
        change_color(0.1)
    elif key == GLFW_KEY_Z and action == GLFW_PRESS:
        change_color(-0.1)
    elif key == GLFW_KEY_N and action == GLFW_PRESS:
        drawing_normals = not drawing_normals


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

    egg_define_vertices_and_normals()

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
