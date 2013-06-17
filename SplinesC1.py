import SplinesC0


class SplineC1:
    NONE_EXISTING_SPLINE = "Please increase the degree!"

    def __init__(self, degree, interval):

        if (degree <= 1):
            raise IndexError(self.NONE_EXISTING_SPLINE)

        self.spline = SplinesC0.SplineC0(degree, interval)
        self.deBoor_points = []
        self.counter = 0

    def append_point(self, point):
        if len(self.deBoor_points) == 2 * len(self.spline._degree):
            raise IndexError

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

    def draw_spline(self):
        self.spline.draw()
