
import sys
from intcode import Intcode, IO

name = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(name) as f:
	prog = [int(x) for x in f.read().strip().split(',')]


'''
@ABCD
#???#
if no ? is hole, no need to jump

Jump:
(¬A v ¬B v ¬C) ^ D
=> ¬(A ^ B ^ C) ^ D

@ABCDEFGHI
#???##--#-
next ^or^ after jumping

Jump:
¬(A ^ B ^ C) ^ D ^ (E v H)
'''

sources = '''\
OR A J
AND B J
AND C J
NOT J J
AND D J
WALK
''', '''\
OR A J
AND B J
AND C J
NOT J J
AND D J
OR E T
OR H T
AND T J
RUN
'''

io = IO(lambda: next(code), lambda x: x > 255 and print(f'Day 21, part {part}:', x))
cpu = Intcode(io, io)

for part, source in zip([1, 2], sources):
	code = map(ord, source)
	cpu(prog)

