# Import statements
from math import isnan

class RPNCalculator():
    # Class variables
    VALID_OPERATIONS = {'+', '-', '*', '/', 'drop', 'roll', 'swap'} # TODO: Start simple and add more later
    INVALID_INPUT_LIMIT = 3 # After this many invalid inputs, calculator will "turn off"

    # Constructor
    def __init__(self):
        # Instance variables
        self.stack = []
        self.invalid_input_cnt = 0

    # Instance methods
    def run(self):
        while True:
            raw_input = self.get_input()
            processed_input = self.process_input(raw_input)
            pass # TODO

    def get_input(self):
        print("Enter operation/number: ", end = "")
        raw_input = input().strip()
        return raw_input

    def process_input(self, raw_input):
        processed_input = None
        try:
            processed_input = float(raw_input)
            if processed_input.is_integer():
                processed_input = int(processed_input)
        except:
            processed_input = raw_input
        return processed_input # Either a float, int, or str

    def print_stack(self):
        print("Stack:")
        for num in self.stack:
            print(num)

    # TODOS
    # - Make `validate_input` function with optional arg for required input type (e.g., number for very first input)
    # - Certain operations require a stack length of at least 2 (e.g., add). Check for that.
    