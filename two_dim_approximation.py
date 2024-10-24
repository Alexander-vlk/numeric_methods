import logging

from file_reader import InterpolationFileReader


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class TwoDimApproximation(InterpolationFileReader):
    """Implementation of consistent two-dimensional interpolation"""

    def __init__(self, input_file, output_file):
        super().__init__(input_file, output_file)
        self.data = self.read_csv()

    def _linear_interpolation(self, point_left, point_right, count_of_points):
        """Linear interpolation between two points"""
        interpolated_points = []

        x1, y1 = point_left
        x2, y2 = point_right

        step = (x2-x1) / count_of_points

        for i in range(count_of_points):
            t = i * step

            x_interpolated = x1 + t*(x2-x1)
            y_interpolated = y1 + t*(y2-y1)

            interpolated_points.append((x_interpolated, y_interpolated))

        return interpolated_points

    def _interpolate_points(self, count_of_points=10):
        """Interpolation of point sequence"""
        if count_of_points <= 0:
            raise Exception('Count of points should be positive')

        for i in range(len(self.data)-1):
            current_point = self.data[i]
            next_point = self.data[i+1]
            self.solution.extend(self._linear_interpolation(current_point, next_point, count_of_points))

        return self.solution

    def write_csv(self, count_of_points, delimeter=';'):
        self.solution = self._interpolate_points(count_of_points)
        return super().write_csv(delimeter)
