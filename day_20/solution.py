
import sys
from heapq import heappush, heappop


class Node:
	__slots__ = ('portal', 'edges')

	def __init__(self, portal='', edges=None):
		self.portal = portal
		self.edges = edges or []

	def __lt__(self, other):
		return True


def out(x, y, bounds):
	x0, y0, x1, y1 = bounds
	return x < x0 or x > x1 or y < y0 or y > y1


def add_portals(nodes, portals, bounds):
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
				p, xp, yp = ports[port]
				d = -1 if out(xp, yp, bounds) else 1
				p.edges.append((1, d, node))
				node.edges.append((1, -d, p))
			else:
				ports[port] = node, x, y
			if port == 'AA':
				aa = node
			elif port == 'ZZ':
				zz = node
	return aa, zz


def scan_line(y, line, nodes, portals, bounds):
	last = None
	for x, c in enumerate(line):
		if c in '# ':
			if c == '#':
				if not bounds[0]:
					bounds[0] = x
				if not bounds[1]:
					bounds[1] = y
				bounds[2] = x
				bounds[3] = y
			last = None
			continue
		if c.isupper():
			portals[x, y] = c
			continue
		node = Node()
		if last:
			node.edges.append((1, 0, last))
			last.edges.append((1, 0, node))
		up = nodes.get((x, y-1))
		if up:
			node.edges.append((1, 0, up))
			up.edges.append((1, 0, node))
		nodes[x, y] = node
		last = node


def read_file(name):
	nodes = {}
	portals = {}
	bounds = [0, 0, 0, 0]
	with open(name) as f:
		for y, line in enumerate(f):
			scan_line(y, line.rstrip(), nodes, portals, bounds)
	aa, zz = add_portals(nodes, portals, bounds)
	return nodes, aa, zz


def simplify(nodes):
	while True:
		some = False
		for n in nodes.values():
			if n.portal:
				continue
			if len(n.edges) == 1:
				w, _, e = n.edges.pop()
				e.edges.remove((w, 0, n))
				some = True
			elif len(n.edges) == 2:
				wl, _, left = n.edges.pop()
				wr, _, right = n.edges.pop()
				w = wl + wr
				left.edges.remove((wl, 0, n))
				left.edges.append((w, 0, right))
				right.edges.remove((wr, 0, n))
				right.edges.append((w, 0, left))
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
		for w, _, e in n.edges:
			if e not in seen:
				heappush(q, (d + w, e))


def search_rec(root, target):
	q = [(0, 0, root)]
	big = float('inf')
	seen = {}
	while q:
		d, lvl, n = heappop(q)
		if lvl == 0 and n == target:
			return d
		for w, x, e in n.edges:
			new_lvl = lvl + x
			if new_lvl < 0:
				continue
			if d + w < seen.get((e, new_lvl), big):
				seen[e, new_lvl] = d + w
				heappush(q, (d + w, new_lvl, e))


nodes, root, target = read_file('input.txt' if len(sys.argv) < 2 else sys.argv[1])
nodes = simplify(nodes)

best = search(root, target)
print('Day 20, part 1:', best)

best = search_rec(root, target)
print('Day 20, part 2:', best)

