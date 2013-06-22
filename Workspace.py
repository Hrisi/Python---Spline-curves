from PyQt4 import QtCore, QtGui, QtOpenGL

from OpenGL.GL import *
from OpenGL.GLU import *


class Workspace(QtOpenGL.QGLWidget):
    OBJECT_BEZIER_CURVES = "Bezier curves"
    OBJECT_SPLINESC0 = "Splines C0"
    OBJECT_SPLINESC1 = "Splines C1"
    OBJECT_SPLINESC2 = "Splines C2"
    AXIS_LENGTH = 10

    def __init__(self):
        super(Workspace, self).__init__()
        self.objects = {self.OBJECT_BEZIER_CURVES: [],
                        self.OBJECT_SPLINESC0: [],
                        self.OBJECT_SPLINESC1: [],
                        self.OBJECT_SPLINESC2: []}

    def add_splineC0_object(self, object_):
        self.objects[self.OBJECT_SPLINESC0].append(object_)

    def add_splineC1_object(self, object_):
        self.objects[self.OBJECT_SPLINESC1].append(object_)

    def add_splineC2_object(self, object_):
        self.objects[self.OBJECT_SPLINESC2].append(object_)

    def add_Bezier_curve_object(self, object_):
        self.objects[self.OBJECT_BEZIER_CURVES].append(object_)

    def reset(self):
        print(self)

    def initializeGL(self):
        glShadeModel(GL_SMOOTH)

        glClearColor(0.0, 0.0, 0.0, 0.0)
        glEnable(GL_DEPTH_TEST)

        glEnable(GL_POINT_SMOOTH)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glFlush()

    def resizeGL(self, width, height):
        print(width, height)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90.0, width / height, 0.1, 100000)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glFlush()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # position the camera to the correct place
        glTranslatef(0, 0, -5)

        # Enable antializing
        glEnable(GL_LINE_SMOOTH)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glFlush()

        # Color in RGB
        glRotatef(30, 1, 0, 0)
        glRotatef(-40, 0, 1, 0)
        glLineWidth(2)
        glShadeModel(GL_SMOOTH)

        self.draw_Bezier_curve()
        self.draw_splineC0()
        self.draw_splineC1()
        self.draw_splineC2()

        self.draw_derivative()
        self.draw_control_polygon()

        self.draw_coordinate_system()

    def draw_coordinate_axis(self, x, y, z, red, green, blue):
        glColor3f(red, green, blue)
        glLineWidth(3)

        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(x, y, z)
        glEnd()

    def draw_coordinate_system(self):
        self.draw_coordinate_axis(self.AXIS_LENGTH, 0, 0, 1.0, 0.0, 0.0)
        self.draw_coordinate_axis(0, self.AXIS_LENGTH, 0, 0.0, 1.0, 0.0)
        self.draw_coordinate_axis(0, 0, self.AXIS_LENGTH, 0.0, 0.0, 1.0)

    def change_curve_visibility(self, object_):
        object_.to_be_drawn = not object_.to_be_drawn

    def change_control_polygon_visibility(self, object_):
        object_.control_polygon_to_be_drawn = (
            not object_.control_polygon_to_be_drawn)

    def change_curve_derivative_visibility(self, object_, degree):
        object_.derivatives_to_be_drawn.add(degree)

    def drawGL(self, points, modeGL):
        glBegin(modeGL)
        for point in points:
            glVertex3f(point.x, point.y, point.z)
        glEnd()

    def object_to_be_drawn(self, object_key):
        for object_ in self.objects[object_key]:
            return object_.to_be_drawn and object_

    def draw_object(self, object_key, modeGL=GL_POINTS):
        object_ = self.object_to_be_drawn(object_key)
        if object_:
            print("draw!")
            self.drawGL(object_.draw(), modeGL)

    def draw_control_polygon(self):
        glColor3f(0.3, 0.3, 0.1)
        for object_ in self.objects[self.OBJECT_BEZIER_CURVES]:
            self.drawGL(object_.control_points, GL_LINE_STRIP)

    def draw_derivative(self):
        glColor3f(1.0, 0.5, 0.5)
        #derivative_to_be_drawn is a number of the derivative to be drawn
        for object_ in self.objects[self.OBJECT_BEZIER_CURVES]:
            for value in object_.derivatives_to_be_drawn:
                self.drawGL(object_.draw_derivative(value), GL_POINTS)

    def draw_Bezier_curve(self):
        glColor3f(1.0, 1.0, 0)

        self.draw_object(self.OBJECT_BEZIER_CURVES)

    def draw_splineC0(self):
        self.draw_object(self.OBJECT_SPLINESC0)

    def draw_splineC1(self):
        self.draw_object(self.OBJECT_SPLINESC1)

    def draw_splineC2(self):
        self.draw_object(self.OBJECT_SPLINESC2)
