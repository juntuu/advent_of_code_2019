
import sys
from heapq import heappush, heappop


class Node:
	__slots__ = ('open', 'key', 'door', 'edges', 'id')

	def __init__(self, t, es=None, i=None):
		self.open = 0
		self.door = 0
		self.key = 0
		if t in '.@':
			self.open = 1
		elif t.isupper():
			self.door = ord(t)
		elif t.islower():
			self.key = ord(t.upper())
		self.edges = es or []
		self.id = i


def scan_line(y, line, nodes):
	last = None
	root = None
	for x, c in enumerate(line):
		if c == '#':
			last = None
			continue
		node = Node(c)
		if c == '@':
			root = node
		if last:
			node.edges.append((1, last))
			last.edges.append((1, node))
		up = nodes.get((y-1, x))
		if up:
			node.edges.append((1, up))
			up.edges.append((1, node))
		nodes[y, x] = node
		last = node
	return root


def read_file(name):
	nodes = {}
	root = None
	with open(name) as f:
		for y, line in enumerate(f):
			root = scan_line(y, line.strip(), nodes) or root
	return list(nodes.values()), root


def simplify(nodes, root):
	while True:
		some = False
		for n in nodes:
			if n == root:
				continue
			if len(n.edges) == 1 and (n.open or n.door):
				w, e = n.edges.pop()
				e.edges.remove((w, n))
				some = True
			if not n.edges or not n.open:
				continue
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
	nodes = [n for n in nodes if n.edges]
	for i, n in enumerate(nodes):
		n.id = i
	return nodes


def search(root, target, nodes):
	q = [(0, root, frozenset())]
	seen = set()
	while q:
		d, i, ks = heappop(q)
		if ks == target:
			return d
		for w, e in nodes[i].edges:
			if e.open or e.key or e.door in ks:
				new_keys = ks
				if e.key:
					new_keys |= {e.key}
				if (e.id, new_keys) not in seen:
					seen.add((e.id, new_keys))
					heappush(q, (d + w, e.id, new_keys))


nodes, root = read_file('input.txt' if len(sys.argv) < 2 else sys.argv[1])
nodes = simplify(nodes, root)
keys = {k.key for k in nodes if k.key}

best = search(root.id, keys, nodes)
print('Day 18, part 1:', best)

