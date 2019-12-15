
import curses
import sys
import asyncio
from collections import deque, defaultdict

from intcode import Intcode


def rev(d):
	return [0, 2, 1, 4, 3][d]


def step(x, y, d):
	if d == 1:
		return x, y-1
	if d == 2:
		return x, y+1
	if d == 3:
		return x-1, y
	if d == 4:
		return x+1, y


def find(x0, y0, x, y, data):
	dist = {(x0, y0): 0}
	q = deque([(x0, y0)])
	while q:
		p = q.popleft()
		if p == (x, y):
			break
		for d in [1, 2, 3, 4]:
			p1 = step(*p, d)
			if data.get(p1) in [1, 2]:
				new = dist[p] + 1
				if p1 not in dist or new < dist[p1]:
					dist[p1] = new
					q.append(p1)
	route = [(x, y)]
	while (x0, y0) != (x, y):
		mind = float('inf')
		best = None
		for d in [1, 2, 3, 4]:
			p1 = step(x, y, d)
			di = dist.get(p1, float('inf'))
			if di < mind:
				mind = di
				best = p1
		route.append(best)
		x, y = best
	return route


async def fill(data, oxygen, draw=None):
	new = [oxygen]
	time = -1
	while new:
		time += 1
		new, frontier = [], new
		for pos in frontier:
			for d in [1, 2, 3, 4]:
				p = step(*pos, d)
				if data.get(p) == 1:
					new.append(p)
					data[p] = 6
		if draw:
			draw(data)
			await asyncio.sleep(0.01)
	return time


async def search(prog, x0=0, y0=0, draw=None):
	io = (asyncio.Queue(), asyncio.Queue())
	cpu = Intcode(*io)
	task = asyncio.Task(cpu.task(prog))
	data = {(x0, y0): 1}
	ds = [1, 3, 2, 4]
	tries = defaultdict(lambda: ds[:])
	trail = []
	x, y = x0, y0
	done = False
	route = []
	oxygen = None
	while not done:
		if draw:
			draw({**data, **{p: 5 for p in route}, (x, y): 3, (x0, y0): 4})
		while not tries[x, y]:
			if not trail:
				done = True
				break
			d = rev(trail.pop())
			await io[0].put(d)
			await io[1].get()
			x, y = step(x, y, d)

		while tries[x, y]:
			d = tries[x, y].pop()
			xi, yi = step(x, y, d)
			await io[0].put(d)
			r = await io[1].get()
			data[xi, yi] = r
			if r == 2 and not route:
				route = find(x0, y0, xi, yi, data)
				oxygen = xi, yi
				data[oxygen] = 6
				if draw:
					draw({**{p: 7 for p in data}, **{p: 5 for p in route}, oxygen: 6, (x0, y0): 3})
					await asyncio.sleep(2)
			if r != 0:
				trail.append(d)
				x, y = xi, yi
				break
	task.cancel()
	time = await fill(data, oxygen, draw)
	if draw:
		draw(data)
		await asyncio.sleep(1)
	return len(route) - 1, time


def visual(prog):
	try:
		scr = curses.initscr()
		curses.noecho()
		curses.cbreak()
		curses.curs_set(False)

		def draw(data, cs='#.*@o+O '):
			for (x, y), tile in data.items():
				if 0 <= x < curses.COLS and 0 <= y < curses.LINES:
					scr.addch(y, x, cs[tile])
			scr.refresh()

		task = search(prog, curses.COLS // 2, curses.LINES // 2, draw)
		return asyncio.run(task)
	except Exception as e:
		raise e
	finally:
		curses.endwin()


with open('input.txt') as f:
	prog = [int(x) for x in f.read().strip().split(',')]

if '-v' in sys.argv or '--verbose' in sys.argv:
	moves, time = visual(prog)
else:
	moves, time = asyncio.run(search(prog))
print('Day 15, part 1:', moves)
print('Day 15, part 2:', time)

