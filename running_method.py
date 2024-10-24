import logging

from file_reader import LinearSystemFileReader


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class RunningMethod(LinearSystemFileReader):
    __EPSILON = 10e-6
    __ROUND_VALUE = 6

    def __init__(self, *, input_file, output_file):
        super().__init__(input_file, output_file)
        self.read_file()
        self.n = self.data.get('dimension')
        self.log = logging.getLogger(__name__)

    def _get_coefficients(self):
        matrix = self.data.get('matrix')
        coefficients = {
            'under_diagonal': [0, *[matrix[i][i-1] for i in range(1, self.n)]],
            'on_diagonal': [matrix[i][i] for i in range(self.n)],
            'over_diagonal': [*[matrix[i-1][i] for i in range(1, self.n)], 0],
        }
        return coefficients.values()
    
    def _is_correct(self, denominator):
        if abs(denominator) < self.__EPSILON:
            self.log.exception(f'It seems like your data are incorrect: {denominator}')
            exit()
    
    def _is_sustainable(self,*, deltas):
        self.log.info(f'deltas {deltas}')
        return all(abs(deltas[i]) > self.__EPSILON for i in range(self.n))
    
    def _get_run_factors(self):
        b, c, d = self._get_coefficients()
        r = self.data.get('free_factors')

        self._is_correct(c[0])
        
        run_factors = {
            'delta': [-d[0]/c[0]],
            'lambda': [r[0]/c[0]],
        }
        self.log.info(f'delta 1: {run_factors['delta'][0]}')
        self.log.info(f'lambda 1: {run_factors['lambda'][0]}')

        for i in range(1, self.n-1):
            last_delta = run_factors['delta'][i-1]
            last_lambda = run_factors['lambda'][i-1]

            denominator = c[i] + b[i] * last_delta
            self.log.info(f'denominator {i}: {denominator}')

            self._is_correct(denominator)
            
            run_factors['delta'].append(
                (- d[i] / denominator)
            )
            run_factors['lambda'].append(
                (r[i] - b[i] * last_lambda) / denominator
            )

            self.log.info(f'delta {i}: {run_factors['delta'][i]}')
            self.log.info(f'lambda {i}: {run_factors['lambda'][i]}')
        
        run_factors['delta'].append(0)

        last_delta = run_factors['delta'][self.n-2]
        last_lambda = run_factors['lambda'][self.n-2]
        run_factors['lambda'].append(
            (r[self.n-1] - b[self.n-1]*last_lambda) / (c[self.n-1] + b[self.n-1]*last_delta)
        )
        return run_factors.values()
        
    def _solve(self):
        delta_run_factors, lambda_run_factors = self._get_run_factors()
        self.log.info('Solution is correct')

        solution = [0] * self.n
        
        current_x = lambda_run_factors[self.n-1] 
        solution[self.n-1] = round(current_x, self.__ROUND_VALUE)
        
        if not self._is_sustainable(deltas=delta_run_factors):
            self.log.warning('Solution is unsustainable')
        else:
            self.log.info('Solution is sustainable')

        for i in range(self.n-1, -1, -1):
            previous_x = delta_run_factors[i] * current_x + lambda_run_factors[i]
            solution[i] = round(previous_x, self.__ROUND_VALUE)

            current_x = previous_x

        return solution

    def write_file(self):
        self.solution = self._solve()
        return super().write_file()
    