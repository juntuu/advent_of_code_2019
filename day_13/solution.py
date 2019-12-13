
from intcode import Intcode


class Game:
	EMPTY = 0
	BLOCK = 2
	PADDLE = 3
	BALL = 4
	SCORE = (-1, 0)

	def __init__(self):
		self.data = {}
		self.buf = []

	@property
	def blocks(self):
		return list(self.data.values()).count(Game.BLOCK)

	async def put(self, a):
		self.buf.append(a)
		if len(self.buf) < 3:
			return
		x, y, tile = self.buf
		self.buf.clear()
		self.data[x, y] = tile


with open('input.txt') as f:
	prog = [int(x) for x in f.read().strip().split(',')]

game = Game()
Intcode(None, game)(prog)
print('Day 12, part 1:', game.blocks)

