#! /usr/bin/python3

# this is meant to implement the sum in the writeup for the version of
# the permutations that only allows one element in the stack at a time

sum_values = [1] # starts with the single element input

for _ in range (10):
    sum_values.append(1 + sum(sum_values))

print(sum_values)
