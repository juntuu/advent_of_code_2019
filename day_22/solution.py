
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


if __name__ == '__main__':
	import sys
	steps = read_file(sys.argv[1] if len(sys.argv) > 1 else 'input.txt')

	cards = 10007
	deck = shuffle(steps, list(range(cards)))
	print('Day 22, part 1:', deck.index(2019))

