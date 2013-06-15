import unittest
import Vec3D
from SplinesC0 import *


class SplinesC0Test(unittest.TestCase):
    def test_raises_InvalidData(self):
        with self.assertRaises(InvalidData):
            spline = SplineC0(-3, 2)

        with self.assertRaises(InvalidData):
            spline = SplineC0(3, 4.6)

        with self.assertRaises(InvalidData):
            spline = SplineC0(6, 6)

    def test_partial_curves_instance(self):
        spline = SplineC0(3, 7)

        for i in range(0, 2):
            self.assertIsInstance(spline.partial_curves[i],
                                  Bezier_curves.BezierCurve)

    def test_partial_curves_count(self):
        spline = SplineC0(3, 7)
        count = 2

        self.assertEqual(len(spline.partial_curves), 2)

    def test_partial_curves_points_count(self):
        spline = SplineC0(3, 7)

        for i in range(0, 7):
            spline.append_point(Vec3D.Vec3D(i, i + 1, i + 2))

        for i in range(0, 2):
            self.assertEqual(len(spline.partial_curves[i].control_points),
                             spline._degree + 1)

if __name__ == '__main__':
    unittest.main()
