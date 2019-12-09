
from intcode import Intcode, IO

with open('input.txt') as f:
	prog = [int(x) for x in f.read().split(',')]

# prog = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
# prog = [1102,34915192,34915192,7,4,7,99,0]
# prog = [104,1125899906842624,99]

io = IO(lambda: 1, lambda x: print('Day 9, part 1:', x))

computer = Intcode(io, io)
computer(prog)

