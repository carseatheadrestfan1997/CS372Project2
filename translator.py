import re
import sys

# TODO: finish conditionals
# TODO: everything else lol

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
            translated.append(indented_line + f"stack.append({value == 'true'})")
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
        elif not runcommand:
            translated.append(indented_line + f"stack.append({value})")
        else:
            throw_error(f"Non-fatal insertion error for value {value}.", stack, translated)
    else:
        if runcommand:
            throw_error("Non-fatal insertion error.", stack, translated)

def handle_print(stack, variables, command, translated, indented_line, runcommand):
    print_matcher = re.match(r'print (\w+)', command)
    print_basic_mathcer = re.match(r'print', command)
    if print_matcher:
        variable_name = print_matcher.group(1)
        if runcommand and variable_name in variables:
            translated.append(indented_line + f"print({variable_name})")
            print('#', variables[variable_name])
        elif runcommand:
            throw_error(f"Variable {variable_name} not found.", stack, translated)
        else:
            translated.append(indented_line + f"print({variable_name})")
    elif print_basic_mathcer:
        if runcommand and stack:
            translated.append(indented_line + "print(stack[-1])")
            print('#', stack[-1])
        elif runcommand:
            throw_error("Non-fatal: Empty stack on print.", stack, translated)
        else:
            translated.append(indented_line + "print(stack[-1])")
    else:
        print('#', 'BAD PRINT COMMAND. PRINT OR PRINT (VAR)')

def handle_remove(stack, translated, indented_line, runcommand):
    if not runcommand:
        translated.append(indented_line + "stack.pop()")
        return
    if stack:
        stack.pop()
        translated.append(indented_line + "stack.pop()")
    else:
        throw_error("Non-fatal: Empty stack on remove.", stack, translated)

def handle_assign(stack, variables, command, translated, indented_line, runcommand):
    assign_matcher = re.match(r'assign (\w+)', command)
    if assign_matcher:
        variable_name = assign_matcher.group(1)
        if variable_name.isdigit():
            throw_error(f"Cannot assign an integer ({variable_name}) as a variable.", stack, translated, kill=not runcommand)
            return
        elif runcommand and stack:
            value = stack.pop()
            variables[variable_name] = value
            translated.append(indented_line + f"{variable_name} = stack.pop()")
        elif runcommand:
            throw_error("Cannot assign to variable.", stack, translated, kill=not runcommand)
        else:
            translated.append(indented_line + f"{variable_name} = stack.pop()")
    else:
        if runcommand:
            throw_error("Cannot assign to variable.", stack, translated, kill=not runcommand)

def handle_and(stack, translated, indented_line, runcommand):
    if not runcommand:
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "stack.append(a and b)")
        return
    if len(stack) >= 2:
        a = stack.pop()
        b = stack.pop()
        result = a and b
        stack.append(result)
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "stack.append(a and b)")
    else:
        throw_error("AND error: empty or insufficient stack.", stack, translated)

def handle_or(stack, translated, indented_line, runcommand):
    if not runcommand:
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "stack.append(a or b)")
        return
    if len(stack) >= 2:
        a = stack.pop()
        b = stack.pop()
        result = a or b
        stack.append(result)
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "stack.append(a or b)")
    else:
        throw_error("OR error: empty or insufficient stack.", stack, translated)

def handle_not(stack, translated, indented_line, runcommand):
    if not runcommand:
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "stack.append(not a)")
        return
    if stack:
        a = stack.pop()
        result = not a
        stack.append(result)
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "stack.append(not a)")
    else:
        throw_error("NOT error: empty stack.", stack, translated)

#!!!NEED TO CHECK TYPES OF THE THINGS AT TOP OF STACK WITH ISINSTANCE
def arithmetic_operations(stack, variables, operation, command, translated, indented_line, runcommand):
    if runcommand:
        if len(stack) < 2:
            throw_error(f"Command error: there must be at least two values on the stack for {operation}", stack, translated)
            return
        else:
            b = stack.pop()
            a = stack.pop()

    if operation == 'add':
        if runcommand:
            try:
                result = a + b
                translated.append(indented_line + "b = stack.pop()")
                translated.append(indented_line + "a = stack.pop()")
                translated.append(indented_line + "stack.append(a + b)")
            except TypeError:
                stack.append(a)
                stack.append(b)
                throw_error(f"TypeError: incompatible types for {operation} {type(a).__name__, type(b).__name__}.", stack, translated)
                return
        else:
            translated.append(indented_line + "b = stack.pop()")
            translated.append(indented_line + "a = stack.pop()")
            translated.append(indented_line + "stack.append(a + b)")
    
    elif operation == 'subtract':
        if runcommand:
            try:
                result = a - b
                translated.append(indented_line + "b = stack.pop()")
                translated.append(indented_line + "a = stack.pop()")
                translated.append(indented_line + "stack.append(a - b)")
            except TypeError:
                stack.append(a)
                stack.append(b)
                throw_error(f"TypeError: incompatible types for {operation} {type(a).__name__, type(b).__name__}.", stack, translated)
                return
        else:
            translated.append(indented_line + "b = stack.pop()")
            translated.append(indented_line + "a = stack.pop()")
            translated.append(indented_line + "stack.append(a - b)")
    
    elif operation == 'multiply':
        if runcommand:
            try:
                result = a * b
                translated.append(indented_line + "b = stack.pop()")
                translated.append(indented_line + "a = stack.pop()")
                translated.append(indented_line + "stack.append(a * b)")
            except TypeError:
                stack.append(a)
                stack.append(b)
                throw_error(f"TypeError: incompatible types for {operation} {type(a).__name__, type(b).__name__}.", stack, translated)
                return
        else:
            translated.append(indented_line + "b = stack.pop()")
            translated.append(indented_line + "a = stack.pop()")
            translated.append(indented_line + "stack.append(a * b)")
    
    elif operation == 'divide':
        if runcommand:
            if b == 0:
                stack.append(a)
                stack.append(b)
                throw_error("Undefined: divide by zero.", stack, translated)
                return
            try:
                result = a / b
                translated.append(indented_line + "b = stack.pop()")
                translated.append(indented_line + "a = stack.pop()")
                translated.append(indented_line + "stack.append(a / b)")
            except TypeError:
                stack.append(a)
                stack.append(b)
                throw_error(f"TypeError: incompatible types for {operation} {type(a).__name__, type(b).__name__}.", stack, translated)
                return
        else:
            translated.append(indented_line + "b = stack.pop()")
            translated.append(indented_line + "a = stack.pop()")
            translated.append(indented_line + "stack.append(a / b)")
    
    elif operation == 'modulus':
    
        if runcommand and b == 0:
            stack.append(a)
            stack.append(b)
            throw_error("Undefined: modulus by zero.", stack, translated)
        if runcommand:
            try:
                result = a % b
                translated.append(indented_line + "b = stack.pop()")
                translated.append(indented_line + "a = stack.pop()")
                translated.append(indented_line + "stack.append(a % b)")
            except TypeError:
                stack.append(a)
                stack.append(b)
                throw_error(f"TypeError: incompatible types for {operation} {type(a).__name__, type(b).__name__}.", stack, translated)
                return
        else:
            translated.append(indented_line + "b = stack.pop()")
            translated.append(indented_line + "a = stack.pop()")
            translated.append(indented_line + "stack.append(a % b)")
    
    elif operation == 'equalto':
        if runcommand:
            try:
                result = a == b
                translated.append(indented_line + "b = stack.pop()")
                translated.append(indented_line + "a = stack.pop()")
                translated.append(indented_line + "stack.append(a == b)")
            except TypeError:
                stack.append(a)
                stack.append(b)
                throw_error(f"TypeError: incompatible types for {operation} {type(a).__name__, type(b).__name__}.", stack, translated)
                return
        else:
            translated.append(indented_line + "b = stack.pop()")
            translated.append(indented_line + "a = stack.pop()")
            translated.append(indented_line + "stack.append(a == b)")
    
    elif operation == 'lessthan':
        if runcommand:
            try:
                result = a < b
                translated.append(indented_line + "b = stack.pop()")
                translated.append(indented_line + "a = stack.pop()")
                translated.append(indented_line + "stack.append(a < b)")
            except TypeError:
                stack.append(a)
                stack.append(b)
                throw_error(f"TypeError: incompatible types for {operation} {type(a).__name__, type(b).__name__}.", stack, translated)
                return
        else:
            translated.append(indented_line + "b = stack.pop()")
            translated.append(indented_line + "a = stack.pop()")
            translated.append(indented_line + "stack.append(a < b)")
    
    elif operation == 'greaterthan':
        if runcommand:
            try:
                result = a > b
                translated.append(indented_line + "b = stack.pop()")
                translated.append(indented_line + "a = stack.pop()")
                translated.append(indented_line + "stack.append(a > b)")
            except TypeError:
                stack.append(a)
                stack.append(b)
                throw_error(f"TypeError: incompatible types for {operation} {type(a).__name__, type(b).__name__}.", stack, translated)
                return
        else:
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
        inner_command_string = if_match.group(1)
        inner_commands = extract_commands(inner_command_string)
        if not runcommand:
            for cmd in inner_commands:
                parser(stack, variables, cmd.strip(), translated, indent + 1, runcommand)
        elif runcommand:
            run = stack.pop()
            for cmd in inner_commands:
                parser(stack, variables, cmd.strip(), translated, indent + 1, run)

def extract_commands(command_string):
    pattern = r'(?:[^,(]|\(.*?\))+'
    commands = re.findall(pattern, command_string)
    filtered_commands = []
    for cmd in commands:
        stripped_cmd = cmd.strip()
        if stripped_cmd:
            filtered_commands.append(stripped_cmd)

    return filtered_commands

def parser(stack, variables, command, translated, indent=0, runcommand=True):
    indented_line = "    " * indent
    command_matcher = re.match(r'(^$|#|if|print|insert|remove|add|assign|and|or|not|subtract|multiply|divide|modulus|greaterthan|lessthan|equalto)', command)
    if command_matcher:
        first_arg = command_matcher.group(1)
        if first_arg == 'insert':
            handle_insert(stack, variables, command, translated, indented_line, runcommand)
        elif first_arg == "" : # ignore empty lines
            return
        elif first_arg == '#': # comments
            translated.append(indented_line + command)
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
        # print("NOT A VALID COMMAND")
        throw_error(f"Syntax error: command \"{command}\" is invalid.", stack, translated, kill=not runcommand)

def execute_commands(stack, variables, commands, translated, indent=0, runcommand=True):
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
                if loop_count_expr in variables:
                    try:
                        count = int(variables[loop_count_expr])
                    except ValueError:
                        throw_error(f"Value error: loop count variable {loop_count_expr} is not an integer.", stack, translated, kill=not runcommand)
                        return
                else:
                    throw_error(f"Value error: loop count variable {loop_count_expr} not found.", stack, translated, kill=not runcommand)
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
            throw_error("Bad endloop location.", stack, translated, kill=not runcommand)
            return
        else:
            parser(stack, variables, command, translated, indent, runcommand)
        i += 1

# rudimentary kill function for when things go bad
# by default, does not kill the script
def throw_error(errormsg, stack, translated, kill=False):
    print(f"ERROR!!! {errormsg}")
    # translated.append(f"# ERROR!!! {errormsg}")
    if kill:
        # print(f"Last stack:\n{stack}\n")
        string = "\n".join(translated)
        print(f"Script up to this point:\n { string } \n")
        print("Killing interpreter...")
        sys.exit()

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
    if not livemode:
        try:
            file = open(sys.argv[1], 'r')
            for line in file:
                filecommands.append(line.strip())
        except OSError as e:
            print(e)
            sys.exit(1)
    # command line arguments. Only works not in livemode.
    if len(sys.argv) > 2 and not livemode:
        for i in range(2, len(sys.argv)):
            variable_name = f'arg{i - 1}'
            variables[variable_name] = sys.argv[i]  
            translated.append(f"{variable_name} = {sys.argv[i]}")
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
