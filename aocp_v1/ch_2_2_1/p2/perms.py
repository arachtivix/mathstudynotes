#! /usr/bin/python3

from itertools import permutations

#for p in permutations([1,2,3,4]):
#    print(p)

def sim(inp, stk, out):
    # option 0: we're done already
    if len(inp) == 0 and len(stk) == 0:
        print(out)
    
    # option 1: take from input, place in stack
    if len(inp) > 0:
        stk.append(inp.pop(0))
        sim(inp, stk, out)
        inp.insert(0, stk.pop())

    # option 2: take from stack, place in output
    if len(stk) > 0:
        out.insert(0, stk.pop())
        sim(inp, stk, out)
        stk.append(out.pop(0))

sim(['1','2','3','4'], [], [])
