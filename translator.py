# translates whatever this language is called into python

import re

# need:
### int, str, bools 
### var assignment
### math
### bool expressions (AND, OR, NOT)
### comparison
# conditionals
### loops
### printing
# cl args


def handle_insert(stack, variables, command, translated, indented_line):
    value_matcher = re.match(r'insert (\d+|true|false|"[^"]*"|\w+)', command)
    if value_matcher:
        value = value_matcher.group(1)
        if value.isdigit():
            stack.append(int(value))
            translated.append(indented_line + f"stack.append({value})")
        elif value in ['true', 'false']:
            stack.append(value == 'true')
            translated.append(indented_line + f"stack.append({value})")
        elif value.startswith('"') and value.endswith('"'):
            value = value.strip('"')
            stack.append(value)
            translated.append(indented_line + f"stack.append('{value}')")
        elif value in variables:
            # is value a var
            stack.append(variables[value])
            translated.append(indented_line + f"stack.append({value})")
        else:
            print("insert error")
    else:
        print("INSERT FAILED")

def handle_print(stack, variables, command, translated, indented_line):
    print_matcher = re.match(r'print (\w+)', command)
    if print_matcher:
        variable_name = print_matcher.group(1)
        if variable_name in variables:
            print(variables[variable_name])
            translated.append(indented_line + f"print({variable_name})")
        else:
            print("variable not found")
    elif stack:
        print(stack[-1])
        translated.append(indented_line + "print(stack[-1])")
    else:
        print("EMPTY STACK")

def handle_remove(stack, translated, indented_line):
    if stack:
        stack.pop()
        translated.append(indented_line + "stack.pop()")
    else:
        print("EMPTY STACK")

def handle_assign(stack, variables, command, translated, indented_line):
    assign_matcher = re.match(r'assign (\w+)', command)
    if assign_matcher and stack:
        variable_name = assign_matcher.group(1)
        value = stack.pop()
        variables[variable_name] = value
        translated.append(indented_line + f"{variable_name} = stack.pop()")
    else:
        print("CANNOT ASSIGN TO VARIABLE")

def handle_and(stack, translated, indented_line):
    if len(stack) >= 2:
        a = stack.pop()
        b = stack.pop()
        result = a and b
        stack.append(result)
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "stack.append(a and b)")
    else:
        print("Not enough elements")

def handle_or(stack, translated, indented_line):
    if len(stack) >= 2:
        a = stack.pop()
        b = stack.pop()
        result = a or b
        stack.append(result)
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "stack.append(a or b)")
    else:
        print("or error")

def handle_not(stack, translated, indented_line):
    if stack:
        a = stack.pop()
        result = not a
        stack.append(result)
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "stack.append(not a)")
    else:
        print("empty stack")

#!!!NEED TO CHECK TYPES OF THE THINGS AT TOP OF STACK WITH ISINSTANCE
def arithmetic_operations(stack, variables, operation, command, translated, indented_line):
    if len(stack) < 2:
        print(f"There must be atleast 2 values on the stack for {operation}")
        return
    
    b = stack.pop()
    a = stack.pop()

    if operation == 'add':
        result = a + b
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "stack.append(a + b)")
    
    elif operation == 'subtract':
        result = a - b
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "stack.append(a - b)")
    
    elif operation == 'multiply':
        result = a * b
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "stack.append(a * b)")
    
    elif operation == 'divide':
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
        if b == 0:
            print("canont mod by zero")
            stack.append(a)
            stack.append(b)
            return
        result = a % b
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "stack.append(a % b)")
    
    elif operation == 'equalto':
        result = a == b
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "stack.append(a == b)")
    
    elif operation == 'lessthan':
        result = a < b
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "stack.append(a < b)")
    
    elif operation == 'greaterthan':
        result = a > b
        translated.append(indented_line + "b = stack.pop()")
        translated.append(indented_line + "a = stack.pop()")
        translated.append(indented_line + "stack.append(a > b)")
        result
    stack.append(result)

def parser(stack, variables, command, translated, indent=0):
    indented_line = "    " * indent
    command_matcher = re.match(r'(print|insert|remove|add|assign|and|or|not|subtract|multiply|divide|modulus|greaterthan|lessthan|equalto)', command)
    if command_matcher:
        first_arg = command_matcher.group(1)
        if first_arg == 'insert':
            handle_insert(stack, variables, command, translated, indented_line)
        elif first_arg == 'print':
            handle_print(stack, variables, command, translated, indented_line)
        elif first_arg == 'remove':
            handle_remove(stack, translated, indented_line)
        elif first_arg == 'add':
            arithmetic_operations(stack, variables, 'add', command, translated, indented_line)
        elif first_arg == 'subtract':
            arithmetic_operations(stack, variables, 'subtract', command, translated, indented_line)
        elif first_arg == 'multiply':
            arithmetic_operations(stack, variables, 'multiply', command, translated, indented_line)
        elif first_arg == 'divide':
            arithmetic_operations(stack, variables, 'divide', command, translated, indented_line)
        elif first_arg == 'modulus':
            arithmetic_operations(stack, variables, 'modulus', command, translated, indented_line)
        elif first_arg == 'greaterthan':
            arithmetic_operations(stack, variables, 'greaterthan', command, translated, indented_line)
        elif first_arg == 'lessthan':
            arithmetic_operations(stack, variables, 'lessthan', command, translated, indented_line)
        elif first_arg == 'equalto':
            arithmetic_operations(stack, variables, 'equalto', command, translated, indented_line)
        elif first_arg == 'assign':
            handle_assign(stack, variables, command, translated, indented_line)
        elif first_arg == 'and':
            handle_and(stack, translated, indented_line)
        elif first_arg == 'or':
            handle_or(stack, translated, indented_line)
        elif first_arg == 'not':
            handle_not(stack, translated, indented_line)
    else:
        print("NOT A VALID COMMAND")

def execute_commands(stack, variables, commands, translated, indent=0):
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
            execute_commands(stack, variables, loop_commands, translated, indent + 1)
            # Iterator
            for _ in range(count - 1):
                execute_commands(stack, variables, loop_commands, [], indent + 1)

        elif endloop_pattern.match(command):
            print("Bad 'endloop' location.")
            return
        else:
            parser(stack, variables, command, translated, indent)
        i += 1

#!!!NEED TO CHECK THE VALIDITY OF COMMANDS WHILE "STUCK" IN A FOR LOOP 
#!!!SHOULD NOT BE HARD. USE REGEX
def main():
    stack = [] 
    
    # dictionary of variables so our language can support var assignment.
    # to make it interesting you can only retrieve variables with insert (var name) and assign variables with assign (var_name)
    variables = {} 
    
    commands = []
    translated = ["stack = []\n"]
    print("Live interaction mode... Type kill to end")
    while True:
        try:
            command = input("------![STACK BASED LANGUAGE]!------\n")
            if command == 'kill':
                print("-------------THE SCRIPT-------------\n")
                print("\n".join(translated))
                break
            commands.append(command)
            loop_present = False
            for cmd in commands:
                if cmd.startswith("loop"):
                    loop_present = True
                    break
            if command == 'endloop':
                print(commands)
                loop_count = 0
                for cmd in commands:
                    if cmd.startswith("loop"):
                        loop_count += 1
                    elif cmd == "endloop":
                        loop_count -= 1
                if loop_count == 0:
                    execute_commands(stack, variables, commands, translated)
                    commands = []
            elif not loop_present:
                parser(stack, variables, command, translated)
                commands.pop(0)
        except EOFError:
            print("EOF")
            break

if __name__ == "__main__":
    main()

