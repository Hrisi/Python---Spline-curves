import unittest
import Vec3D
from Bezier_curves import *


class BezierCurvesTest(unittest.TestCase):
    PARAMETERS = (0, 0.5, 1)

    def setUp(self):
        self.curve = BezierCurve()

    def tearDown(self):
        self.curve = None

    def test_append_point(self):
        points = [Vec3D.Vec3D(1, 2, -1),
                  Vec3D.Vec3D(2, 3, 4),
                  Vec3D.Vec3D(-3, 4, 8),
                  Vec3D.Vec3D(10, 10, 8)]

        for i in range(0, 4):
            self.curve.append_point(points[i])
            self.assertEqual(self.curve.control_points[i], points[i])

    def test_deCasteljau_algorithm(self):
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(1, 1, 1)]
        result_points = [Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0.25, 0.75, 0.75),
                         Vec3D.Vec3D(1, 1, 1)]

        for i in range(0, 3):
            self.curve.append_point(points[i])

        for i in range(0, 3):
            algorithm_result = self.curve.deCasteljau_algorithm(
                self.PARAMETERS[i],
                self.curve.control_points)
            self.assertEqual(algorithm_result, result_points[i])

    def test_curve_interpolation(self):
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(1, 1, 1)]

        for i in range(0, 3):
            self.curve.append_point(points[i])

        self.curve._curve_calculation(self.curve.control_points)

        self.assertEqual(self.curve.curve[0], Vec3D.Vec3D(0, 0, 0))
        self.assertEqual(self.curve.curve[self.curve.RANGE_STEP],
                         Vec3D.Vec3D(1, 1, 1))

    def test_linear_curves(self):
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 2)]

        for i in range(0, 3):
            self.curve.append_point(points[i])

        curve_points = self.curve.draw_curve()

        self.assertEqual(self.curve.curve[int(self.curve.RANGE_STEP / 2)],
                         points[1])

    def test_finite_difference(self):
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(2, 8, 6),
                  Vec3D.Vec3D(3, 5, 4),
                  Vec3D.Vec3D(4, 4, 5)]

        for i in range(0, 4):
            self.curve.append_point(points[i])

        derivative = []
        derivative = self.curve.finite_difference(2)
        self.assertEqual(derivative[0], Vec3D.Vec3D(-1, -11, -8))
        self.assertEqual(derivative[1], Vec3D.Vec3D(0, 2, 3))

        derivative = self.curve.finite_difference(3)
        self.assertEqual(derivative[0], Vec3D.Vec3D(1, 13, 11))

    def test_curve_derivative(self):
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(2, 8, 6),
                  Vec3D.Vec3D(3, 5, 4),
                  Vec3D.Vec3D(4, 4, 5)]

        for i in range(0, 4):
            self.curve.append_point(points[i])

        self.curve._derivative_calculation(2)

        self.assertEqual(self.curve.derivative[2][0],
                         Vec3D.Vec3D(-1, -11, -8))
        self.assertEqual(self.curve.derivative[2][self.curve.RANGE_STEP],
                         Vec3D.Vec3D(0, 2, 3))

    def test_subdivision(self):
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 3)]

        result_points = {'left': [Vec3D.Vec3D(0, 0, 0),
                                  Vec3D.Vec3D(0, 0, 0),
                                  Vec3D.Vec3D(0, 0, 0)],
                         'right': [Vec3D.Vec3D(0, 0, 0),
                                   Vec3D.Vec3D(0, 1, 1),
                                   Vec3D.Vec3D(0, 2, 3)]}

        for i in range(0, 3):
            self.curve.append_point(points[i])

        curve_points = self.curve.draw_curve()

        for i in range(0, 3):
            self.assertEqual(self.curve.subdivision_left[0][i],
                             result_points['left'][i])
            self.assertEqual(self.curve.subdivision_right[0][i],
                             result_points['right'][i])

    def test_degree_elevation(self):
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 3)]

        for i in range(0, 3):
            self.curve.append_point(points[i])

        elevation = self.curve.degree_elevation()

        self.assertEqual(elevation[1], Vec3D.Vec3D(0, 2 / 3, 2 / 3))

if __name__ == '__main__':
    unittest.main()
