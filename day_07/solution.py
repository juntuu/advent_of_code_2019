
from intcode import Intcode, puts, gets
from itertools import permutations


with open('input.txt') as f:
	prog = [int(x) for x in f.read().strip().split(',')]

amps = [Intcode(c) for c in 'ABCDE']

# 1: phase setting 0..4
# 2: input from previous, initially 0

max_signal = 0
for phases in permutations(range(5)):
	buf = [0]
	for amp, phase in zip(amps, phases):
		amp.fd0 = gets([phase, buf[-1]])
		amp.fd1 = puts(buf)
		amp(prog[:])
	max_signal = max(max_signal, buf[-1])

print('Day 7, part 1:', max_signal)

