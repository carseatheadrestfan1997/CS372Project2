#-------------THE SCRIPT-------------

stack = []

arg1 = 5
arg2 = 10
# demonstrate basic insertion, removal, comparisons
# call with two command line arguments of integers
stack.append(arg1)
stack.append(arg2)
b = stack.pop()
a = stack.pop()
stack.append(a > b)
if stack.pop():
    stack.append(arg1)
    stack.append('MAX:')
    print(stack[-1])
    stack.pop()
    print(stack[-1])
    stack.pop()
stack.append(arg2)
stack.append(arg1)
b = stack.pop()
a = stack.pop()
stack.append(a > b)
if stack.pop():
    stack.append(arg2)
    stack.append('MAX:')
    print(stack[-1])
    stack.pop()
    print(stack[-1])
    stack.pop()
stack.append(arg2)
stack.append(arg1)
b = stack.pop()
a = stack.pop()
stack.append(a == b)
if stack.pop():
    stack.append(arg1)
    stack.append('EQUAL MAXES:')
    print(stack[-1])
    stack.pop()
    print(stack[-1])
    stack.pop()
stack.append(arg1)
stack.append(arg2)
b = stack.pop()
a = stack.pop()
stack.append(a + b)
stack.append('SUM:')
print(stack[-1])
stack.pop()
print(stack[-1])
stack.pop()
stack.append(arg1)
stack.append(arg2)
b = stack.pop()
a = stack.pop()
stack.append(a - b)
stack.append('DIFF:')
print(stack[-1])
stack.pop()
print(stack[-1])
stack.pop()
stack.append(arg1)
stack.append(arg2)
b = stack.pop()
a = stack.pop()
stack.append(a * b)
stack.append('PRODUCT:')
print(stack[-1])
stack.pop()
print(stack[-1])
stack.pop()