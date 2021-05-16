# Import statements
from enum import Enum
import math

# Enum used by `input_type` method
class InputType(Enum):
    NUMBER = 1
    STRING = 2
    INVALID = 3

# Base class the *RPN* calculator class derives from
class Calculator:
    # Instance methods
    ## Mathematical (in alphabetical order)
    def add(self, addend1, addend2):
        return addend1 + addend2 # sum

    def divide(self, dividend, divisor):
        return dividend / divisor # quotient

    def multiply(self, factor1, factor2):
        return factor1 * factor2 # product

    def power(self, base, exponent):
        return base ** exponent # power

    def reciprocal(self, num):
        return 1 / num # reciprocal

    def square(self, num):
        return num ** 2 # square

    def square_root(self, num):
        return math.sqrt(num) # square root

    def subtract(self, minuend, subtrahend):
        return minuend - subtrahend # difference

    # TODO: Start simple and add more later

    ## Other
    def input_type(self, input):
        input_type = None
        if type(input) == int or type(input) == float: # Not including `complex` type (for now)
            input_type = InputType.NUMBER
        elif type(input) == str:
            input_type = InputType.STRING
        else:
            input_type = InputType.INVALID
        return input_type
