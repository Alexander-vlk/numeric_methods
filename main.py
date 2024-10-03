from pathlib import Path


from running_method import RunningMethod


if __name__ == '__main__':

    BASE_DIR = Path(__file__).resolve().parent

    INPUT_FILE = BASE_DIR.joinpath('io_data/INPUT.txt')
    OUTPUT_FILE = BASE_DIR.joinpath('io_data/OUTPUT.txt')

    method = RunningMethod(input_file=INPUT_FILE, output_file=OUTPUT_FILE)

    method.write_file()