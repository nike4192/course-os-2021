
#include <iostream>
#include <string.h>
#include <pthread.h>
#include <stdlib.h>

static void *thread_function(void *ptr)
{
    char *message = (char *)ptr;

    printf("%s\n", message);

    for (char *p = message; *p != '\0'; p++)
        *p = toupper(*p);
}


int main(int argc, char ** argv)
{

    // Init variables
    pthread_t thread1, thread2;
    char message1[] = "Thread 1";
    char message2[] = "Thread 2";
    int iret1, iret2;

    // Create threads
    iret1 = pthread_create( &thread1, NULL, thread_function, (void *)message1);
    iret2 = pthread_create( &thread2, NULL, thread_function, (void *)message2);

    // Wait until threads are done
    pthread_join( thread1, NULL );
    pthread_join( thread2, NULL );

    std::cout << "Wait until threads are done" << std::endl;

    // Print returned values
    std::cout << message1 << std::endl;
    std::cout << message2 << std::endl;

    exit(0);

}