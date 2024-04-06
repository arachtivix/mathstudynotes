#! /usr/bin/python3

def sim(inp, stk, out):
    # option 0: we're done already
    if len(inp) == 0 and len(stk) == 0:
        lz = ' '.join(out)
        print(f"{lz}")
        return

    opts = []
    # option 1: take from input, place in stack
    if len(inp) > 0:
        stk.append(inp.pop(0))
        sim(inp, stk, out)
        inp.insert(0,stk.pop())

    # option 2: take from stack, place in output
    if len(stk) > 0:
        out.append(stk.pop())
        sim(inp, stk, out)
        stk.append(out.pop(-1))
        
sim(['1','2','3','4','5', '6'], [], [])
