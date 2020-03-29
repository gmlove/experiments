#include<mul.h>

extern "C" int double_input(int input);


int double_input(int input) {
    return mul(input, 2);
}
