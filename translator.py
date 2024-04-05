# translates whatever this language is called into python

import re

# i forgot regex syntax
var_assign = re.compile("some pattern for variable assignment")
type = re.compile("int bool and str")
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

# parse a line and throw things wherever accordingly
def parse_cmd(cmd):
    print(cmd)

# interpreter-style
def main():
    inp = input("? ")
    while inp != "exit":
        parse_cmd(inp)
        inp = input("? ")
        
    
if __name__ == "__main__":
    main()
