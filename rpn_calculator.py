from calculator import Calculator, InputType
from math import isnan

class RPNCalculator(Calculator):
    def __init__(self):
        self.stack = []

    def run(self):
        print("Enter a number: ", end = "")
        num = self.convert_input_to_num(input())
        if isnan(num):
            print("ERROR: Did not enter a number. Terminating execution.")
            return # Exit this method
        self.stack.append(num)
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

    def print_stack(self):
        pass # TODO: Add functionality
    