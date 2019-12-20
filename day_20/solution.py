
import sys
from heapq import heappush, heappop


class Node:
	__slots__ = ('portal', 'edges')

	def __init__(self, portal='', edges=None):
		self.portal = portal
		self.edges = edges or []

	def __lt__(self, other):
		return True


def add_portals(nodes, portals):
	aa = zz = None
	ports = {}
	while portals:
		(x, y), c = portals.popitem()
		port = None
		node = None
		if (x-1, y) in portals:
			port = portals.pop((x-1, y)) + c
			node = nodes.get((x-2, y)) or nodes.get((x+1, y))
		elif (x+1, y) in portals:
			port = c + portals.pop((x+1, y))
			node = nodes.get((x-1, y)) or nodes.get((x+2, y))
		elif (x, y-1) in portals:
			port = portals.pop((x, y-1)) + c
			node = nodes.get((x, y-2)) or nodes.get((x, y+1))
		elif (x, y+1) in portals:
			port = c + portals.pop((x, y+1))
			node = nodes.get((x, y-1)) or nodes.get((x, y+2))
		if port:
			assert node
			node.portal = port
			if port in ports:
				p = ports[port]
				p.edges.append((1, node))
				node.edges.append((1, p))
			else:
				ports[port] = node
			if port == 'AA':
				aa = node
			elif port == 'ZZ':
				zz = node
	return aa, zz


def scan_line(y, line, nodes, portals):
	last = None
	for x, c in enumerate(line):
		if c in '# ':
			last = None
			continue
		if c.isupper():
			portals[x, y] = c
			continue
		node = Node()
		if last:
			node.edges.append((1, last))
			last.edges.append((1, node))
		up = nodes.get((x, y-1))
		if up:
			node.edges.append((1, up))
			up.edges.append((1, node))
		nodes[x, y] = node
		last = node


def read_file(name):
	nodes = {}
	portals = {}
	with open(name) as f:
		for y, line in enumerate(f):
			scan_line(y, line.rstrip(), nodes, portals)
	aa, zz = add_portals(nodes, portals)
	return nodes, aa, zz


def simplify(nodes):
	while True:
		some = False
		for n in nodes.values():
			if n.portal:
				continue
			if len(n.edges) == 1:
				w, e = n.edges.pop()
				e.edges.remove((w, n))
				some = True
			elif len(n.edges) == 2:
				wl, left = n.edges.pop()
				wr, right = n.edges.pop()
				w = wl + wr
				left.edges.remove((wl, n))
				left.edges.append((w, right))
				right.edges.remove((wr, n))
				right.edges.append((w, left))
				some = True
		if not some:
			break
	nodes = {k: n for k, n in nodes.items() if n.edges}
	return nodes


def search(root, target):
	q = [(0, root)]
	seen = set()
	while q:
		d, n = heappop(q)
		if n == target:
			return d
		seen.add(n)
		for w, e in n.edges:
			if e not in seen:
				heappush(q, (d + w, e))


nodes, root, target = read_file('input.txt' if len(sys.argv) < 2 else sys.argv[1])
nodes = simplify(nodes)

best = search(root, target)
print('Day 20, part 1:', best)

