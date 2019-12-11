
import asyncio
from intcode import Intcode

with open('input.txt') as f:
	prog = [int(x) for x in f.read().strip().split(',')]


async def bot(prog, white, *, x=0, y=0):
	io = asyncio.Queue(), asyncio.Queue()
	cpu = Intcode(*io)
	task = asyncio.Task(cpu.task(prog))

	painted = set()
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


def print_msg(white, bw=(' ', '#')):
	x_range = range(min(x for x, _ in white), max(x for x, _ in white) + 1)
	y_range = range(max(y for _, y in white), min(y for _, y in white) - 1, -1)
	for y in y_range:
		line = []
		for x in x_range:
			line.append(bw[(x, y) in white] * 2)
		print(''.join(line))


painted = asyncio.run(bot(prog, set()))
print('Day 11, part 1:', painted)

start_x = start_y = 0
white = {(start_x, start_y)}
asyncio.run(bot(prog, white, x=start_x, y=start_y))
print('Day 11, part 2:')
print_msg(white)

