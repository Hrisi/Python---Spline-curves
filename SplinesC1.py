import SplinesC0


class SplineC1:
    def __init__(self, degree, points_count, interval):
        self.spline = SplineC0(degree, points_count)
        self.deBoor_points = []
        self.counter = 0

    def append_point(self, point):
        len_points = len(self.spline.control_points)
        if len_points % self.spline._degree == 0:
            self.counter += 1
            denominator = (self.spline.interval[count - 1] +
                           self.spline.interval[count])
            numerator = (self.spline.interval[count] *
                         self.spline.control_points[len_points - 1] +
                         self.spline.interval[count] *
                         self.spline.control_points[count - 1])

            calculated_point = numerator / denominator

            self.spline.append_point(calculated_point)

        self.spline.append_point(point)
        self.deBoor_points.append(point)
