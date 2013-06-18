import Bezier_curves


class InvalidData(Exception):
    pass


class SplineC0:
    NEGATIVE_DATA_MESSAGE = "Please insert a positive degree!"
    NOT_INT_DATA_MESSAGE = "Please insert integers!"
    NONE_INTERVALS_MESSAGE = "Please insert intervals!"
    INCORRECT_COUNT_CONTROL_POINTS = "Please insert more control points!"
    INCORRECT_INTERVAL_DIVISION = "Incorrect intervals inserted. Try again!"

    def __init__(self, degree, intervals):
        if degree < 0:
            raise InvalidData(self.NEGATIVE_DATA_MESSAGE)

        if not isinstance(degree, int):
            raise InvalidData(self.NOT_INT_DATA_MESSAGE)

        if not intervals:
            raise InvalidData(self.NONE_INTERVALS_MESSAGE)

        if len(intervals) > 1:
            for count in range(1, len(intervals)):
                if intervals[count - 1][1] != intervals[count][0]:
                    raise InvalidData(self.INCORRECT_INTERVAL_DIVISION)

        self._degree = degree
        self.points_count = len(intervals) * degree + 1
        self.control_points = []
        self.partial_curves = []
        self.intervals = []

        for count in range(0, len(intervals)):
            self.intervals.append(intervals[count][1] - intervals[count][0])

        for count in range(0, len(intervals)):
            self.partial_curves.append(Bezier_curves.BezierCurve())

    def append_point(self, point):
        if len(self.control_points) == self.points_count:
            raise IndexError

        self.control_points.append(point)

        partial_curves_count = (len(self.control_points) - 1) // self._degree
        condition = (self.points_count == len(self.control_points))

        if ((len(self.control_points) - 1) % self._degree == 0 and
                (not condition) and len(self.control_points) > 1):
            self.partial_curves[partial_curves_count - 1].append_point(point)

        self.partial_curves[partial_curves_count -
                            condition].append_point(point)

    def draw_spline(self):
        if len(self.control_points) < self.points_count:
            raise InvalidData(self.INCORRECT_COUNT_CONTROL_POINTS)

        draw = []
        for curve in self.partial_curves:
            draw.append(curve.draw_curve())

        return draw
