from utils import *
from ac3 import *

def selectVar(csp1):
    # sizes = [(len(csp1.D[x]),x) for x in range(len(csp1.D)) if (len(csp1.D[x])) > 1]
    # sizes = sorted(sizes)
    # return sizes[0][1]
    consts = worklist(csp1)
    c_count = [(len([(x,y) for x,y in consts if x == i]),i) if str(csp1)[i] == '.' else (0,i) for i in range(len(csp1.D))]
    c_count = sorted(c_count, reverse=True)
    return c_count[0][1]

def sortValues(i,csp1):
    violate_count = [(len([True for y in neighboors(i,csp1) if x in csp1.D[y]]),x) for x in csp1.D[i]]
    violate_count = sorted(violate_count)
    violations = [x[1] for x in violate_count]
    return violations

def allSingle(csp1):
    for d in csp1.D:
        if len(d) > 1: return False
    return True

def anyEmpty(csp1):
    for d in csp1.D:
        if len(d) < 1: return True
    return False

def assign(x,val,new_csp):
    new_csp.D[x] = [val]
    for k in neighboors(x,new_csp):
        if len(new_csp.D[k]) > 1: 
            new_csp.D[k] = [y for y in new_csp.D[k] if new_csp.C(val,x,y,k)]
    return ac3(new_csp)

def backtracking(csp1):
    print(csp1)
    if allSingle(csp1): return csp1
    if anyEmpty(csp1): return "Falha2"
    i = selectVar(csp1)
    for v in sortValues(i,csp1):
        csp2 = assign(i,v,csp(str(csp1)))
        if csp2: 
            sol = backtracking(csp(str(csp2)))
            if sol: return sol
    return None