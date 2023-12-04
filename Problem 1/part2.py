import string
import numpy as np

answer = 0

values = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9}
values.update(dict((s, int(s)) for s in string.digits))

values_rev = dict((''.join(reversed(s)), v) for s, v in values.items())

search_forward = np.array(['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', *string.digits])
print(search_forward)
search_backward = np.array([''.join(reversed(s)) for s in search_forward])
print(search_backward)

with open('Problem 1/input.txt', 'r') as f:
    for line in f.readlines():
        position_fwd = np.array([line.find(s) for s in search_forward])
        position_rev = np.array([''.join(reversed(line)).find(s) for s in search_backward])
        found_fwd = search_forward[position_fwd >= 0]
        found_rev = search_backward[position_rev >= 0]
        idx_fwd = np.argmin(position_fwd[position_fwd >= 0])
        idx_rev = np.argmin(position_rev[position_rev >= 0])
        answer += 10 * (values[found_fwd[idx_fwd]]) + values_rev[found_rev[idx_rev]]

print(f'Answer = {answer}')
