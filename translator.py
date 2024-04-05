import re

# i forgot regex syntax
var_assgn = re.compile("^(.+) = (.+)\\.$")

def parse_cmd(cmd):
    print(cmd)

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

# interpreter-style
def main():
    inp = input(">> ")
    while inp != "exit":
        parse_cmd(inp)
        inp = input(">> ")
        
    
if __name__ == "__main__":
    main()
