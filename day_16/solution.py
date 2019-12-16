

def fft(sig, out):
	for i in range(len(sig)):
		new = 0
		j = i
		sign = 1
		while j < len(sig):
			new += sum(sig[j:j+i+1]) * sign
			sign *= -1
			j += (i+1) * 2
		out[i] = abs(new) % 10


def p1(signal):
	sig = signal[:]
	out = sig[:]
	for _ in range(100//2):
		fft(sig, out)
		fft(out, sig)
	return ''.join(map(str, sig[:8]))


def p2(signal, offset):
	N = len(signal) * 10000 - offset
	sig = (signal * (N // len(signal) + 1))[-N:]
	for _ in range(100):
		s = sum(sig)
		for i, e in enumerate(sig):
			sig[i] = s % 10
			s -= e
	return ''.join(map(str, sig[:8]))


with open('input.txt') as f:
	raw = f.read().strip()

signal = [int(x) for x in raw]
offset = int(raw[:7])

print('Day 16, part 1:', p1(signal))
print('Day 16, part 2:', p2(signal, offset))

