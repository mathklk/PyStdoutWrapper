#include <iostream>
#include <unistd.h>

int main(void)
{
    long long int i = 0;
    while (true) {
        std::cout << i++ << std::endl;
        sleep(1);
    }
}