#-------------THE SCRIPT-------------

stack = []

stack.append(1)
stack.append(2)
b = stack.pop()
a = stack.pop()
stack.append(a + b)
print(stack[-1])
for _ in range(25):
    for _ in range(25):
        print(stack[-1])
