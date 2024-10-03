class NumericMethod:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.data = {}
        self.solution = []

    def __str__(self):
        return str(self.solution)

    def read_file(self):
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
        with open(self.output_file, 'w') as output:
            print(*self.solution, file=output)

    def read_csv(self):
        pass

    def write_csv(self):
        pass