# translates whatever this language is called into python

import re

# need:
# int, str, bools
# var assignment
# math
# bool expressions (AND, OR, NOT)
# comparison
# conditionals
# loops
# printing
# cl args

def parser(stack, input):
    command = re.match(r'(insert|othercommandsgorightward)', input)
    if command:
        firstArg = command.group(1)
        if firstArg == 'insert':
            print("Entered insert")
        else:
            print("error")
    else:
        print("error")

def main():
    #generate stack here so it doesnt fall out of scope obviously
    stack = []
    while True:
        command = input()
        if command == 'kill':
            break
        parser(stack, command)


if __name__ == "__main__":
    main()
