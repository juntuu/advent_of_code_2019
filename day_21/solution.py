
import sys
from intcode import Intcode, IO

name = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(name) as f:
	prog = [int(x) for x in f.read().strip().split(',')]


'''
@ABCD
#???#

Jump:
(¬A v ¬B v ¬C) ^ D
=> ¬(A ^ B ^ C) ^ D
'''

code = map(ord, '''\
OR A J
AND B J
AND C J
NOT J J
AND D J
WALK
''')

io = IO(lambda: next(code), lambda x: x > 255 and print('Day 21, part 1:', x))
Intcode(io, io)(prog)

