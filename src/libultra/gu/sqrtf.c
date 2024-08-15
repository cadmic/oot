#include "guint.h"
#include "math.h"

f32 sqrtf(f32 f) {
#ifndef __GNUC__
    return sqrtf(f);
#else
    return __builtin_sqrtf(f);
#endif
}
