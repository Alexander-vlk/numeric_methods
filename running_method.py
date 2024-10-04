from numeric_method import NumericMethod


class RunningMethod(NumericMethod):
    __EPSILON = 10e-6

    def __init__(self, *, input_file, output_file):
        super().__init__(input_file, output_file)
        self.read_file()
        self.n = self.data.get('dimension')


    def _get_coefficients(self):
        matrix = self.data.get('matrix')
        coefficients = {
            'under_diagonal': [0, *[matrix[i][i-1] for i in range(1, self.n)]],
            'on_diagonal': [matrix[i][i] for i in range(self.n)],
            'over_diagonal': [*[matrix[i-1][i] for i in range(1, self.n)], 0],
        }
        return coefficients.values()
    
    def _get_run_factors(self):
        b, c, d = self._get_coefficients()
        r = self.data.get('free_factors')

        if abs(c[0]) < self.__EPSILON:
            raise ZeroDivisionError(f'It seems like your data are incorrect: c1 = {c[0]}')
        
        run_factors = {
            'delta': [-d[0]/c[0]],
            'lambda': [r[0]/c[0]],
        }
        for i in range(1, self.n-1):
            last_delta = run_factors['delta'][i-1]
            last_lambda = run_factors['lambda'][i-1]
            run_factors['delta'].append(
                (- d[i] / (c[i] + b[i] * last_delta))
            )
            run_factors['lambda'].append(
                (r[i] - b[i] * last_lambda) / (c[i] + b[i]*last_delta)
            )
        
        run_factors['delta'].append(0)

        last_delta = run_factors['delta'][self.n-2]
        last_lambda = run_factors['lambda'][self.n-2]
        run_factors['lambda'].append(
            (r[self.n-1] - b[self.n-1]*last_lambda) / (c[self.n-1] + b[self.n-1]*last_delta)
        )
        return run_factors.values()
        
    def _solve(self):
        delta_run_factors, lambda_run_factors = self._get_run_factors()
        
        # TODO: Make solvation: direct run and reverse run

        solution = [0] * self.n
        return solution

    def write_file(self):
        self.solution = self._solve()
        return super().write_file()