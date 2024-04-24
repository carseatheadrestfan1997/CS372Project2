# CS372Project2
project for CSC372

A rudimentary stack-based programming language.<br/>
Does not yet support oneliners, gotta do a single command per line.

To use, just call Python normally. For example, on Windows:
- python translator.py to use the interactive live shell, or
- python translator.py \<filename> to read a file

To call with command line arguments, simply append them to the end of the above commands, e.g.:
- python translator.py example-program \<arg1> \<arg2> ...

Both output the resulting script to stdout, redirect accordingly.

Basic syntax/commands:
- indentation is unimportant when writing a file - the parser will strip it out.
- comments can be written by preceding a line with "#"
- one line must be one command
- insert \<value> : push a value onto the stack
- assign \<variable> : assign a variable to the top item on the stack
- print : prints the top item on the stack
- print \<variable> : prints a variable
- add/subtract/multiply/divide/modulus : pops the top two items, performs an arithmetic operation, pushes the result.
- equalto/lessthan/greaterthan : pops the top two items, performs a comparison, and pushes a boolean.
- and/or : pops the top two items, performs a boolean comparison, and pushes the result.
- not : pops the top element and pushes its boolean negation.
- loop \<int> : loops for int times. int can be a variable assigned to an integer.
- endloop : marks the end of a loop block
- if (\<expression1>, \<expression2>,...) : evaluates the contained expressions if the top item on the stack evaluates to true

Example program:

insert 1<br/>
insert 2<br/>
add<br/>
print<br/>
loop 25<br/>
loop 25<br/>
print<br/>
endloop<br/>
endloop<br/>
insert true<br/>
if (insert 7, print)<br/>
insert false<br/>
if (insert 8, print)<br/>

The resulting script will be as follows:

stack = []

stack.append(1)<br/>
stack.append(2)<br/>
b = stack.pop()<br/>
a = stack.pop()<br/>
stack.append(a + b)<br/>
print(stack[-1])<br/>
for _ in range(25):<br/>
&emsp;for _ in range(25):<br/>
&emsp;&emsp;print(stack[-1])<br/>
stack.append(true)<br/>
if stack.pop():<br/>
&emsp;stack.append(7)<br/>
&emsp;print(stack[-1])<br/>
stack.append(false)<br/>
if stack.pop():<br/>
&emsp;stack.append(8)<br/>
&emsp;print(stack[-1])