
from collections import Counter

WIDTH = 25
HEIGHT = 6

with open('input.txt') as f:
	image = list(iter(lambda: f.read(WIDTH * HEIGHT).strip(), ''))

counts = (Counter(layer) for layer in image)
least_zeros = min(counts, key=lambda c: c['0'])

print('Day 8, part 1:', least_zeros['1'] * least_zeros['2'])

