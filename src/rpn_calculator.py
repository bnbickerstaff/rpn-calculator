from enum import Enum
from abc import ABC, abstractmethod


class InputType(Enum):
    NUMBER = 1
    STRING = 2


class Error(Enum):
    NONE = 1
    INVALID_OP_EMPTY_STACK = 2
    UNSUPPORTED_OP = 3
    INVALID_OP_STACK_LEN_1 = 4
    FULL_STACK = 5
    DIVIDE_BY_ZERO = 6


class RPNCalculator(ABC):
    # Commands/operations that are always valid, require a stack length
    # of at least one, and require a stack length at least two,
    # respectively; defined as sets so their relevant unions can be
    # easily computed
    ALWAYS_VALID_CMDS = {'help', 'h', 'quit', 'q'}
    VALID_ONE_NUM_OPS = {'clear', 'c', 'drop', 'd'}
    VALID_TWO_NUM_OPS = {'+', '-', '*', '/', 'roll', 'r', 'swap', 's'}

    # Stack can only hold this many numbers
    STACK_LENGTH_LIMIT = 100  # Must be an int >= 3

    # Indices to display alongside the stack elements
    DISPLAY_STACK_INDICES = ('x', 'y', *range(3, STACK_LENGTH_LIMIT + 1))

    # After this many invalid inputs, the calculator will shut down
    INVALID_INPUT_LIMIT = 5  # Must be a natural number

    def __init__(self):
        self.stack = []
        self.invalid_input_cnt = 0

    @abstractmethod
    def run(self):
        pass  # Get input > refine input > validate input > preprocess input > process input > display stack

    @abstractmethod
    def get_input(self):
        pass  # Return raw input

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
        # Assume the input is invalid
        self.invalid_input_cnt += 1
        input_is_valid = False

        len_stack = len(self.stack)
        input_type = refined_input['type']
        input_value = refined_input['value']

        if input_type == InputType.STRING and \
            input_value not in RPNCalculator.ALWAYS_VALID_CMDS.union(
                RPNCalculator.VALID_ONE_NUM_OPS,
                RPNCalculator.VALID_TWO_NUM_OPS):
            return Error.UNSUPPORTED_OP
        elif len_stack == 0 and input_type != InputType.NUMBER and \
            input_value not in RPNCalculator.ALWAYS_VALID_CMDS:
            return Error.INVALID_OP_EMPTY_STACK
        elif len_stack == 1 and input_type == InputType.STRING and \
            input_value not in RPNCalculator.ALWAYS_VALID_CMDS.union(
                RPNCalculator.VALID_ONE_NUM_OPS):
            return Error.INVALID_OP_STACK_LEN_1
        elif len_stack == RPNCalculator.STACK_LENGTH_LIMIT and \
            input_type == InputType.NUMBER:
            return Error.FULL_STACK
        elif input_value == '/' and self.stack[-1] == 0:
            return Error.DIVIDE_BY_ZERO
        else:
            # Input is actually valid
            self.invalid_input_cnt = 0
            input_is_valid = True
            return Error.NONE

    @abstractmethod
    def preprocess_input(self, error, refined_input):
        pass  # TODO: Handle error, help and force-quit requests, etc. Return flag indicating whether or not to proceed with processing.

    def process_input(self, refined_input):
        if refined_input['type'] == InputType.NUMBER:
            self.stack.append(refined_input['value'])
        else:  # refined_input['type'] == InputType.STRING
            operation = refined_input['value']
            if operation == '+':
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
            elif operation == 'clear' or operation == 'c':
                self.stack.clear()
            elif operation == 'drop' or operation == 'd':
                self.stack.pop()
            elif operation == 'roll' or operation == 'r':
                self.stack.insert(0, self.stack.pop())
            elif operation == 'swap' or operation == 's':
                self.stack[-2], self.stack[-1] = self.stack[-1], self.stack[-2]

    def display_stack(self):
        pass  # Display the stack (e.g., in the CLI or GUI)
