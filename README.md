# CS372Project2
project for CSC372

A rudimentary stack-based programming language.

Does not yet support oneliners, gotta do a single command per line.

Basic syntax:
- insert <value> : push a value onto the stack
- assign <variable> : assign a variable to the top item on the stack
- print : prints the top item on the stack
- print <variable> : prints a variable
- add/subtract/multiply/divide/modulus : pops the top two items, performs an arithmetic operation, pushes the result.
- equalto/lessthan/greaterthan : pops the top two items, performs a comparison, and pushes a boolean.
- loop <int> : loops for int times
- endloop : marks the end of a loop block

Example program:

insert 5

assign x

loop 5

insert x

insert 5

add

assign x

endloop

print x