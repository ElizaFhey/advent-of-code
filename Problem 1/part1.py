import string

answer = 0
with open('Problem 1/input.txt', 'r') as f:
    for line in f.readlines():
        digits = [int(s) for s in line if s in string.digits]
        answer += 10 * digits[0] + digits[-1]

print(answer)