from PyQt4 import QtCore, QtGui, QtOpenGL

from OpenGL.GL import *
from OpenGL.GLU import *


class Workspace(QtOpenGL.QGLWidget):
    OBJECT_BEZIER_CURVES = "Bezier curves"
    OBJECT_SPLINESC0 = "Splines C0"
    OBJECT_SPLINESC1 = "Splines C1"
    OBJECT_SPLINESC2 = "Splines C2"

    def __init__(self):
        super(Workspace, self).__init__()
        self.objects = {self.OBJECT_BEZIER_CURVES: [],
                        self.OBJECT_SPLINESC0: [],
                        self.OBJECT_SPLINESC1: [],
                        self.OBJECT_SPLINESC2: []}

    def add_splineC0_object(self, object):
        self.objects[self.OBJECT_SPLINESC0].append(object)

    def add_splineC1_object(self, object):
        self.objects[self.OBJECT_SPLINESC1].append(object)

    def add_splineC2_object(self, object):
        self.objects[self.OBJECT_SPLINESC2].append(object)

    def add_Bezier_curve_object(self, object):
        self.objects[self.OBJECT_BEZIER_CURVES].append(object)

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
        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(2)

        self.draw_Bezier_curve()
        self.draw_splineC0()
        self.draw_splineC1()
        self.draw_splineC2()

    def drawGL(self, points, modeGL):
        glBegin(mode)
        for point in points:
            glVertex3f(point)  # point is Vec3D -> to return a tuple?
        glEnd()

    def object_to_be_drawn(self, object_key):
        for object in self.objects[object_key]:
            return object.to_be_drawn and object

    def draw_object(self, object_key, modeGL=GL_LINE_STRIP):
        object = self.object_to_be_drawn(object_key)
        if object:
            self.drawGL(object.draw(), modeGL)

    def draw_derivative(self):
        #derivative_to_be_drawn is a number of the derivative to be drawn
        for object in self.objects[self.OBJECTS_BEZIER_CURVES]:
            if object.derivative_to_be_drawn:
                self.drawGL(object.draw_derivative(derivative_to_be_drawn),
                            GL_LINE_STRIP)

    def draw_Bezier_curve(self):
        self.draw_object(self.OBJECT_BEZIER_CURVES)

    def draw_splineC0(self):
        self.draw_object(self.OBJECT_SPLINESC0)

    def draw_splineC1(self):
        self.draw_object(self.OBJECT_SPLINESC1)

    def draw_splineC2(self):
        self.draw_object(self.OBJECT_SPLINESC2)
