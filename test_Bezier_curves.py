import unittest
import Vec3D
from Bezier_curves import *


class BezierCurvesTest(unittest.TestCase):
    PARAMETERS = (0, 0.5, 1)

    def test_append_point(self):
        points = [Vec3D.Vec3D(1, 2, -1),
                  Vec3D.Vec3D(2, 3, 4),
                  Vec3D.Vec3D(-3, 4, 8),
                  Vec3D.Vec3D(10, 10, 8)]

        curve = BezierCurves()

        for i in range(0, 4):
            curve.append_point(points[i])
            self.assertEqual(curve.control_points[i], points[i])

    def test_deCasteljau_algorithm(self):
        curve = BezierCurves()
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(1, 1, 1)]
        result_points = [Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0.25, 0.75, 0.75),
                         Vec3D.Vec3D(1, 1, 1)]

        for i in range(0, 3):
            curve.append_point(points[i])

        for i in range(0, 3):
            self.assertEqual(curve.deCasteljau_algorithm(self.PARAMETERS[i],
                             curve.control_points), result_points[i])

    def test_curve_interpolation(self):
        curve = BezierCurves()
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(1, 1, 1)]

        for i in range(0, 3):
            curve.append_point(points[i])

        curve._curve_calculation(curve.control_points)

        self.assertEqual(curve.curve[0], Vec3D.Vec3D(0, 0, 0))
        self.assertEqual(curve.curve[curve.RANGE_STEP],
                         Vec3D.Vec3D(1, 1, 1))

    def test_linear_curves(self):
        curve = BezierCurves()
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 2)]

        for i in range(0, 3):
            curve.append_point(points[i])

        curve_points = curve.draw_curve()

        self.assertEqual(curve.curve[int(curve.RANGE_STEP / 2)],
                         points[1])

    def test_finite_difference(self):
        curve = BezierCurves()
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(2, 8, 6),
                  Vec3D.Vec3D(3, 5, 4),
                  Vec3D.Vec3D(4, 4, 5)]

        for i in range(0, 4):
            curve.append_point(points[i])

        derivative = []
        derivative = curve.finite_difference(2)
        self.assertEqual(derivative[0], Vec3D.Vec3D(-1, -11, -8))
        self.assertEqual(derivative[1], Vec3D.Vec3D(0, 2, 3))

        derivative = curve.finite_difference(3)
        self.assertEqual(derivative[0], Vec3D.Vec3D(1, 13, 11))

    def test_curve_derivative(self):
        curve = BezierCurves()
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(2, 8, 6),
                  Vec3D.Vec3D(3, 5, 4),
                  Vec3D.Vec3D(4, 4, 5)]

        for i in range(0, 4):
            curve.append_point(points[i])

        curve._derivative_calculation(2)

        self.assertEqual(curve.derivative[2][0],
                         Vec3D.Vec3D(-1, -11, -8))
        self.assertEqual(curve.derivative[2][curve.RANGE_STEP],
                         Vec3D.Vec3D(0, 2, 3))

    def test_subdivision(self):
        curve = BezierCurves()
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
            curve.append_point(points[i])

        curve_points = curve.draw_curve()

        for i in range(0, 3):
            self.assertEqual(curve.subdivision_left[0][i],
                             result_points['left'][i])
            self.assertEqual(curve.subdivision_right[0][i],
                             result_points['right'][i])

    def test_degree_elevation(self):
        curve = BezierCurves()
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 3)]

        for i in range(0, 3):
            curve.append_point(points[i])

        elevation = curve.degree_elevation()

        self.assertEqual(elevation[1], Vec3D.Vec3D(0, 2 / 3, 2 / 3))

if __name__ == '__main__':
    unittest.main()
