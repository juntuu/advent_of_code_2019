
from collections import Counter

WIDTH = 25
HEIGHT = 6

with open('input.txt') as f:
	image = list(iter(lambda: f.read(WIDTH * HEIGHT).strip(), ''))

counts = (Counter(layer) for layer in image)
least_zeros = min(counts, key=lambda c: c['0'])

print('Day 8, part 1:', least_zeros['1'] * least_zeros['2'])

print('Day 8, part 2:')

layers = zip(*image)
for _ in range(HEIGHT):
	for i in range(WIDTH):
		visible = ('#' if c == '1' else ' ' for c in next(layers) if c != '2')
		print(next(visible, ' ') * 2, end='')
	print()

