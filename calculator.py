# Base class the *RPN* calculator class derives from
from enum import Enum

class InputType(Enum):
    NUMBER = 1
    STRING = 2
    INVALID = 3

class Calculator:
    # Mathematical operations
    def add(self, addend1, addend2):
        return addend1 + addend2 # sum

    def subtract(self, minuend, subtrahend):
        return minuend - subtrahend # difference

    def multiply(self, factor1, factor2):
        return factor1 * factor2 # product

    def divide(self, dividend, divisor):
        return dividend / divisor # quotient

    def power(self, base, exponent):
        return base ** exponent # power

    def reciprocal(self, num):
        return 1 / num # reciprocal

    # TODO: Starting simple. Add more operations (e.g., exp and square) later.

    # Other instance methods
    def input_type(self, input):
        input_type = None
        if type(input) == int or type(input) == float: # Not including `complex` for now
            input_type = InputType.NUMBER
        elif type(input) == str:
            input_type = InputType.STRING
        else:
            input_type = InputType.INVALID
        return input_type
