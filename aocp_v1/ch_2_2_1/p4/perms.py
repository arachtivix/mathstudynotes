#! /usr/bin/python3

def sim(inp, stk, out, stack_lim):
    # option 0: we're done already
    if len(inp) == 0 and len(stk) == 0:
        lz = ' '.join(out)
        # print(f"{lz}")
        return 1

    ret = 0
    # option 1: take from input, place in stack
    if len(inp) > 0 and len(stk) < stack_lim:
        stk.append(inp.pop(0))
        ret += sim(inp, stk, out, stack_lim)
        inp.insert(0,stk.pop())
    elif len(inp) > 0:
        out.append(inp.pop(0))
        ret += sim(inp, stk, out, stack_lim)
        inp.insert(0,out.pop())

    # option 2: take from stack, place in output
    if len(stk) > 0:
        out.append(stk.pop())
        ret += sim(inp, stk, out, stack_lim)
        stk.append(out.pop())

    return ret
    
def genInput(size):
    ret = []
    for n in range(1, size + 1):
        ret.append(str(n))
    return ret

for n in range(1, 15):
    print(f"{n} -> {sim(genInput(n),[],[],n)}")
