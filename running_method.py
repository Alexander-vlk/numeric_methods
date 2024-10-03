from numeric_method import NumericMethod


class RunningMethod(NumericMethod):
    __EPSILON = 10e-6

    def __init__(self, *, input_file, output_file):
        super().__init__(input_file, output_file)
        self.read_file()

    def _get_coefficients(self):
        n = self.data.get('dimension')
        matrix = self.data.get('matrix')
        coefficients = {
            'under_diagonal': [0, *[matrix[i][i-1] for i in range(1, n)]],
            'on_diagonal': [matrix[i][i] for i in range(n)],
            'over_diagonal': [*[matrix[i-1][i] for i in range(1, n)], 0],
        }
        return coefficients.values()
    
    def _get_run_factors(self):
        b, c, d = self._get_coefficients()
        r = self.data.get('free_factors')

        # TODO: Make checking for division by zero 

    def _solve(self):
        delta_run_factors, lambda_run_factors = self._get_run_factors()
        
        # TODO: Make solvation: direct run and reverse run
        
        solution = []
        return solution

    def write_file(self):
        self.solution = self._solve()
        return super().write_file()