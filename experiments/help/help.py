"""
Takes module or function as input, outputs the result of `help()` stored in `help.txt` for easier reading
"""

import contextlib
import importlib

def write_help(func, out_file):
    with open(out_file, 'w') as f:
        with contextlib.redirect_stdout(f):
            help(func)

def begin_interaction():
    user_input = input("Write the name of the function that you want to check, or type 'import' to first import a new module: ")
    while True:
        if user_input.strip().lower() == 'import':
            try:
                module_input = input("\nWrite the name of the module you want to import: ")
                module = importlib.import_module(module_input)
            except Exception as e:
                raise e
        else:
            try:
                write_help(user_input, 'help.txt')
                print("Successful: switch to the `help.txt file to see results\n")
            except Exception as e:
                raise e('please tell me more')
                #print("Unsuccessful: please provide a valid function or import a missing module\n")

if __name__ == "__main__":
    while True:
        user_input = input(
            "Write the name of the function you want to check,\n or type 'import' to try to import a new module: "
            )
        if user_input.lower().strip() == 'import':
            try:
                module_input = input("\nWrite the name of the module you want to import: ")
                module = importlib.import_module(module_input)
            except Exception as e:
                raise e('what')
        else:
            try:
                write_help(user_input, 'help.txt')
                print("Successful: switch to the `help.txt file to see results\n")
            except Exception as e:
                raise e('please tell me more')

        