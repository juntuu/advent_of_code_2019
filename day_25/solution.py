
import sys
from intcode import Intcode


class Game:
	def __init__(self, verbose=False, prompt=input):
		self.verbose = verbose
		self.prompt = prompt
		self.inv = []
		self.items = []
		self.buf = ''
		self.line = None
		self.i = 0
		self.check_point = False
		self.result = None
		self.commands = []

	def parse_buf(self):
		line = self.buf
		if line.startswith('Items'):
			self.i = 1
			self.items = []
		elif line.startswith('== Security Checkpoint'):
			self.check_point = True
		elif self.i:
			self.items.append(line[2:])
			self.i += 1

	def decide(self):
		if self.check_point and self.inv:
			print('Items in your inventory:')
			for i, x in enumerate(self.inv):
				print(f'{i+1}. {x}')
		d = {'n': 'north', 'e': 'east', 's': 'south', 'w': 'west'}
		x = self.prompt()
		if x in d:
			x = d[x]
		elif x.startswith('t ') or x.startswith('d '):
			c, n = x.split()
			it = self.items[int(n)-1]
			if c == 't':
				x = f'take {it}'
			elif c == 'd':
				x = f'drop {it}'
		self.commands.append(x)
		self.line = iter(x + '\n')
		self.check_point = False
		self.i = 0

	async def get(self):
		return ord(next(self.line))

	async def put(self, x):
		x = chr(x)
		if self.verbose:
			if not self.buf and self.i and x == '-':
				sys.stdout.write(f'{self.i}.')
			else:
				sys.stdout.write(x)
		if x == '\n':
			if self.buf == 'Command?':
				self.decide()
			elif 'typing ' in self.buf:
				_, _, rest = self.buf.partition('typing ')
				self.result = int(rest.split()[0])
			else:
				self.parse_buf()
			self.buf = ''
		else:
			self.buf += x


with open('input.txt') as f:
	prog = [int(x) for x in f.read().strip().split(',')]

# mouse, prime number, hypercube, wreath
v = '-v' in sys.argv
if v:
	g = Game(v)
else:
	commands = iter([
		'west', 'take mouse',
		'north', 'west', 'north', 'east', 'take hypercube',
		'north', 'east', 'take prime number',
		'west', 'south', 'west', 'north', 'west', 'north', 'take wreath',
		'south', 'east', 'south', 'south', 'west', 'west', 'north',
		])
	g = Game(prompt=lambda: next(commands))

Intcode(g, g)(prog)
print('Day 25, part 1:', g.result)

