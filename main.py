import time
import sys
import logging

from pathlib import Path

from running_method import RunningMethod


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


if __name__ == '__main__':
    BASE_DIR = Path(__file__).resolve().parent

    log = logging.getLogger(__name__)

    try:
        called_method, example_number, filetype = sys.argv[1:4]
    except ValueError:
        log.error('Not enough values...')
        exit()

    INPUT_FILE = BASE_DIR.joinpath(f'io_data/INPUT/{called_method}/{example_number}.txt')
    OUTPUT_FILE = BASE_DIR.joinpath(f'io_data/OUTPUT/{called_method}/{example_number}.{filetype}')

    help_commands = ('--help', 'help', '--h', )

    numeric_methods = {
        'running_method': RunningMethod,
    }

    if called_method in help_commands:
        print('Available numeric methods:')
        print('\n'.join(numeric_method for numeric_method in numeric_methods.keys()))
        exit()
    
    if not numeric_methods.get(called_method):
        raise ModuleNotFoundError(
            f'No such numeric method {called_method}. Type "{help_commands[0]}" to see allowed methods.'
            )
    
    start = time.time()

    method = numeric_methods.get(called_method)(input_file=INPUT_FILE, output_file=OUTPUT_FILE)
    method.write_file()
    
    end = time.time() - start

    print(f'Process finished at {end} seconds')
