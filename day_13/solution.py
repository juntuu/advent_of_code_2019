
import curses
import time
import sys

from intcode import Intcode


class Game:
	EMPTY = 0
	BLOCK = 2
	PADDLE = 3
	BALL = 4
	SCORE = (-1, 0)

	def __init__(self, scr=None):
		self.data = {}
		self.buf = []
		self.ball = None
		self.paddle = None
		self.score = 0
		self.scr = scr
		self.total_blocks = None

	@property
	def blocks(self):
		return list(self.data.values()).count(Game.BLOCK)

	async def put(self, a):
		self.buf.append(a)
		if len(self.buf) < 3:
			return
		x, y, tile = self.buf
		self.buf.clear()
		if (x, y) == Game.SCORE:
			self.score = tile
			return
		self.data[x, y] = tile
		if tile == Game.PADDLE:
			self.paddle = x
		elif tile == Game.BALL:
			self.ball = x

	async def get(self):
		if self.scr:
			self.draw()
			time.sleep(1/60)
			self.scr.refresh()
		if self.ball > self.paddle:
			return 1
		if self.ball < self.paddle:
			return -1
		return 0

	def draw(self, cs=' @#—o'):
		blocks = 0
		for (x, y), tile in self.data.items():
			if tile == Game.BLOCK:
				blocks += 1
			self.scr.addch(y + 1, x, cs[tile])
		if self.total_blocks is None:
			self.total_blocks = blocks
		self.scr.addstr(0, 3, f'score: {self.score:6}')
		self.scr.addstr(0, 20, f'blocks: {blocks:4}/{self.total_blocks:<4}')


with open('input.txt') as f:
	prog = [int(x) for x in f.read().strip().split(',')]

game = Game()
Intcode(None, game)(prog)
print('Day 12, part 1:', game.blocks)

prog[0] = 2
if '-v' in sys.argv or '--verbose' in sys.argv:
	try:
		scr = curses.initscr()
		curses.noecho()
		curses.cbreak()
		curses.curs_set(False)
		game = Game(scr)
		Intcode(game, game)(prog)
	finally:
		curses.endwin()
else:
	game = Game()
	Intcode(game, game)(prog)

print('Day 13, part 2:', game.score)

