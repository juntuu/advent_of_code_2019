
from collections import Counter

password_range = (254032, 789860)
adjusted_range = (255555, 788999)


def non_decreasing(seq):
	high = seq[0]
	for x in seq[1:]:
		if x < high:
			return False
		high = x
	return True


def double(seq):
	return any(a == b for a, b in zip(seq, seq[1:]))


start, stop = adjusted_range
matches = [
		s for s in map(str, range(start, stop + 1))
		if non_decreasing(s) and double(s)]

print('Day 4, part 1:', len(matches))

print('Day 4, part 2:', sum(1 for s in matches if 2 in Counter(s).values()))

