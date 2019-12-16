
#include <stdio.h>
#include <stdlib.h>

void fft(int *sig, int *out, int n) {
	for (int i = 0; i < n; i++) {
		int new = 0;
		int j = i;
		int sign = 1;
		while (j < n) {
			int max = j+i+1;
			max = max > n ? n : max;
			int sum = 0;
			for (int x = j; x < max; x++)
				sum += sig[x];
			new += sum * sign;
			sign *= -1;
			j += (i+1) * 2;
		}
		out[i] = ((new < 0) ? -new : new) % 10;
	}
}

void hfft(int *sig, int n) {
	int sum = 0;
	while (n--) {
		sum += sig[n];
		sig[n] = sum % 10;
	}
}

void p3(int *sig, int n);

#ifndef N
#define N 650
#endif

int main() {
	int n = 0;
	int *sig = malloc(2 * N * sizeof(int));
	if (!sig) return 1;
	int c;
	while ((c = getchar()) >= '0' && c <= '9' && n < N)
		sig[n++] = c - '0';

	if (c >= '0' && c <= '9' && n == N) {
		printf("too much input, recompile with bigger N (currently %d)\n", N);
		return 1;
	}

	int offset = 0;
	for (int i = 0; i < 7; i++)
		offset = offset * 10 + sig[i];
	if (offset < n * 5000) {
		puts("offset too low, can't apply hfft (Half Flawed Frequency Transmission)");
		return 1;
	}
	int len = n * 10000 - offset;
	int *sig2 = malloc(len * sizeof(int));
	int *sig3 = malloc(len * sizeof(int));
	if (!sig2 || !sig3) return 2;
	for (int i = 0; i < len; i++)
		sig2[i] = sig3[i] = sig[(offset + i) % n];

	for (int i = 0; i < 100; i+=2) {
		fft(sig, sig+n, n);
		fft(sig+n, sig, n);
	}
	for (int i = 0; i < 100; i++)
		hfft(sig2, len);

	printf("Day 16, part 1: ");
	for (int i = 0; i < 8; i++)
		printf("%d", sig[i]);

	printf("\nDay 16, part 2: ");
	for (int i = 0; i < 8; i++)
		printf("%d", sig2[i]);
	puts("");

	p3(sig3, len);

	free(sig);
	free(sig2);
	free(sig3);
}

typedef long T;

/*
 * Adapted from gist by alexanderhaupt:
 *    https://gist.github.com/alexanderhaupt/1ac31ecbd316aca32c469f42d8646c98
 * solving the part 3 from Reddit:
 *    https://www.reddit.com/r/adventofcode/comments/ebb8w6/2019_day_16_part_three_a_fanfiction_by_askalski/
 */

int binom(int n, int k) {
	/* binomial coefficients */
	return k ? n*binom(n-1, k-1)/k : 1;
}


int binomModPrime(T n, T k, T p) {
	/* Lucas's theorem */
	if (k == 0)
		return 1;
	if (n < p && k < p)
		return binom(n, k) % p;
	return (binomModPrime(n / p, k / p, p) * binomModPrime(n % p, k % p, p)) % p;
}


int binomMod10(T n, T k) {
	/* Chinese Remainder Theorem */
	return (binomModPrime(n, k, 2)*5 + binomModPrime(n, k, 5)*6) % 10;
}

#define DAM_TO_URANUS 287029238942
void p3(int *sig, int n) {
	int *binomialsMod10 = malloc(n * sizeof(int));
	if (!binomialsMod10) {
		perror("no luck allocating");
		return;
	}
	for (int i = 0; i < n; i++)
		binomialsMod10[i] = binomMod10(DAM_TO_URANUS - 1 + i, i);
	printf("Day 16, part 3: ");
	for (int i = 0; i < 8; i++) {
		int sum = 0;
		for (int j = 0; j < n-i; j++)
			sum += sig[i+j] * binomialsMod10[j];
		printf("%d", sum % 10);
	}
	puts("");
	free(binomialsMod10);
}

