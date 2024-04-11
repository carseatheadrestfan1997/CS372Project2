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
    commandMatcher = re.match(r'(insert|remove|print|add)', input)
    if commandMatcher:
        firstArg = commandMatcher.group(1)
        if firstArg == 'insert':
            valueMatcher = re.match(r'insert (\d+|true|false|"[^"]*")', input)
            if valueMatcher:
                value = valueMatcher.group(1)
                # INTEGER Support
                if value.isdigit():
                    stack.append(int(value))
                # BOOLEAN Support
                elif value == 'true' or value == 'false':
                    stack.append(value == 'true')
                # STRING Support
                else:
                    stack.append(value.strip('"'))
            else:
                print("insert command contains nothing valid")
        elif firstArg == 'print':
            if stack:
                print(stack[-1])
            else:
                print("Empty STACK ERROR")
        elif firstArg == 'remove':
            if stack:
                stack.pop()
            else:
                print("Empty stack error. Can't remove from top of stack")
        elif firstArg == 'add':
            if len(stack) >= 2:
                if (isinstance(stack[-1], int)) and (isinstance(stack[-2], int)):
                    x = stack.pop()
                    y = stack.pop()
                    stack.append(x + y)
                else:
                    print("The two values on the top of the stack are not integers!")
        else:
            print("Error, not a valid command (succeeded command matcher, failed to find if block for command.) Make sure to remove it from the matcher if it has not been implemented, as this is the only time this really long print statement will run!")
    else:
        print("error, not a valid command (failed command matcher)")

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
