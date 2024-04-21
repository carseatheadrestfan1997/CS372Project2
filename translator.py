# translates whatever this language is called into python

import re
import sys
# need:
### int, str, bools 
### var assignment
### math
### bool expressions (AND, OR, NOT)
### comparison
## conditionals (kind of implemented. Basic if statement functioning)
### loops
### printing
# cl args
def handle_insert(stack, variables, command, translated, indented_line, runcommand):
    value_matcher = re.match(r'insert (\d+|true|false|"[^"]*"|\w+)', command)
    if value_matcher:
        value = value_matcher.group(1)
        if value.isdigit():
            if runcommand:
                stack.append(int(value))
            translated.append(indented_line + f"stack.append({value})")
        elif value in ['true', 'false']:
            if runcommand:
                stack.append(value == 'true')
            translated.append(indented_line + f"stack.append({value})")
        elif value.startswith('"') and value.endswith('"'):
            value = value.strip('"')
            if runcommand:
                stack.append(value)
            translated.append(indented_line + f"stack.append('{value}')")
        elif value in variables:
            # is value a var
            if runcommand:
                stack.append(variables[value])
            translated.append(indented_line + f"stack.append({value})")
        else:
            if runcommand:
                print("insert error")
    else:
        if runcommand:
            print("INSERT FAILED")

def handle_print(stack, variables, command, translated, indented_line, runcommand):
    print_matcher = re.match(r'print (\w+)', command)
    if print_matcher:
        variable_name = print_matcher.group(1)
        translated.append(indented_line + f"print({variable_name})")
        if variable_name in variables:
            if runcommand:
                print('#', variables[variable_name])
        else:
            if runcommand:
                print("variable not found")
    elif stack:
        translated.append(indented_line + "print(stack[-1])")
        if runcommand:
            print('#', stack[-1])
    else:
        translated.append(indented_line + "print(stack[-1])")
        if runcommand:
            print("EMPTY STACK")

def handle_remove(stack, translated, indented_line, runcommand):
    translated.append(indented_line + "stack.pop()")
    if not runcommand:
        return
    if stack:
        stack.pop()
    else:
        print("EMPTY STACK")

def handle_assign(stack, variables, command, translated, indented_line, runcommand):
    assign_matcher = re.match(r'assign (\w+)', command)
    if assign_matcher:
        variable_name = assign_matcher.group(1)
        if runcommand and stack:
            value = stack.pop()
            variables[variable_name] = value
        elif runcommand:
            print("CANNOT ASSIGN TO VARIABLE")
        translated.append(indented_line + f"{variable_name} = stack.pop()")
    else:
        if runcommand:
            print("CANNOT ASSIGN TO VARIABLE")

def handle_and(stack, translated, indented_line, runcommand):
    translated.append(indented_line + "a = stack.pop()")
    translated.append(indented_line + "b = stack.pop()")
    translated.append(indented_line + "stack.append(a and b)")
    if not runcommand:
        return
    if len(stack) >= 2:
        a = stack.pop()
        b = stack.pop()
        result = a and b
        stack.append(result)
    else:
        print("Not enough elements")

def handle_or(stack, translated, indented_line, runcommand):
    translated.append(indented_line + "a = stack.pop()")
    translated.append(indented_line + "b = stack.pop()")
    translated.append(indented_line + "stack.append(a or b)")
    if not runcommand:
        return
    if len(stack) >= 2:
        a = stack.pop()
        b = stack.pop()
        result = a or b
        stack.append(result)
    else:
        print("or error")

def handle_not(stack, translated, indented_line, runcommand):
    translated.append(indented_line + "a = stack.pop()")
    translated.append(indented_line + "stack.append(not a)")
    if not runcommand:
        return
    if stack:
        a = stack.pop()
        result = not a
        stack.append(result)
    else:
        print("empty stack")

#!!!NEED TO CHECK TYPES OF THE THINGS AT TOP OF STACK WITH ISINSTANCE
def arithmetic_operations(stack, variables, operation, command, translated, indented_line, runcommand):
    if runcommand:
        if len(stack) < 2:
            print(f"There must be atleast 2 values on the stack for {operation}")
            return
        else:
            b = stack.pop()
            a = stack.pop()

    if operation == 'add':
        if runcommand:
            result = a + b
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "stack.append(a + b)")
    
    elif operation == 'subtract':
        if runcommand:
            result = a - b
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "stack.append(a - b)")
    
    elif operation == 'multiply':
        if runcommand:
            result = a * b
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "stack.append(a * b)")
    
    elif operation == 'divide':
        if runcommand:
            if b == 0:
                print("cannot divide by zero")
                stack.append(a)
                stack.append(b)
                return
            result = a / b
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "stack.append(a / b)")
    
    elif operation == 'modulus':
    
        if runcommand and b == 0:
            print("canont mod by zero")
            if runcommand:
                stack.append(a)
                stack.append(b)
            return
        if runcommand:
            result = a % b
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "stack.append(a % b)")
    
    elif operation == 'equalto':
        if runcommand:
            result = a == b
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "stack.append(a == b)")
    
    elif operation == 'lessthan':
        if runcommand:
            result = a < b
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "stack.append(a < b)")
    
    elif operation == 'greaterthan':
        if runcommand:
            result = a > b
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "stack.append(a > b)")
    
    if runcommand:
        stack.append(result)

# basic if statement. Will try to expand for elif else. 
def handle_if(stack, variables, command, translated, indent, runcommand):
    if_match = re.match(r'^if \((.*)\)$', command)
    if if_match:
        translated.append("    " * indent + "if stack.pop():")
    if if_match and not runcommand:
        inner_commands = if_match.group(1).split(',')
        for cmd in inner_commands:
            parser(stack, variables, cmd.strip(), translated, indent + 1, runcommand)
    # run in live mode
    elif if_match and runcommand:
        inner_commands = if_match.group(1).split(',')
        run = stack.pop()
        for cmd in inner_commands:
            parser(stack, variables, cmd.strip(), translated, indent + 1, run)
            

def parser(stack, variables, command, translated, indent=0, runcommand=True):
    indented_line = "    " * indent
    command_matcher = re.match(r'(if|print|insert|remove|add|assign|and|or|not|subtract|multiply|divide|modulus|greaterthan|lessthan|equalto)', command)
    if command_matcher:
        first_arg = command_matcher.group(1)
        if first_arg == 'insert':
            handle_insert(stack, variables, command, translated, indented_line, runcommand)
        elif first_arg == 'print':
            handle_print(stack, variables, command, translated, indented_line, runcommand)
        elif first_arg == 'remove':
            handle_remove(stack, translated, indented_line, runcommand)
        elif first_arg == 'add':
            arithmetic_operations(stack, variables, 'add', command, translated, indented_line, runcommand)
        elif first_arg == 'subtract':
            arithmetic_operations(stack, variables, 'subtract', command, translated, indented_line, runcommand)
        elif first_arg == 'multiply':
            arithmetic_operations(stack, variables, 'multiply', command, translated, indented_line, runcommand)
        elif first_arg == 'divide':
            arithmetic_operations(stack, variables, 'divide', command, translated, indented_line, runcommand)
        elif first_arg == 'modulus':
            arithmetic_operations(stack, variables, 'modulus', command, translated, indented_line, runcommand)
        elif first_arg == 'greaterthan':
            arithmetic_operations(stack, variables, 'greaterthan', command, translated, indented_line, runcommand)
        elif first_arg == 'lessthan':
            arithmetic_operations(stack, variables, 'lessthan', command, translated, indented_line, runcommand)
        elif first_arg == 'equalto':
            arithmetic_operations(stack, variables, 'equalto', command, translated, indented_line, runcommand)
        elif first_arg == 'assign':
            handle_assign(stack, variables, command, translated, indented_line, runcommand)
        elif first_arg == 'and':
            handle_and(stack, translated, indented_line, runcommand)
        elif first_arg == 'or':
            handle_or(stack, translated, indented_line, runcommand)
        elif first_arg == 'not':
            handle_not(stack, translated, indented_line, runcommand)
        elif first_arg == 'if':
            handle_if(stack, variables, command, translated, indent, runcommand)
    else:
        print("NOT A VALID COMMAND")

def execute_commands(stack, variables, commands, translated, indent=0, runcommand = True):
    i = 0
    loop_command_pattern = re.compile(r'^loop (\d+|\w+)$')
    endloop_pattern = re.compile(r'^endloop$')
    while i < len(commands):
        command = commands[i]
        loop_match = loop_command_pattern.match(command)
        
        if loop_match:
            loop_count_expr = loop_match.group(1)
            if loop_count_expr.isdigit():
                count = int(loop_count_expr)
            elif loop_count_expr in variables and isinstance(variables[loop_count_expr], int):
                count = variables[loop_count_expr]
            else:
                print("Loop count error")
                return
            
            loop_commands = []
            loop_level = 1
            i += 1
            
            while i < len(commands) and loop_level > 0:
                if endloop_pattern.match(commands[i]):
                    loop_level -= 1
                elif loop_command_pattern.match(commands[i]):
                    loop_level += 1
                if loop_level > 0:
                    loop_commands.append(commands[i])
                i += 1
            
            translated.append("    " * indent + f"for _ in range({count}):")
            execute_commands(stack, variables, loop_commands, translated, indent + 1, runcommand)
            # Iterator
            for _ in range(count - 1):
                execute_commands(stack, variables, loop_commands, [], indent + 1, runcommand)

        elif endloop_pattern.match(command):
            print("Bad 'endloop' location.")
            return
        else:
            parser(stack, variables, command, translated, indent, runcommand)
        i += 1

#!!!NEED TO CHECK THE VALIDITY OF COMMANDS WHILE "STUCK" IN A FOR LOOP 
#!!!SHOULD NOT BE HARD. USE REGEX
def main():
    stack = [] 
    
    # dictionary of variables so our language can support var assignment.
    # to make it interesting you can only retrieve variables with insert (var name) and assign variables with assign (var_name)
    variables = {} 
    commands = []
    filecommands = []
    ifstatementhandling = []
    translated = ["stack = []\n"]
    livemode = False
    if len(sys.argv) == 1:
        livemode = True
    elif len(sys.argv) != 2:
        sys.exit(1)
    if not livemode:
        try:
            file = open(sys.argv[1], 'r')
            for line in file:
                filecommands.append(line.strip())
        except OSError as e:
            print(e)
            sys.exit(1)
        
    while True:
        try:
            if livemode:
                command = input("#live mode\n")
            else:
                if filecommands:
                    command = filecommands.pop(0)
                else:
                    command = "kill"
            if command == 'kill':
                print("#-------------THE SCRIPT-------------\n")
                print("\n".join(translated))
                break
            commands.append(command)
            loop_present = False
            for cmd in commands:
                if cmd.startswith("loop"):
                    loop_present = True
                    break
            if command == 'endloop':
                #print(commands)
                loop_count = 0
                for cmd in commands:
                    if cmd.startswith("loop"):
                        loop_count += 1
                    elif cmd == "endloop":
                        loop_count -= 1
                if loop_count == 0:
                    execute_commands(stack, variables, commands, translated, 0, livemode)
                    commands = []
            elif not loop_present:
                parser(stack, variables, command, translated, 0, livemode)
                commands.pop(0)
        except EOFError:
            print("-------------THE SCRIPT-------------\n")
            print("\n".join(translated))
            break

if __name__ == "__main__":
    main()

