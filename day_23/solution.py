
import sys
import asyncio
from intcode import Intcode


class NIC:
	cond = None
	first = None

	def __init__(self, address, qs):
		self.address = address
		self.qs = qs
		self.inq = []

	async def get(self):
		q = self.qs[self.address]
		if not q:
			await asyncio.sleep(0)
			return -1
		return q.pop(0)

	async def put(self, x):
		self.inq.append(x)
		if len(self.inq) == 3:
			dest, x, y = self.inq
			self.inq.clear()
			if dest == 255:
				NIC.first = y
				async with NIC.cond:
					NIC.cond.notify(1)
			else:
				self.qs[dest].extend([x, y])


async def main(prog):
	qs = [[i] for i in range(50)]
	ts = []
	NIC.cond = asyncio.Condition()
	for i, q in enumerate(qs):
		switch = NIC(i, qs)
		t = asyncio.Task(Intcode(switch, switch).task(prog[:]))
		ts.append(t)
	async with NIC.cond:
		await NIC.cond.wait_for(lambda: NIC.first)
	for t in ts:
		t.cancel()
	return NIC.first


name = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(name) as f:
	prog = [int(x) for x in f.read().strip().split(',')]

first = asyncio.run(main(prog))
print('Day 23, part 1:', first)

