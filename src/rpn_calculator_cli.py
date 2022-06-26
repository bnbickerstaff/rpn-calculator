"""RPN calculator that runs in a command-line interface (CLI)

'Pieces' of the rpn_calculator, math, time, and sys modules are imported
for the command-line calculator.
"""

from rpn_calculator import RPNCalculator, Error, InputType
from math import floor, log10
from time import sleep
from sys import exit


class RPNCalculatorCLI(RPNCalculator):
    """RPN calculator--CLI version

    This derived class implements the abstract methods of the RPN
    calculator ABC.
    """

    def run(self):
        print('REVERSE POLISH NOTATION (RPN) CALCULATOR')
        print('At any time, enter "help" or "h" for help.\n')

        while True:
            raw_input = self.get_input()
            refined_input = self.refine_input(raw_input)
            error = self.validate_input(refined_input)
            proceed_flag = self.preprocess_input(error, refined_input)

            if proceed_flag:
                self.process_input(refined_input)
            else:
                if self.invalid_input_cnt == \
                    RPNCalculator.INVALID_INPUT_LIMIT:
                    print('Invalid input limit exceeded. Shutting down.\n')
                    sleep(3)  # Wait three seconds
                    break
                else:
                    continue

            self.display_stack()

    def get_input(self):
        print('Operation/number: ', end='')

        return input().strip()

    def preprocess_input(self, error, refined_input):
        proceed_flag = False
        if error == Error.NONE:
            if refined_input['type'] == InputType.NUMBER:
                proceed_flag = True
            else:  # refined_input['type'] == InputType.STRING
                input_value = refined_input['value']
                if input_value == 'help' or input_value == 'h':
                    with open('help.txt', 'r') as help_txt:
                        print('\n', help_txt.read(), sep='')
                elif input_value == 'quit' or input_value == 'q':
                    exit('\nApplication terminated.\n')
                else:
                    proceed_flag = True
        elif error == Error.INVALID_OP_EMPTY_STACK:
            print('ERROR: Stack is empty. Cannot perform operation.\n')
        elif error == Error.UNSUPPORTED_OP:
            print('ERROR: Entered operation not supported.\n')
        elif error == Error.INVALID_OP_STACK_LEN_1:
            print('ERROR: Cannot perform entered operation with ', end='')
            print('only one element in stack.\n')
        elif error == Error.FULL_STACK:
            print('ERROR: Stack is already at max capacity.\n')
        else:  # error == Error.DIVISION_BY_ZERO
            print('ERROR: Cannot divide by zero.\n')
        
        return proceed_flag

    def display_stack(self):
        len_stack = len(self.stack)
        index_print_width, stack_print_width = 0, 0
        if len_stack != 0:
            index_print_width = floor(log10(len_stack)) + 1
            stack_print_width = max([len(str(num)) for num in self.stack])

        print('\nStack:')
        for i, num in enumerate(self.stack):
            print('{0:>{width0}}: {1:>{width1}}'.format(
                RPNCalculator.DISPLAY_STACK_INDICES[len_stack-1-i],
                num,
                width0=index_print_width,
                width1=stack_print_width))
        print()
