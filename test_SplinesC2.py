import unittest
import Vec3D
from SplinesC0 import InvalidData
from SplinesC2 import *


class TestSplinesC2(unittest.TestCase):
    def test_raises_none_existing_spline_exception(self):
        with self.assertRaises(InvalidData):
            spline = SplineC2(2, [[1, 2], [2, 5]])

        with self.assertRaises(InvalidData):
            spline = SplineC2(1, [[1, 2], [2, 5]])

    def test_raises_exception_draw_spline(self):
        spline = SplineC2(4, [[1, 2], [2, 5], [5, 8]])

        for index in range(0, 7):
            spline.append_deBoor_point(Vec3D.Vec3D(index, index + 1,
                                       index + 2))

        with self.assertRaises(InvalidData):
            spline.draw()

    def test_Bezier_points_count(self):
        spline = SplineC2(3, [[1, 2], [2, 5], [5, 8]])
        count = 10

        for index in range(0, 6):
            spline.append_deBoor_point(Vec3D.Vec3D(index, index + 1,
                                       index + 2))

        spline.draw()
        self.assertEqual(count,
                         spline.splineC1.splineC0.points_count)

    def test_count_deBoor_points_for_splineC1(self):
        spline = SplineC2(3, [[1, 2], [2, 5], [5, 8]])
        count = 8

        for index in range(0, 6):
            spline.append_deBoor_point(Vec3D.Vec3D(index, index + 1,
                                       index + 2))
        spline.draw()
        self.assertEqual(count,
                         len(spline.splineC1.deBoor_points))

    def test_calculation_for_deBoor_points_for_splineC1(self):
        spline = SplineC2(3, [[1, 2], [2, 5]])
        splineC2 = SplineC2(3, [[1, 2], [2, 7]])

        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 0),
                  Vec3D.Vec3D(2, 1, 0),
                  Vec3D.Vec3D(3, 0, 0),
                  Vec3D.Vec3D(4, -1, 0),
                  Vec3D.Vec3D(4, -1, 0)]

        for index in range(0, 5):
            splineC2.append_deBoor_point(points[index])
        splineC2.draw()
        self.assertEqual(6,
                         len(splineC2.splineC1.deBoor_points))

        points = [Vec3D.Vec3D(1, 1, 1),
                  Vec3D.Vec3D(4, 4, 4),
                  Vec3D.Vec3D(8, 4, 4),
                  Vec3D.Vec3D(4, 8, 4),
                  Vec3D.Vec3D(8, 8, 6)]

        result_points = [Vec3D.Vec3D(1, 1, 1),
                         Vec3D.Vec3D(4, 4, 4),
                         Vec3D.Vec3D(5, 4, 4),
                         Vec3D.Vec3D(7, 5, 4),
                         Vec3D.Vec3D(4, 8, 4),
                         Vec3D.Vec3D(8, 8, 6)]

        for index in range(0, 5):
            spline.append_deBoor_point(points[index])

        spline.draw()

        for index in range(0, 6):
            self.assertEqual(result_points[index],
                             spline.splineC1.deBoor_points[index])

if __name__ == '__main__':
    unittest.main()
