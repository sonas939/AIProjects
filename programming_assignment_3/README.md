HOW TO RUN PROGRAM
1. Enter python3 DPLL.py [filename] into the command line
    a. To add facts/enable UCH on the command line, simply enter them after filename. Ex. python3 DPLL.py sammy.cnf O1Y O2W +UCH
2. Profuse error checking is not implemented. For instance, if an invalid filename is entered, the program will crash. 
3. After running the program, the model will be outputted if satisfiable. If the solution is unsatisfiable, unsatisfiable will be outputted. 