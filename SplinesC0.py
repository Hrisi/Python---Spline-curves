import Bezier_curves


class InvalidData(Exception):
    pass


class SplineC0:
    NEGATIVE_DATA_MESSAGE = "Please insert positive numbers!"
    NOT_INT_DATA_MESSAGE = "Please insert integers!"
    NOT_LOGIC_CORRECT_MESSAGE = "Degree should be less than Points Count!"

    def __init__(self, degree, points_count):
        if degree < 0 or points_count < 0:
            raise InvalidData(self.NEGATIVE_DATA_MESSAGE)

        if not isinstance(degree, int) or not isinstance(points_count, int):
            raise InvalidData(self.NOT_INT_DATA_MESSAGE)

        if (degree >= points_count):
            raise InvalidData(self.NOT_LOGIC_CORRECT_MESSAGE)

        self._degree = degree
        self.points_count = points_count
        self.control_points = []
        self.partial_curves = []

        for count in range(0, self.points_count // self._degree):
            self.partial_curves.append(Bezier_curves.BezierCurve())

    def append_point(self, point):
        if len(self.control_points) == self.points_count:
            raise IndexError

        self.control_points.append(point)

        partial_curve_count = (len(self.control_points) - 1) // self._degree
        condition = (self.points_count == len(self.control_points))

        if ((len(self.control_points) - 1) % self._degree == 0 and
                (not condition) and len(self.control_points) > 1):
            print(partial_curve_count, condition, len(self.control_points))
            self.partial_curves[partial_curve_count - 1].append_point(point)

        self.partial_curves[partial_curve_count -
                            condition].append_point(point)

    def draw_spline(self):
        for curve in self.partial_curves:
            curve.draw_curve()
