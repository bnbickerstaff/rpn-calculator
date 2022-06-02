"""Implementation of a reverse Polish notation (RPN) calculator

'Pieces' of the enum and abc modules are imported for the calculator,
which is implemented as an abstract base class (ABC).
"""

from enum import Enum
from abc import ABC, abstractmethod


class InputType(Enum):
    """Input-type enumeration used by RPNCalculator"""

    NUMBER = 1
    STRING = 2


class Error(Enum):
    """Error enumeration used by RPNCalculator"""

    NONE = 1
    INVALID_OP_EMPTY_STACK = 2
    UNSUPPORTED_OP = 3
    INVALID_OP_STACK_LEN_1 = 4
    FULL_STACK = 5
    DIVISION_BY_ZERO = 6


class RPNCalculator(ABC):
    """RPN calculator ABC
    
    Class variables
    ---------------

    ALWAYS_VALID_CMDS, VALID_ONE_NUM_OPS, and VALID_TWO_NUM_OPS
        Commands/operations that are always valid, require a stack
        length of at least one, and require a stack length at least two,
        respectively; defined as sets so their relevant unions can be
        easily computed

    STACK_LENGTH_LIMIT
        Stack can only hold this many numbers

    DISPLAY_STACK_INDICES
        Indices to display alongside the stack elements

    INVALID_INPUT_LIMIT
        After this many invalid inputs, the calculator will shut down
    """

    ALWAYS_VALID_CMDS = {'help', 'h', 'quit', 'q'}
    VALID_ONE_NUM_OPS = {'clear', 'c', 'drop', 'd'}
    VALID_TWO_NUM_OPS = {'+', '-', '*', '/', 'roll', 'r', 'swap', 's'}
    STACK_LENGTH_LIMIT = 100  # Must be an int >= 2
    DISPLAY_STACK_INDICES = ('x', 'y', *range(3, STACK_LENGTH_LIMIT + 1))
    INVALID_INPUT_LIMIT = 5  # Must be a natural number

    def __init__(self):
        """Create and return an RPN calculator object.
        
        Because RPNCalculator is an ABC, this method can only be called
        via a derived class.
        
        The two instance variables are the stack--a list--and the count
        of the number of invalid inputs.
        """

        self.stack = []
        self.invalid_input_cnt = 0

    @abstractmethod
    def run(self):
        """Run the calculator.

        STEPS: Get input > refine input > validate input > preprocess
        input > process input > display stack (if necessary) > repeat
        """
        pass

    @abstractmethod
    def get_input(self):
        """Get and return the raw input (string)."""
        pass

    def refine_input(self, raw_input):
        """Refine the raw input and return the refined input.

        The refined input is a dictionary that contains the input's
        type (i.e., number or string) and value (e.g., 7 or '+').
        """
        refined_input = {}
        try:
            refined_input['value'] = float(raw_input)
            if refined_input['value'].is_integer():
                refined_input['value'] = int(refined_input['value'])
            refined_input['type'] = InputType.NUMBER
        except:
            refined_input['type'] = InputType.STRING
            refined_input['value'] = raw_input.lower()

        return refined_input

    def validate_input(self, refined_input):
        """Validate the refined input and return an error.

        The error is an enumeration, and one of the enumeration's
        enumerators is NONE.
        """
        # Assume the input is invalid
        self.invalid_input_cnt += 1

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
            return Error.DIVISION_BY_ZERO
        else:
            # Input is actually valid
            self.invalid_input_cnt = 0
            return Error.NONE

    @abstractmethod
    def preprocess_input(self, error, refined_input):
        """Handle various things and return a 'proceed' flag.

        The error always needs to be handled, and the refined input may
        hold a specific request--such as 'help' or 'quit'--that also
        needs to be handled.
        """
        pass

    def process_input(self, refined_input):
        """Process the (validated) refined input."""
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
        """Display the stack.
        
        For example, in a command-line or desktop graphical user
        interface--dependant on how the derived class utilizes this ABC
        """
        pass
