stack = []

stack.append(7)
stack.append(8)
b = stack.pop()
a = stack.pop()
stack.append(a + b)
print(stack[-1])
stack.append(7)
b = stack.pop()
a = stack.pop()
stack.append(a - b)
print(stack[-1])
stack.append(2)
b = stack.pop()
a = stack.pop()
stack.append(a * b)
print(stack[-1])
stack.append(2)
b = stack.pop()
a = stack.pop()
stack.append(a / b)
print(stack[-1])
stack.pop()
stack.append(20)
stack.append(6)
b = stack.pop()
a = stack.pop()
stack.append(a % b)
print(stack[-1])
stack.pop()
stack.append(True)
print(stack[-1])
stack.pop()
stack.append('string')
print(stack[-1])
stack.pop()
stack.append(7)
x = stack.pop()
stack.append(x)
print(stack[-1])
stack.pop()
stack.append(8)
stack.append(8)
b = stack.pop()
a = stack.pop()
stack.append(a == b)
print(stack[-1])
if stack.pop():
    stack.append('if statement ran')
    print(stack[-1])
print(stack[-1])
stack.pop()
stack.append(7)
stack.append(9)
b = stack.pop()
a = stack.pop()
stack.append(a > b)
print(stack[-1])
if stack.pop():
    stack.append('if statement')
    print(stack[-1])
stack.append(7)
stack.append(9)
b = stack.pop()
a = stack.pop()
stack.append(a < b)
print(stack[-1])
stack.pop()
stack.append(True)
a = stack.pop()
stack.append(not a)
print(stack[-1])
stack.pop()
print(x)
for _ in range(10):
    for _ in range(10):
        stack.append(1)
        stack.append(x)
        b = stack.pop()
        a = stack.pop()
        stack.append(a + b)
        x = stack.pop()
        print(x)