#! /usr/bin/python3

def reverse(n):
  ls = []
  while n > 0:
    ls.append(n % 10)
    n //= 10
  ret = 0
  pow = 0
  for v in ls[::-1]:
    ret += v * (10 ** pow)
    pow += 1
  return ret

for n in range(11,999999):
  nsq = n * n
  ninv = reverse(n)
  ninvsq = ninv * ninv
  if (nsq == reverse(ninvsq)):
    print(f'{n} * {n} = {nsq}, {ninv} * {ninv} = {ninvsq}')
