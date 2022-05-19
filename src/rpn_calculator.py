from enum import Enum
from math import log10, floor
from time import sleep


class InputType(Enum):
    NUMBER = 1
    STRING = 2


class RPNCalculator():
    # Valid operations that require stack length of at least one and
    # two, respectively, and their union
    VALID_ONE_NUM_OPERATIONS = {'clear', 'c', 'drop', 'd'}
    VALID_TWO_NUM_OPERATIONS = {'+', '-', '*', '/', 'roll', 'r', 'swap', 's'}
    VALID_OPERATIONS = tuple(
        VALID_ONE_NUM_OPERATIONS.union(VALID_TWO_NUM_OPERATIONS))

    # Stack can only hold this many numbers
    STACK_LENGTH_LIMIT = 100
    # Indices to print alongside stack elements
    PRINT_STACK_INDICES = ('x', 'y', *range(3, STACK_LENGTH_LIMIT + 1))
    # Field width for printing latter indices
    INDEX_PRINT_WIDTH = floor(log10(STACK_LENGTH_LIMIT)) + 1

    # After this many invalid inputs, calculator will "shut down"
    INVALID_INPUT_LIMIT = 3

    def __init__(self):
        self.stack = []
        self.invalid_input_cnt = 0

    def run(self):
        print('REVERSE POLISH NOTATION (RPN) CALCULATOR')
        print('At any time, enter "help" or "h" for help.\n')

        while True:
            raw_input = self.get_input()
            refined_input = self.refine_input(raw_input)
            input_is_valid = self.validate_input(refined_input)

            if not input_is_valid:
                if self.invalid_input_cnt == \
                    RPNCalculator.INVALID_INPUT_LIMIT:
                    print('Invalid input limit exceeded. Shutting down.\n')
                    sleep(3)  # Wait three seconds
                    break
                else:
                    continue
            else:
                self.process_input(refined_input)

            self.print_stack()

    def get_input(self):
        print('Operation/number: ', end='')
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

        len_stack = len(self.stack)
        input_type = refined_input['type']
        input_value = refined_input['value']

        if input_value == 'help' or input_value == 'h':
            # Input is actually valid
            self.invalid_input_cnt = 0
            input_is_valid = True
        elif len_stack == 0 and input_type != InputType.NUMBER:
            print('ERROR: Stack is empty. Cannot perform operation.\n')
        elif input_type == InputType.STRING and len_stack != 0 and \
            input_value not in RPNCalculator.VALID_OPERATIONS:
            print('ERROR: Entered operation not supported.\n')
        elif input_type == InputType.STRING and len_stack == 1 and \
            input_value not in RPNCalculator.VALID_ONE_NUM_OPERATIONS:
            print('ERROR: Cannot perform entered operation with ', end='')
            print('only one element in stack.\n')
        elif input_type == InputType.NUMBER and \
            len_stack == RPNCalculator.STACK_LENGTH_LIMIT:
            print('ERROR: Stack is already at max capacity.\n')
        elif input_value == '/' and self.stack[-1] == 0:
            print('ERROR: Cannot divide by zero.\n')
        else:
            # Input is actually valid
            self.invalid_input_cnt = 0
            input_is_valid = True

        return input_is_valid

    def process_input(self, refined_input):
        if refined_input['type'] == InputType.NUMBER:
            self.stack.append(refined_input['value'])
        else:  # refined_input['type'] == InputType.STRING
            operation = refined_input['value']

            if operation == 'help' or operation == 'h':
                # Not REALLY an operation
                with open('help.txt', 'r') as help_txt:
                    print('\n', help_txt.read(), sep='')
            elif operation == 'clear' or operation == 'c':
                self.stack.clear()
            elif operation == 'drop' or operation == 'd':
                self.stack.pop()
            elif operation == '+':
                x = self.stack.pop()
                y = self.stack.pop()
                self.stack.append(y + x)
            elif operation == '-':
                x = self.stack.pop()
                y = self.stack.pop()
                self.stack.append(y - x)
            elif operation == '*':
                x = self.stack.pop()
                y = self.stack.pop()
                self.stack.append(y * x)
            elif operation == '/':
                x = self.stack.pop()
                y = self.stack.pop()
                self.stack.append(y / x)
            elif operation == 'roll' or operation == 'r':
                self.stack.insert(0, self.stack.pop())
            elif operation == 'swap' or operation == 's':
                len_stack = len(self.stack)
                self.stack[len_stack-2], self.stack[len_stack-1] = \
                    self.stack[len_stack-1], self.stack[len_stack-2]

    def print_stack(self):
        stack_print_width = 0
        len_stack = len(self.stack)

        if len_stack != 0:
            stack_print_width = max([len(str(num)) for num in self.stack])

        print('\nStack:')
        for i, num in enumerate(self.stack):
            print('{0:>{width0}}: {1:>{width1}}'.format(
                RPNCalculator.PRINT_STACK_INDICES[len_stack-1-i],
                num,
                width0=RPNCalculator.INDEX_PRINT_WIDTH,
                width1=stack_print_width))
        print()
