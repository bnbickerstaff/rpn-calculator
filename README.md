# rpn-calculator
This is a [Reverse Polish notation (RPN)](https://en.wikipedia.org/wiki/Reverse_Polish_notation) calculator. Thus far, the [abstract base class](https://docs.python.org/3/library/abc.html) and a command-line-interface (CLI) version have been implemented.

`src/run.py` is used to run the command-line calculator. (Refer to [this article](https://realpython.com/run-python-scripts/) for how to run Python scripts.)

Future improvements:
1. Mitigate possible floating-point errors
2. Add more mathematical operations [e.g., `^` (exponentiation) and `sum`, where the latter adds all the elements in the stack together]
3. Develop a (desktop) graphical user interface
