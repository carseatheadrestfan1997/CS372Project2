#-------------THE SCRIPT-------------

stack = []

stack.append(True)
if stack.pop():
    stack.append(True)
    if stack.pop():
        stack.append('yes')
        print(stack[-1])
