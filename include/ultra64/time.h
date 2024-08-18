#ifndef ULTRA64_TIME_H
#define ULTRA64_TIME_H

#include "ultratypes.h"
#include "message.h"

typedef u64 OSTime;

typedef struct OSTimer {
    /* 0x00 */ struct OSTimer* next;
    /* 0x04 */ struct OSTimer* prev;
    /* 0x08 */ OSTime interval;
    /* 0x10 */ OSTime value;
    /* 0x18 */ OSMesgQueue* mq;
    /* 0x1C */ OSMesg msg;
} OSTimer; // size = 0x20

OSTime osGetTime(void);
void osSetTime(OSTime);
s32 osSetTimer(OSTimer*, OSTime, OSTime, OSMesgQueue*, OSMesg);
s32 osStopTimer(OSTimer*);

#endif
