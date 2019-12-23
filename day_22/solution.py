
def read_file(name):
	steps = []
	with open(name) as f:
		for line in f:
			a, b, *rest = line.split()
			if a == 'cut':
				steps.append(('cut', int(b)))
			elif b == 'into':
				steps.append(('rev', 0))
			elif b == 'with':
				steps.append(('step', int(rest[1])))
	return steps


def shuffle(steps, deck):
	temp = list(deck)
	for a, b in steps:
		if a == 'cut':
			b %= len(deck)
			deck = deck[b:] + deck[:b]
		elif a == 'rev':
			deck.reverse()
		elif a == 'step':
			n = len(temp)
			i = 0
			for c in deck:
				temp[i] = c
				i += b % len(deck)
				i %= n
			deck, temp = temp, deck
	return deck


def mod_inverse(a, n):
	t = 0
	newt = 1
	r = n
	newr = a
	while newr != 0:
		quotient = r // newr
		t, newt = newt, t - quotient * newt
		r, newr = newr, r - quotient * newr
	assert r <= 1
	if t < 0:
		t += n
	return t


def mod_div(a, b, m):
	a = a % m
	inv = mod_inverse(b, m)
	return (inv * a) % m


def dedup(s, m):
	(a, x), (b, y), (c, z) = s[:3]
	if a == b:
		if a == 'cut':
			s[1] = (a, (x + y) % m)
		if a == 'step':
			s[1] = (a, (x * y) % m)
		s.pop(0)
	elif b == c:
		if b == 'cut':
			s[2] = (b, (y + z) % m)
		if b == 'step':
			s[2] = (b, (y * z) % m)
		s.pop(1)


def swap(s, m):
	(a, x), (b, y), (c, z) = s[:3]
	if a == 'step' and b == 'cut':
		s[0] = ('cut', mod_div(y, x, m))
		s[1] = ('step', x)
	if b == 'step' and c == 'cut':
		s[1] = ('cut', mod_div(z, y, m))
		s[2] = ('step', y)


def simplify(steps, m):
	while len(steps) > 2:
		swap(steps, m)
		dedup(steps, m)
	return steps


def fake_shuffle(steps, times, pos, length):
	new = []
	for s, n in steps:
		if s == 'rev':
			new.append(('step', length-1))
			new.append(('cut', 1))
		else:
			new.append((s, n))
	steps = new
	while times:
		steps = simplify(steps, length)
		if times % 2:
			for a, b in reversed(steps):
				if a == 'cut':
					pos = (pos + b) % length
				elif a == 'step':
					pos = mod_div(pos, b, length)
		times //= 2
		steps = steps + steps
	return pos


if __name__ == '__main__':
	import sys
	steps = read_file(sys.argv[1] if len(sys.argv) > 1 else 'input.txt')

	cards = 10007
	deck = shuffle(steps, list(range(cards)))
	print('Day 22, part 1:', deck.index(2019))

	cards = 119315717514047
	shuffles = 101741582076661

	res = fake_shuffle(steps, shuffles, 2020, cards)
	print('Day 22, part 2:', res)

