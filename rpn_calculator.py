from math import isnan

class RPNCalculator():
    # Class variables
    allowed_operations = {'+', '-', '*', '/', 'drop', 'roll', 'swap'} # TODO: Start simple and add more later
    erroneous_input_limit = 3 # After this many erroneous inputs, will terminate execution

    def __init__(self):
        # Instance variables
        self._stack = [] # "Private"

    # Instance methods
    def run(self):
        print("Enter a number: ", end = "")
        num = self.convert_input_to_num(input())
        if isnan(num):
            print("ERROR: Did not enter a number. Terminating execution.")
            return # Exit this method
        self._stack.append(num)
        while True:
            pass # TODO: Add functionality

    def convert_input_to_num(self, input):
        num = None
        try:
            num = float(input)
            if num.is_integer():
                num = int(num)
        except:
            num = float('NaN') 
        return num

    ## Stack
    def clear_stack(self):
        pass # TODO

    def print_stack(self):
        pass # TODO

    # TODOS
    # - Remove whitespace before and after input
    # - Certain operations require a stack length of at least 2 (e.g., add). Check for that.
    