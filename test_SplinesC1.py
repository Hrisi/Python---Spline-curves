import unittest
import Vec3D
import Bezier_curves
from SplinesC0 import InvalidData
from SplinesC1 import SplineC1


class TestSplinesC1(unittest.TestCase):
    def test_raise_none_existing_spline_exception(self):
        with self.assertRaises(InvalidData):
            spline = SplineC1(1, [2, 1])

    def test_raise_exception_while_appending_deBoor_points(self):
        spline = SplineC1(3, [2, 1])

        for count in range(0, 6):
            spline.append_deBoor_point(Vec3D.Vec3D(count, count + 1, count))

        with self.assertRaises(IndexError):
            spline.append_deBoor_point(Vec3D.Vec3D(1, 1, 1))

    def test_Bezier_points_count(self):
        spline = SplineC1(3, [2, 1])

        for count in range(0, 6):
            spline.append_deBoor_point(Vec3D.Vec3D(count, count + 1, count))

        spline.draw()
        self.assertEqual(spline.splineC0.points_count,
                         len(spline.splineC0.control_points))

    def test_correct_calculation_Bezier_points(self):
        points = [Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 1),
                  Vec3D.Vec3D(0, 3, 3),
                  Vec3D.Vec3D(2, 5, 5),
                  Vec3D.Vec3D(3, 6, 6),
                  Vec3D.Vec3D(2, 2, 6),
                  Vec3D.Vec3D(2, 2, 7.5),
                  Vec3D.Vec3D(2, 2, 12),
                  Vec3D.Vec3D(3, 5, 8),
                  Vec3D.Vec3D(4, 2, 9)]
        spline = SplineC1(3, [2, 1, 3])

        for count in range(0, 3):
            spline.append_deBoor_point(points[count])

        for count in range(4, 6):
            spline.append_deBoor_point(points[count])

        for count in range(7, 10):
            spline.append_deBoor_point(points[count])

        spline.draw()

        for count in range(0, 10):
            self.assertEqual(points[count],
                             spline.splineC0.control_points[count])

    def test_calculate_control_points_after_replacing_point(self):
        points = [Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 1),
                  Vec3D.Vec3D(0, 3, 3),
                  Vec3D.Vec3D(2, 5, 5),
                  Vec3D.Vec3D(3, 6, 6),
                  Vec3D.Vec3D(2, 2, 6),
                  Vec3D.Vec3D(2, 2, 7.5),
                  Vec3D.Vec3D(2, 2, 12),
                  Vec3D.Vec3D(3, 5, 8),
                  Vec3D.Vec3D(4, 2, 9)]
        spline = SplineC1(3, [2, 1, 3])

        for count in range(0, 3):
            spline.append_deBoor_point(points[count])

        for count in range(4, 6):
            spline.append_deBoor_point(points[count])

        for count in range(7, 9):
            spline.append_deBoor_point(points[count])

        spline.append_deBoor_point(Vec3D.Vec3D(0, 0, 0))
        spline.draw()
        spline.replace_point(7, points[9])

        for index in (0, 8):
            self.assertEqual(spline.control_points[index],
                             points[index])

    def test_draw_spline_raise_exception(self):
        points = [Vec3D.Vec3D(1, 2, -1),
                  Vec3D.Vec3D(2, 3, 4),
                  Vec3D.Vec3D(-3, 4, 8),
                  Vec3D.Vec3D(10, 10, 8),
                  Vec3D.Vec3D(12, 12, 8),
                  Vec3D.Vec3D(10, 15, 8),
                  Vec3D.Vec3D(10, 12, 13)]
        spline = SplineC1(3, [2, 1])

        for count in range(0, 3):
            spline.append_deBoor_point(points[count])

        with self.assertRaises(InvalidData):
            spline.draw()

if __name__ == '__main__':
    unittest.main()
