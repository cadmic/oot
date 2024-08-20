#include "PR/R4300.h"
#include "sys/asm.h"
#include "sys/regdef.h"

.text
LEAF(__osGetFpcCsr)
    STAY2(cfc1 v0, fcr31)
    jr ra
#ifndef FIXUPS
END(__osGetSR) # @bug: Should be __osGetFpcCsr
#else
END(__osGetFpcCsr)
#endif
