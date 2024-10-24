import time
import sys
import logging

from pathlib import Path

from running_method import RunningMethod
from two_dim_approximation import TwoDimApproximation
from newton_method import NewtonNumericMethod


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


if __name__ == '__main__':
    BASE_DIR = Path(__file__).resolve().parent

    log = logging.getLogger(__name__)

    called_method = sys.argv[1]

    help_commands = ('--help', 'help', '--h', )

    numeric_methods = {
        'running_method': RunningMethod,
        'two_dimensional_approximation': TwoDimApproximation,
        'newton_method': NewtonNumericMethod,
    }

    if called_method in help_commands:
        log.info('Available methods')
        print('\n'.join(numeric_method for numeric_method in numeric_methods.keys()))
        exit()

    try:
        example_number, filetype = sys.argv[2:4]
    except ValueError:
        log.error('Not enough values...')
        exit()

    INPUT_FILE = BASE_DIR.joinpath(f'io_data/INPUT/{called_method}/{example_number}.{filetype}')
    OUTPUT_FILE = BASE_DIR.joinpath(f'io_data/OUTPUT/{called_method}/{example_number}.{filetype}')
    
    if not numeric_methods.get(called_method):
        log.error(
            f'No such numeric method {called_method}. Type "{help_commands[0]}" to see allowed methods.'
            )
        exit()
    
    start = time.time()

    method = numeric_methods.get(called_method)(input_file=INPUT_FILE, output_file=OUTPUT_FILE)
    method.write_csv(1000)
    
    end = time.time() - start

    log.info(f'Process finished at {end} seconds')
