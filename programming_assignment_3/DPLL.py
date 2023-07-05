import sys

count = 0

'''read in file containing KB'''
def read_file(fileName,clauses,symbols):
    #strip comments
    with open(fileName) as my_file:
        for line in my_file:
            l = line.strip("\n").split(" ")
            empty_clause = []
            for i in l:
                if i == "#":
                    break
                elif i[0] == "-":
                    if i[1:] not in symbols:
                        symbols.append(i[1:])
                elif i not in symbols:
                    symbols.append(i)
                empty_clause.append(i)
            clauses.append(empty_clause)

'''returns True if the model is valid for all clauses'''
def modelValid(clauses,model):
    for clause in clauses:
        val = False
        for sym in clause:
            if sym[0] == "-":
                if model[sym[1:]] == -1:
                    val = True
            else:
                if model[sym] == 1:
                    val = True
        if not val:
            return False
    return val

'''returns False if the model is False for any clause'''
def modelNotValid(clauses,model):
    for clause in clauses:
        a = True
        for sym in clause:
            val = True
            if sym[0] != "-":
                if model[sym] == -1:
                    val = False
            else:
                if model[sym[1:]] == 1:
                    val = False
            if val:
                a = False
                break
        if a:
            return False
    return True

'''implements Unit Clause Heuristic. Returns clause only if all other symbols in clause are False'''
def findUnitClause(clauses,model):
    for clause in clauses:
        if len(clause) == 1:
            if clause[0][0] == "-":
                if model[clause[0][1:]] == 0:
                    return (clause[0][1:],-1)
            else:
                if model[clause[0]] == 0:
                    return (clause[0],1)
        if len(clause) > 1:
            c = (None,None)
            for sym in clause:
                if sym[0] == "-":
                    if model[sym[1:]] == -1:
                        c = (None,None)
                        break
                else:
                    if model[sym] == 1:
                        c = (None,None)
                        break

                if sym[0] == "-":
                    if model[sym[1:]] == 0:
                        if c == (None,None):
                            c = (sym[1:],-1)
                        else:
                            return (None,None)
                else:
                    if model[sym] == 0:
                        if c == (None,None):
                            c = (sym,1)
                        else:
                            return (None,None)
            if c != (None,None):
                return c
    return (None,None)

'''contains DPLL algorithm'''
def DPLL(clauses,symbols,model,uch=False):
    print("model:",model)
    global count
    count += 1
    if modelValid(clauses,model):
        return (True,model)
    if not modelNotValid(clauses,model) or len(symbols) == 0:
        return (False,None)
    if uch:
        p,value = findUnitClause(clauses,model)
        if p != None:
            ind = symbols.index(p)
            outputString = "T"
            if value == -1:
                outputString = "F"
            print("trying {}={}".format(p,outputString))
            return DPLL(clauses,symbols[0:ind]+symbols[ind+1:],{**model,**{p:value}},uch)
    p = symbols[0]
    rest = symbols[1:]
    
    print("trying {}=T".format(p))
    model1 = DPLL(clauses,rest,{**model,**{p:1}},uch)
    if model1[0]:
        return model1

    print("backtracking")
    print("trying {}=F".format(p))
    return DPLL(clauses,rest,{**model,**{p:-1}},uch)


def main():
    command_arg = sys.argv
    print("command:",end=" ")
    for i in command_arg:
        print(i,end=" ")
    print()

    clauses,symbols,model = [],[],{}
    uch = False
    for i in range(2,len(command_arg)): #read in command line args and update values of literals
        if command_arg[i] == "+UCH":
            uch = True
        else:
            clauses.append([command_arg[i]])
    read_file(command_arg[1],clauses,symbols)
    for i in symbols:
        model[i] = 0
    solution = DPLL(clauses,symbols,model,uch)
    if solution[0]:
        print("solution:")
        satisfied = []
        for i in solution[1]:
            print("{}: {}".format(i,solution[1][i]))
            if solution[1][i] == 1:
                satisfied.append(i)
        print("just the Satisfied (true) propositions:")
        for i in satisfied:
            print(i,end=" ")
        print()
        print("total DPLL calls: {}".format(count))
        print("UCH={}".format(uch))
    else:
        print("unsatisifiable solution")
        print("total DPLL calls: {}".format(count))
        print("UCH={}".format(uch))


if __name__ == "__main__":
    main()