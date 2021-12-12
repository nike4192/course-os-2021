
#include <chrono>
#include <thread>

#include <algorithm>
#include <iostream>
#include <string.h>
#include <pthread.h>
#include <unistd.h>

#include <mutex>

int foreground_codes[] = {
//  30,  // Black
    31,  // Red
    32,  // Green
    33,  // Yellow
    34,  // Blue
    35,  // Magenta
    36,  // Cyan
    37,  // Light Gray
    90,  // Gray
    91,  // Light Red
    92,  // Light Green
    93,  // Light Yellow
    94,  // Light Blue
    95,  // Light Magenta
    96,  // Light Cyan
    97   // White
};

std::string str;  // Shared variable

enum ThreadSync { BAKER, MUTEX };
int thread_mode;  // Storage ThreadSync value

// Lamport's bakery algorithm variables
bool *choosing;
int *number;
int N = 0;

// or

// Mutex
std::mutex mtx;

struct thread_info {
    int thread_idx;
    int foreground;
    char key;
};

void print_colorize_char(int fg, char key)
{
    printf("\033[1;%dm%c\033[0m", fg, key);
}

void sleep_ms(int ms)
{
    std::this_thread::sleep_for(std::chrono::milliseconds(ms));
}

void lock(int id)
{
    switch(static_cast<ThreadSync>(thread_mode))
    {
        case BAKER:
            choosing[id] = true;
            number[id] = *std::max_element(number, number + N) + 1;
            choosing[id] = false;
            for (int j = 0; j < N; j++)
            {
                while(choosing[j]) {}
                while(
                    number[j] != 0 &&
                    (number[id] > number[j] || (
                        number[id] == number[j] && id > j))) {}
            }
            break;

        case MUTEX:
            mtx.lock();
            break;
    }

}

void unlock(int id)
{
    switch(static_cast<ThreadSync>(thread_mode))
    {
        case BAKER: number[id] = 0; break;
        case MUTEX: mtx.unlock();   break;
    }
}

static void *thread_function(void *ptr)
{
    struct thread_info *tinfo = (struct thread_info *)ptr;

    int thread_idx = tinfo->thread_idx;
    int fg = tinfo->foreground;
    char key = tinfo->key;

    lock(thread_idx);
    for(int i = 0; i < 10; i++)
    {
        printf("Thread %d: ", thread_idx + 1);  // Print thread number
        print_colorize_char(fg, key);  // Colorize char output
        std::cout << std::endl;
        str.push_back(key);  // Strcat(str, key);
        sleep_ms(10);  // Sleep(1000)
    }
    unlock(thread_idx);
}

int main(int argc, char ** argv)
{
    int s;
    int num_threads = argc > 1 ? atoi(argv[1]) : 3;
    thread_mode = int(argc > 2 && std::string(argv[2]) == "mutex" ? MUTEX : BAKER);

    // Init variables for algorithm
    N = num_threads;
    choosing = new bool[num_threads];
    number = new int[num_threads];

    str.reserve(num_threads * 10);  // Resorve memory for string

    pthread_t thread_ids[num_threads];
    struct thread_info *tinfo = new struct thread_info[num_threads];

    // Create threads and set thread structure
    for (int i = 0; i < num_threads; i++)
    {
        tinfo[i].thread_idx = i;
        tinfo[i].foreground = foreground_codes[i];  // Foreground
        tinfo[i].key = 65 + i;  // Keys begin with the letter A
        s = pthread_create(&thread_ids[i], NULL, &thread_function, &tinfo[i]);
        if (s != 0)
            exit(1);
    }

    // Wait until thread are done
    for (int i = 0; i < num_threads; i++)
    {
        s = pthread_join(thread_ids[i], NULL);
        if (s != 0)
            exit(1);
    }

    // Finally string by threads output
    for (int i = 0; i < num_threads; i++)
    {
        std::string substr = str.substr(i * 10, 10);
        for (int j = 0; j < 10; j++)
        {
            char c = substr[j];
            int fg = foreground_codes[c - 65];
            print_colorize_char(fg, c);
        }
        std::cout << std::endl;
    }

    exit(0);
}