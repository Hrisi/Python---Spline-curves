from PyQt4 import QtCore, QtGui, QtOpenGL

from OpenGL.GL import *
from OpenGL.GLU import *

import Vec3D


class Workspace(QtOpenGL.QGLWidget):
    OBJECT_BEZIER_CURVES = "Bezier curves"
    OBJECT_SPLINESC0 = "Splines C0"
    OBJECT_SPLINESC1 = "Splines C1"
    OBJECT_SPLINESC2 = "Splines C2"
    AXIS_LENGTH = 5
    MIN_ZOOM = 1
    MAX_ZOOM = 39
    ZOOM_STEP = 2
    BASIC_ZOOM = -5

    def __init__(self):
        super(Workspace, self).__init__()
        self.objects = {self.OBJECT_BEZIER_CURVES: list(),
                        self.OBJECT_SPLINESC0: list(),
                        self.OBJECT_SPLINESC1: list(),
                        self.OBJECT_SPLINESC2: list()}
        print(self.objects)
        self.zoom = 1
        self.angle_x, self.angle_y = 30, -40
        self.current_x, self.current_y = 0, 0
        self.pressed_button = None

        self.min_z = 0
        self.min_distance = -1
        self.point_to_be_moved_index = None
        self.clicked_object = None
        print('init')

    def add_splineC0_object(self, object_):
        self.objects[self.OBJECT_SPLINESC0].append(object_)

    def add_splineC1_object(self, object_):
        self.objects[self.OBJECT_SPLINESC1].append(object_)

    def add_splineC2_object(self, object_):
        self.objects[self.OBJECT_SPLINESC2].append(object_)

    def add_Bezier_curve_object(self, object_):
        self.objects[self.OBJECT_BEZIER_CURVES].append(object_)

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

    def set_view_point(self):
        glTranslatef(0, 0, self.BASIC_ZOOM * self.zoom)
        glRotatef(self.angle_x, 1, 0, 0)
        glRotatef(self.angle_y, 0, 1, 0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # position the camera to the correct place

        # Enable antializing
        glEnable(GL_LINE_SMOOTH)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glFlush()
        # Color in RGB
        self.set_view_point()
        glLineWidth(2)

        self.draw_Bezier_curve()
        self.draw_splineC0()
        self.draw_splineC1()
        self.draw_splineC2()

        self.draw_derivative()
        self.draw_control_polygon()
        self.draw_Bezier_control_polygon()
        self.draw_deBoor_control_polygon()

        self.draw_coordinate_system()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.current_x, self.current_y = event.x(), event.y()
            event.accept()
        elif event.button() == QtCore.Qt.RightButton:
            self.find_clicked_point(event.x(), event.y())
        else:
            self.current_x, self.current_y = -1, -1

        self.pressed_button = event.button()

    def mouseMoveEvent(self, event):
        if self.current_x >= 0 and self.current_y >= 0:
            new_x, new_y = event.x(), event.y()
            if self.pressed_button == QtCore.Qt.LeftButton:
                self.angle_x += (new_y - self.current_y) / 2
                self.angle_y += (new_x - self.current_x) / 2
                self.current_x, self.current_y = new_x, new_y
            if self.pressed_button == QtCore.Qt.RightButton:
                model, projection, view = None, None, None
                self.set_view_point(model, projection, view)
                new_y = view[3] - new_y

                point = gluUnProject(new_x, new_y, self.min_z,
                                     model, projection, view)
                self.clicked_object.replace_point(
                    self.point_to_be_moved_index,
                    Vec3D.Vec3D(point[0], point[1], points[2]))

        event.accept()
        self.updateGL()

    def reset(self):
        print(self)

    def zoom_in(self):
        if self.zoom > self.MIN_ZOOM:
            self.zoom -= self.ZOOM_STEP

        print(self.zoom)

        self.updateGL()

    def zoom_out(self):
        if self.zoom < self.MAX_ZOOM:
            self.zoom += self.ZOOM_STEP

        self.updateGL()

    def draw_coordinate_axis(self, x, y, z, red, green, blue):
        glColor3f(red, green, blue)
        glLineWidth(5)

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

    def change_Bezier_control_polygon_visibility(self, object_):
        object_.control_polygon_Bezier_to_be_drawn = (
            not object_.control_polygon_Bezier_to_be_drawn)

    def change_deBoor_control_polygon_visibility(self, object_):
        object_.control_polygon_deBoor_to_be_drawn = (
            not object_.control_polygon_deBoor_to_be_drawn)

    def change_curve_derivative_visibility(self, object_, degree):
        object_.derivatives_to_be_drawn.add(degree)

    def drawGL(self, points, modeGL):
        glBegin(modeGL)
        for point in points:
            #print(point.x, point.y, point.z, 'point')
            glVertex3f(point.x, point.y, point.z)
        glEnd()

    def object_to_be_drawn(self, object_key):
        for object_ in self.objects[object_key]:
            if object_.to_be_drawn:
                return object_

    def draw_object(self, object_key, modeGL=GL_POINTS):
        glPointSize(2)
        object_ = self.object_to_be_drawn(object_key)
        print(object_, 'obj')
        if object_:
            print('here!')
            self.drawGL(object_.draw(), modeGL)

    def drawGL_control_polygon(self, object_, red, green, blue, deBoor=None):
        if not deBoor:
            control_points = object_.control_points
        else:
            control_points = object_.deBoor_points

        self.drawGL(control_points, GL_LINE_STRIP)
        glPointSize(8)
        glColor3f(red, green, blue)
        self.drawGL(control_points, GL_POINTS)

    def draw_control_polygon(self):
        glColor3f(0.3, 0.3, 0.1)

        for key in (self.OBJECT_BEZIER_CURVES, self.OBJECT_SPLINESC0):
            for object_ in self.objects[key]:
                if object_.control_polygon_to_be_drawn:
                    self.drawGL_control_polygon(object_, 0.3, 0.3, 0.1)

    def draw_Bezier_control_polygon(self):
        glColor3f(0.3, 0.3, 0.6)

        for key in (self.OBJECT_SPLINESC1, self.OBJECT_SPLINESC2):
            for object_ in self.objects[key]:
                if object_.control_polygon_Bezier_to_be_drawn:
                    self.drawGL_control_polygon(object_, 0.3, 0.3, 0.6)

    def draw_deBoor_control_polygon(self):
        glColor3f(1.0, 0.3, 0.6)

        for key in (self.OBJECT_SPLINESC1, self.OBJECT_SPLINESC2):
            for object_ in self.objects[key]:
                if object_.control_polygon_deBoor_to_be_drawn:
                    print('deBoor')
                    self.drawGL_control_polygon(object_, 1.0, 0.3, 0.6, True)

    def draw_derivative(self):
        glColor3f(1.0, 0.5, 0.5)
        #derivative_to_be_drawn is a number of the derivative to be drawn
        for object_ in self.objects[self.OBJECT_BEZIER_CURVES]:
            for value in object_.derivatives_to_be_drawn:
                print('der')
                self.drawGL(object_.draw_derivative(value), GL_POINTS)

    def draw_Bezier_curve(self):
        glColor3f(1.0, 0.7, 0.5)

        self.draw_object(self.OBJECT_BEZIER_CURVES)

    def draw_splineC0(self):
        glColor3f(0.7, 0.2, 1.0)

        self.draw_object(self.OBJECT_SPLINESC0)

    def draw_splineC1(self):
        glColor3f(0.7, 1.0, 0.5)

        self.draw_object(self.OBJECT_SPLINESC1)

    def draw_splineC2(self):
        glColor3f(0.7, 0.5, 1.0)

        self.draw_object(self.OBJECT_SPLINESC2)

    def getDistance(self, control_point, model, projection, view):
        projected_value = gluProjection(control_point, model, projection, view)
        distance = ((projected_value[0] - x) * (projected_value[0] - x) +
                    (projected_value[1] - y) * (projected_value[1] - y))

        return distance, projected_value[2]

    def find_clicked_point(self, x, y):
        """ The function finds the point clicked by comparing the minimal
            distance from the place where we click to the control points.
            Modifies screen coordinates to coordinates in 3D."""

        control_points = []
        objects = []
        for key, value in self.objects.items():
            for object_ in value:
                objects.append(object_)
                if key in (self.OBJECT_BEZIER_CURVES, self.OBJECT_SPLINESC0):
                    object_control_points = object_.control_points
                else:
                    object_control_points = object_.deBoor_points

                if object_.control_polygon_to_be_drawn:
                    control_points += object_control_points

        objects_control_points = zip(objects, control_points)

        self.set_view_point()

        model = glGetDoublev(GL_MODELVIEW)
        projection = glGetDoublev(GL_PROJECTION)
        view = glGetIntegerv(GL_VIEWPORT)

        y = view[3] - y
        distance_result = self.getDistance(control_points[0], model,
                                           projection, view, x, y)
        self.min_distance = distance_result[0]
        self.min_z = distance_result[1]
        self.point_to_be_moved_index = 0
        self.clicked_object = objects[0]
        count = 0

        for object_, point in object_control_points:
            distance = self.getDistance(points, model, projection, view, x, y)
            if (distance[0] < min_distance or
                    (distance[0] == self.min_distance and
                     distance[1] < self.min_z)):
                self.min_distance = distance[0]
                self.min_z = distance[1]
                self.point_to_be_moved_index = count
                self.clicked_object = object_

            count += 1
