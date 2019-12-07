
from intcode import Intcode
from itertools import permutations
import asyncio


with open('input.txt') as f:
	prog = [int(x) for x in f.read().strip().split(',')]


async def run(prog, amps, phase_range):
	max_signal = 0
	for phases in permutations(phase_range):
		bufs = [asyncio.Queue() for _ in amps]
		for i, (amp, phase) in enumerate(zip(amps, phases)):
			await bufs[i].put(phase)
			amp.fd0 = bufs[i]
			amp.fd1 = bufs[i - 1]
		await bufs[-1].put(0)
		await asyncio.gather(*(amp.task(prog[:]) for amp in amps))
		max_signal = max(max_signal, await bufs[-1].get())
	return max_signal


# 1: phase setting 0..4
# 2: input from previous, initially 0
amps = [Intcode(name=c) for c in 'ABCDE']
max_signal = asyncio.run(run(prog, amps, range(5)))
print('Day 7, part 1:', max_signal)

# 1: phase setting 5..9
# 2..: input from previous, initially 0, feedback from last to first
max_signal = asyncio.run(run(prog, amps, range(5, 10)))
print('Day 7, part 2:', max_signal)

