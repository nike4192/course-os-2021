
#include <gmp.h>
#include <math.h>
#include <chrono>
#include <iostream>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

// Variant - 9
// pow(3, n) * fact(n) / fact(3 * n)
void mpf_series_term_ui(mpf_t rop, unsigned long int n)
{
	// Init integers
	mpz_t a, b, c;
	mpz_init(a);
	mpz_init(b);
	mpz_init(c);

	// Init pieces
	mpz_ui_pow_ui(a, 3, n);
	mpz_fac_ui(b, n);
	mpz_fac_ui(c, 3 * n);

	// Init floats
	mpf_t x, y, z;
	mpf_init(x);
	mpf_init(y);
	mpf_init(z);

	// Set the values of int to float
	mpf_set_z(x, a);
	mpf_set_z(y, b);
	mpf_set_z(z, c);

	// Clear integers
	mpz_clear(a);
	mpz_clear(b);
	mpz_clear(c);

	// Series term
	mpf_mul(rop, x, y);
	mpf_div(rop, rop, z);

	// Clear floats
	mpf_clear(x);
	mpf_clear(y);
	mpf_clear(z);
}

struct thread_info {
	pthread_t thread_id;
	int thread_num;
	int start_n;
	int end_n;
	mpf_t sum;
};

static void *thread_function(void *arg)
{
	struct thread_info *tinfo = (struct thread_info *)arg;

	printf("Thread %d: %d - %d\n", tinfo->thread_num, tinfo->start_n, tinfo->end_n);

	mpf_t sum, rop;
	mpf_init(sum);
	mpf_init(rop);
	for (int n = tinfo->start_n; n <= tinfo->end_n; n++)
	{
		mpf_series_term_ui(rop, n);
		mpf_add(sum, sum, rop);
	}

	mpf_clear(rop);
	mpf_set(tinfo->sum, sum);
	mpf_clear(sum);

	return tinfo;
}

int main(int argc, char ** argv)
{
	int s;
	int num_threads =     argc > 1 ? atoi(argv[1]) : 3;
	int sequence_length = argc > 2 ? atoi(argv[2]) : 3;
	int precision =       argc > 3 ? atoi(argv[3]) : 5;
	int bit_count =       argc > 4 ? atoi(argv[4]) : 64;

	mpf_set_default_prec(bit_count);
	if (num_threads > sequence_length)
	{
		printf("Thread counts should be smaller than sequence length\n");
		num_threads = sequence_length;
	}

	struct thread_info *tinfo = new struct thread_info[num_threads];
	pthread_t thread_ids[num_threads];

	if (tinfo == NULL)
		exit(1);

    auto start = std::chrono::steady_clock::now();

	for (int i = 0; i < num_threads; i++)
	{
		tinfo[i].start_n = i * sequence_length / num_threads + 1;
		tinfo[i].end_n = (i + 1) * sequence_length / num_threads;
		tinfo[i].thread_num = i + 1;
		mpf_init(tinfo[i].sum);

		s = pthread_create(&thread_ids[i], NULL, &thread_function, &tinfo[i]);
		if (s != 0)
			exit(1);
	}

	mpf_t total_sum;
	mpf_init(total_sum)
	for (int i = 0; i < num_threads; i++)
	{
		s = pthread_join(thread_ids[i], NULL);
		if (s != 0)
			exit(1);

		mpf_add(total_sum, total_sum, tinfo[i].sum);
		mpf_clear(tinfo[i].sum);
	}

    auto end = std::chrono::steady_clock::now();

	gmp_printf("Total sum: %.*Ff\n", precision, total_sum);

	mpf_clear(total_sum);

    std::chrono::duration<double> elapsed_seconds = end - start;
    std::cout << "Elapsed time: " << elapsed_seconds.count() << "s\n";

	return 0;
}