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
            spline.draw_spline()

    def test_Bezier_points_count(self):
        spline = SplineC2(3, [[1, 2], [2, 5], [5, 8]])
        count = 10

        for index in range(0, 6):
            spline.append_deBoor_point(Vec3D.Vec3D(index, index + 1,
                                       index + 2))

        spline.draw_spline()
        self.assertEqual(count,
                         spline.splineC1.splineC0.points_count)

    def test_count_deBoor_points_for_splineC1(self):
        spline = SplineC2(3, [[1, 2], [2, 5], [5, 8]])
        count = 8

        for index in range(0, 6):
            spline.append_deBoor_point(Vec3D.Vec3D(index, index + 1,
                                       index + 2))
        spline.draw_spline()
        self.assertEqual(count,
                         len(spline.splineC1.deBoor_points))

    def test_calculation_for_deBoor_points_for_splineC1(self):
        spline = SplineC2(3, [[1, 2], [2, 5]])
        points = [Vec3D.Vec3D(1, 1, 1),
                  Vec3D.Vec3D(4, 4, 4),
                  Vec3D.Vec3D(5, 4, 4),
                  Vec3D.Vec3D(8, 4, 4),
                  Vec3D.Vec3D(7, 3, 4),
                  Vec3D.Vec3D(4, 8, 4),
                  Vec3D.Vec3D(8, 8, 6)]

        spline.append_deBoor_point(points[0])
        spline.append_deBoor_point(points[1])
        spline.append_deBoor_point(points[3])
        spline.append_deBoor_point(points[5])
        spline.append_deBoor_point(points[6])

        spline.draw_spline()
        print(spline.splineC1.deBoor_points)
        for index in range(0, 7):
            print(index, spline.splineC1.deBoor_points[index].x)
            self.assertEqual(points[index],
                             spline.splineC1.deBoor_points[index])

if __name__ == '__main__':
    unittest.main()
