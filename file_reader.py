import csv


class BaseFileReader:
    """Base class for file reading"""

    def __init__(self, input_file: str, output_file: str) -> None:
        self.input_file = input_file
        self.output_file = output_file
        self.data = []
        self.solution = []

    def read_file(self):
        pass

    def write_file(self):
        pass

    def read_csv(self):
        pass

    def write_csv(self):
        pass


class LinearSystemFileReader(BaseFileReader):
    """Class for reading files for linear system"""

    def __init__(self, input_file, output_file):
        super().__init__(input_file, output_file)
        self.data = {}
        self.solution = []

    def read_file(self):
        """Reads diagonals from thw file"""
        with open(self.input_file, 'r') as input:
            self.data = {
                'dimension': int(input.readline()),
                'matrix': [],
                'free_factors': [],
            }
            for row in input.readlines():
                processed_row = list(map(float, row.split()))
                self.data['matrix'].append(processed_row[:-1])
                self.data['free_factors'].append(processed_row[-1])
        return self.data


    def write_file(self):
        """Writes solution of linear system"""
        with open(self.output_file, 'w') as output:
            print(*self.solution, file=output)


class InterpolationFileReader(BaseFileReader):
    """File reader for function approximation"""

    def __init__(self, input_file, output_file):
        super().__init__(input_file, output_file)

    def read_csv(self, delimeter=';'):
        """Reads points from csv file and returns list of points"""
        points = []
        with open(self.input_file, 'r') as input:
            csv_read = csv.reader(input, delimiter=delimeter)
            for row in csv_read:
                point = (float(row[0]), float(row[1]))
                points.append(point)
        return points


    def write_csv(self, delimeter=';'):
        """Writes points to csv file"""
        with open(self.output_file, 'w', newline='') as output:
            csv_write = csv.writer(output, delimiter=delimeter)
            for point in self.solution:
                csv_write.writerow(point)
