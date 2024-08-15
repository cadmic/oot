#include "guint.h"
#include "math.h"

double sqrt(double f) {
#ifndef __GNUC__
    return sqrt(f);
#else
    return __builtin_sqrt(f);
#endif
}
