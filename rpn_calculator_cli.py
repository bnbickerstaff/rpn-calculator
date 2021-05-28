from enum import Enum
from math import log10, floor


class InputType(Enum):
    NUMBER = 1
    STRING = 2


class RPNCalculatorCLI():

    VALID_ONE_NUM_OPERATIONS = {'clear', 'c', 'drop', 'd'}  # Require stack length of at least one
    VALID_TWO_NUM_OPERATIONS = {'+', '-', '*', '/', 'roll', 'r', 'swap', 's'}  # Require stack length of at least two
    VALID_OPERATIONS = tuple(VALID_ONE_NUM_OPERATIONS.union(VALID_TWO_NUM_OPERATIONS))

    STACK_LENGTH_LIMIT = 10  # Stack can only hold this many numbers
    PRINT_STACK_INDICES = ('x', 'y', *range(3, STACK_LENGTH_LIMIT + 1))  # Indices to print alongside stack elements
    INDEX_PRINT_WIDTH = floor(log10(STACK_LENGTH_LIMIT)) + 1  # Field width for printing latter indices

    INVALID_INPUT_LIMIT = 3  # After this many invalid inputs, calculator will "shut down"

    def __init__(self):
        self.stack = []
        self.invalid_input_cnt = 0

    def run(self):
        while True:
            raw_input = self.get_input()
            refined_input = self.refine_input(raw_input)
            input_is_valid = self.validate_input(refined_input)

            if input_is_valid == False:
                if self.invalid_input_cnt == RPNCalculatorCLI.INVALID_INPUT_LIMIT:
                    print("Invalid input limit exceeded. Shutting down.\n")
                    break
                else:
                    continue
            else:
                self.process_input(refined_input)

            self.print_stack()

    def get_input(self):
        print("Operation/number: ", end="")
        raw_input = input().strip()

        return raw_input

    def refine_input(self, raw_input):
        refined_input = {}
        try:
            refined_input['value'] = float(raw_input)

            if refined_input['value'].is_integer():
                refined_input['value'] = int(refined_input['value'])

            refined_input['type'] = InputType.NUMBER
        except:
            refined_input['value'] = raw_input.lower()
            refined_input['type'] = InputType.STRING

        return refined_input

    def validate_input(self, refined_input):
        # Assume input is invalid
        self.invalid_input_cnt += 1
        input_is_valid = False

        if len(self.stack) == 0 and refined_input['type'] != InputType.NUMBER:
            print("ERROR: Stack is empty. Cannot perform operation.\n")
        elif refined_input['type'] == InputType.STRING and len(self.stack) != 0 and \
            refined_input['value'] not in RPNCalculatorCLI.VALID_OPERATIONS:
            print("ERROR: Entered operation not supported.\n")
        elif refined_input['type'] == InputType.STRING and len(self.stack) == 1 and \
            refined_input['value'] not in RPNCalculatorCLI.VALID_ONE_NUM_OPERATIONS:
            print("ERROR: Cannot perform entered operation with only one element in stack.\n")
        elif refined_input['type'] == InputType.NUMBER and \
            len(self.stack) == RPNCalculatorCLI.STACK_LENGTH_LIMIT:
            print("ERROR: Stack is already at max capacity.\n")
        else:
            # Input is actually valid
            self.invalid_input_cnt = 0
            input_is_valid = True

        return input_is_valid

    def process_input(self, refined_input):
        if refined_input['type'] == InputType.NUMBER:
            self.stack.append(refined_input['value'])
        else: # refined_input['type'] == InputType.STRING
            operation = refined_input['value']
            len_stack = len(self.stack)

            if operation == 'clear' or operation == 'c':
                self.stack.clear()
            elif operation == 'drop' or operation == 'd':
                self.stack.pop()
            elif operation == '+':
                self.stack.append(self.stack.pop() + self.stack.pop())
            elif operation == '-':
                self.stack.append(-(self.stack.pop() - self.stack.pop()))
            elif operation == '*':
                self.stack.append(self.stack.pop() * self.stack.pop())
            elif operation == '/':
                self.stack.append(1 / (self.stack.pop() / self.stack.pop()))
            elif operation == 'roll' or operation == 'r':
                self.stack.insert(0, self.stack.pop())
            elif operation == 'swap' or operation == 's':
                self.stack[len_stack-2], self.stack[len_stack-1] = \
                    self.stack[len_stack-1], self.stack[len_stack-2]

    def print_stack(self):
        stack_print_width = 0
        len_stack = len(self.stack)

        if len_stack != 0:
            stack_print_width = max([len(str(num)) for num in self.stack])

        print("\nStack:")
        for i, num in enumerate(self.stack):
            print("{0:>{width0}}: {1:>{width1}}".format(
                RPNCalculatorCLI.PRINT_STACK_INDICES[len_stack-1-i],
                num,
                width0=RPNCalculatorCLI.INDEX_PRINT_WIDTH,
                width1=stack_print_width))
        print()


    # TODOs:
    # - Protect against division by zero (and other math "no-nos")
    # - Generate single .exe file
    # - Clean up inline commnets IAW PEP 8
    # - Create help doc that is printed to CLI when "help" or "h" is entered
    # - Add more math operations (e.g., sqrt, ^, and exp)
    