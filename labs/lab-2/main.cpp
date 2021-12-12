
#include <gmp.h>
#include <math.h>
#include <chrono>
#include <iostream>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

// Variant - 9
// pow(3, n) * fact(n) / fact(3 * n)
//
//      3 * (1)
// 1) ---------
//    (1) * 2 * 3
//
//        3 * 3 * (1 * 2)
// 2) ---------------------
//    (1 * 2) * 3 * 4 * 5 * 6
//
//          3 * 3 * 3 * (1 * 2 * 3)
// 3) ---------------------------------
//    (1 * 2 * 3) * 4 * 5 * 6 * 7 * 8 * 9

double series_term(int n)
{
	int pow_three = n;  // Количество троек в числителе (степень)
	int divisor = 1;  // Знаменатель
	int term = 0;  // Переменная для множителей знаменателя
	for (int i = n + 1; i <= 3 * n; i++)  // Проходим только от n + 1 до 3n потому что остальное сокращается с верхним факториалом
	{
		term = i;
		while (term % 3 == 0 && pow_three > 0)  // Сокращаем множители в знаменатиле, пока в числителе есть тройки
		{
			term = term / 3;
			pow_three--;
		}
		divisor *= term;  // Домнажаем к знаменателю множители
	}

	return pow(3, pow_three) / divisor;  // Результат
}

struct thread_info {
	int thread_num;
	int start_n;
	int end_n;
	double sum;
};

static void *thread_function(void *arg)
{
	struct thread_info *tinfo = (struct thread_info *)arg;

	printf("Thread %d: %d - %d\n", tinfo->thread_num, tinfo->start_n, tinfo->end_n);

	double sum = 0;
	for (int n = tinfo->start_n; n <= tinfo->end_n; n++)
	{
		sum += series_term(n);
	}

	tinfo->sum = sum;
}

int main(int argc, char ** argv)
{
	int s;
	int num_threads =     argc > 1 ? atoi(argv[1]) : 3;
	int sequence_length = argc > 2 ? atoi(argv[2]) : 3;
	int precision =       argc > 3 ? atoi(argv[3]) : 5;

	if (num_threads > sequence_length)
	{
		printf("Thread counts should be smaller than sequence length\n");
		num_threads = sequence_length;
	}

	struct thread_info *tinfo = new struct thread_info[num_threads];
	pthread_t thread_ids[num_threads];

	if (tinfo == NULL)
		exit(1);

	for (int i = 0; i < num_threads; i++)
	{
		tinfo[i].start_n = i * sequence_length / num_threads + 1;
		tinfo[i].end_n = (i + 1) * sequence_length / num_threads;
		tinfo[i].thread_num = i + 1;

		s = pthread_create(&thread_ids[i], NULL, &thread_function, &tinfo[i]);
		if (s != 0)
			exit(1);
	}

	double total_sum = 0;
	for (int i = 0; i < num_threads; i++)
	{
		s = pthread_join(thread_ids[i], NULL);
		if (s != 0)
			exit(1);

		total_sum += tinfo[i].sum;
	}

	printf("Total sum: %.*f\n", precision, total_sum);

	return 0;
}