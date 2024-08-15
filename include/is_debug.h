#ifndef ISVIEWER_H
#define ISVIEWER_H

#include "ultra64.h"
#include "attributes.h"

#if OOT_DEBUG
void isPrintfInit(void);
#endif

void isPrintf(const char* fmt, ...);
void osSyncPrintf(const char* fmt, ...);
void rmonPrintf(const char* fmt, ...);

#if OOT_DEBUG
void* is_proutSyncPrintf(void* arg, const char* str, size_t count);
NORETURN void isAssertFail(const char* exp, const char* file, int line);
#endif

#endif
