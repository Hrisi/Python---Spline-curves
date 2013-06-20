import SplinesC1
from SplinesC0 import InvalidData


class SplineC2:
    def __init__(self, degree, intervals):
        if (degree <= 2):
            raise InvalidData(SplinesC1.SplineC1.NONE_EXISTING_SPLINE_MESSAGE)

        self.splineC1 = SplinesC1.SplineC1(degree, intervals)
        self.deBoor_points = []

    def append_deBoor_point(self, point):
        if len(self.deBoor_points) == (
                2 * (-1 + self.splineC1.splineC0._degree) +
                len(self.splineC1.splineC0.intervals) - 1):
            raise IndexError

        self.deBoor_points.append(point)

    def _append_splineC1_point(self):
        degree = self.splineC1.splineC0._degree

        for index in range(0, degree - 1):
            self.splineC1.append_deBoor_point(
                self.deBoor_points[index])

        intervals = self.splineC1.splineC0.intervals
        intervals_count = len(intervals)

        for index in range(0, intervals_count):
            denominator = []
            numerator = []
            calculated_point = []

            if index == 0:
                previous_interval = 0
                next_interval = intervals[index + 1]
            elif index == intervals_count - 1:
                previous_interval = intervals[index - 1]
                next_interval = 0
            else:
                previous_interval, next_interval = (intervals[index - 1],
                                                    intervals[index + 1])

            denominator.append(previous_interval + intervals[index] +
                               next_interval)
            numerator.append(
                next_interval *
                self.deBoor_points[index + degree - 2] +
                intervals[index] *
                self.deBoor_points[index + degree - 1])

            calculated_point.append(numerator[0] * (1 / denominator[0]))
            self.splineC1.append_deBoor_point(calculated_point[0])

            if index > 0 and index < intervals_count - 1:
                print("if")
                numerator.append((intervals[index] +
                                  next_interval) *
                                 self.deBoor_points[index + degree - 1] +
                                 intervals[index] *
                                 self.deBoor_points[index + degree])

                calculated_point.append(numerator[1] * (1 / denominator[0]))
                self.splineC1.append_deBoor_point(calculated_point[1])

        for index in range(1, 3):
            self.splineC1.append_deBoor_point(self.deBoor_points[
                len(self.deBoor_points) - index])

    def draw_spline(self):
        if len(self.deBoor_points) < (
                2 * (-1 + self.splineC1.splineC0._degree) +
                len(self.splineC1.splineC0.intervals) - 1):
            raise InvalidData(
                self.splineC1.INCORRECT_COUNT_DEBOOR_POINTS_MESSAGE)

        self._append_splineC1_point()
        self.splineC1.draw_spline()
