
import asyncio
from intcode import Intcode

with open('input.txt') as f:
	prog = [int(x) for x in f.read().strip().split(',')]


async def bot(prog):
	io = asyncio.Queue(), asyncio.Queue()
	cpu = Intcode(*io)
	task = asyncio.Task(cpu.task(prog))

	painted = set()
	white = set()
	x, y = 0, 0
	turns = [0, 1, 0, -1, 0]
	direction = 0
	while not task.done():
		await io[0].put((x, y) in white)
		if await io[1].get():
			white.add((x, y))
		else:
			white.discard((x, y))
		painted.add((x, y))
		if await io[1].get():
			direction += 1
		else:
			direction -= 1
		direction = (direction + 4) % 4
		dx, dy = turns[direction:direction+2]
		x += dx
		y += dy
	await task
	return len(painted)

painted = asyncio.run(bot(prog))
print('Day 11, part 1:', painted)

