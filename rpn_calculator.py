# Import statements
from enum import Enum
from math import isnan

class InputType(Enum):
    NUMBER = 1
    STRING = 2

class RPNCalculator():
    # Class variables
    VALID_ONE_ARG_OPERATIONS = {'drop'} # TODO: Start simple and add more later
    VALID_TWO_ARG_OPERATIONS = {'+', '-', '*', '/', 'roll', 'swap'} # TODO: Start simple and add more later
    VALID_OPERATIONS = VALID_ONE_ARG_OPERATIONS.union(VALID_TWO_ARG_OPERATIONS)
    INVALID_INPUT_LIMIT = 3 # After this many invalid inputs, calculator will "shut down"

    # Constructor
    def __init__(self):
        # Instance variables
        self.stack = []
        self.invalid_input_cnt = 0

    # Instance methods
    def run(self):
        while True:
            raw_input = self.get_input()
            refined_input = self.refine_input(raw_input)
            input_is_valid = self.validate_input(refined_input)
            if input_is_valid == False:
                if self.invalid_input_cnt == RPNCalculator.INVALID_INPUT_LIMIT:
                    print("Invalid input limit exceeded. Shutting down.")
                    break
                else:
                    continue
            else:
                self.process_input(refined_input)
            self.print_stack()

    def get_input(self):
        print("Enter operation/number: ", end = "")
        raw_input = input().strip().lower()

        return raw_input

    def refine_input(self, raw_input):
        refined_input = {}
        try:
            refined_input['value'] = float(raw_input)
            if refined_input['value'].is_integer():
                refined_input['value'] = int(refined_input['value'])
            refined_input['type'] = InputType.NUMBER
        except:
            refined_input['value'] = raw_input
            refined_input['type'] = InputType.STRING

        return refined_input

    def validate_input(self, refined_input):
        self.invalid_input_cnt += 1
        input_is_valid = False
        if len(self.stack) == 0 and refined_input['type'] != InputType.NUMBER:
            print("ERROR: Stack is empty. Cannot perform entered operation.")
        elif refined_input['type'] == InputType.STRING and len(self.stack) != 0 \
            and refined_input['value'] not in RPNCalculator.VALID_OPERATIONS:
            print("ERROR: Entered operation not supported.")
        elif refined_input['type'] == InputType.STRING and len(self.stack) == 1 \
            and refined_input['value'] not in RPNCalculator.VALID_ONE_ARG_OPERATIONS:
            print("ERROR: Cannot perform entered operation with only one element in stack.")
        else:
            self.invalid_input_cnt -= 1
            input_is_valid = True

        return input_is_valid

    def process_input(self, refined_input):
        if refined_input['type'] == InputType.NUMBER:
            self.stack.append(refined_input['value'])
        else: # refined_input['type'] == InputType.STRING
            operation = refined_input['value']
            len_stack = len(self.stack)
            if operation == 'drop':
                self.stack.pop()
            elif operation == '+':
                self.stack.append(self.stack.pop() + self.stack.pop())
            elif operation == '-':
                self.stack.append(-(self.stack.pop() - self.stack.pop()))
            elif operation == '*':
                self.stack.append(self.stack.pop() * self.stack.pop())
            elif operation == '/':
                self.stack.append(1 / (self.stack.pop() / self.stack.pop()))
            elif operation == 'roll':
                self.stack.insert(0, self.stack.pop())
            elif operation == 'swap':
                self.stack[len_stack - 2], self.stack[len_stack - 1] = self.stack[len_stack - 1], self.stack[len_stack - 2]

    def print_stack(self):
        print("Stack:")
        for num in self.stack:
            print(num)

    # TODOS
    # - Create class var for stack length limit and check against it
    