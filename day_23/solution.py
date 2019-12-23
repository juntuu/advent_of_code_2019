
import sys
import asyncio
from intcode import Intcode


class NAT:
	def __init__(self, qs):
		self.qs = qs
		self.packet = None
		self.last = None
		self.first = None
		self.cond = asyncio.Condition()

	async def go(self):
		while True:
			async with self.cond:
				await self.cond.wait_for(lambda: self.packet and not any(self.qs))
				self.qs[0].extend(self.packet)
				_, y = self.packet
				if self.last == y:
					return self.first, y
				self.last = y
				self.packet = None

	async def ping(self):
		async with self.cond:
			self.cond.notify(1)

	def send(self, x, y):
		if self.first is None:
			self.first = y
		self.packet = x, y


class NIC:
	def __init__(self, address, qs, nat):
		self.address = address
		self.qs = qs
		self.nat = nat
		self.inq = []

	async def get(self):
		q = self.qs[self.address]
		if not q:
			await asyncio.sleep(0)
			return -1
		val = q.pop(0)
		if not q:
			await self.nat.ping()
		return val

	async def put(self, x):
		self.inq.append(x)
		if len(self.inq) == 3:
			dest, x, y = self.inq
			self.inq.clear()
			if dest == 255:
				self.nat.send(x, y)
			else:
				self.qs[dest].extend([x, y])


async def main(prog):
	qs = [[i] for i in range(50)]
	nat = NAT(qs)
	ts = []
	for i, q in enumerate(qs):
		switch = NIC(i, qs, nat)
		t = asyncio.Task(Intcode(switch, switch).task(prog[:]))
		ts.append(t)
	first, repeat = await nat.go()
	for t in ts:
		t.cancel()
	return first, repeat


name = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(name) as f:
	prog = [int(x) for x in f.read().strip().split(',')]

first, repeat = asyncio.run(main(prog))
print('Day 23, part 1:', first)
print('Day 23, part 2:', repeat)

