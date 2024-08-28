#include "global.h"
#include "ultra64/leo.h"
#include "ultra64/leoappli.h"
#include "ultra64/leodrive.h"

void leoC2_single_ecc(void);
void leoC2_double_ecc(void);
void leoC2_3_ecc(void);
void leoC2_4_ecc(void);
s32 leoAlpha_mult(s32 i, s32 k);
s32 leoAlpha_div(s32 i, s32 k);

extern u8 LEO_TempBuffer[0xE8];

const u8 ganlog[512] = {
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1D, 0x3A, 0x74, 0xE8, 0xCD, 0x87, 0x13, 0x26, 0x4C, 0x98, 0x2D,
    0x5A, 0xB4, 0x75, 0xEA, 0xC9, 0x8F, 0x03, 0x06, 0x0C, 0x18, 0x30, 0x60, 0xC0, 0x9D, 0x27, 0x4E, 0x9C, 0x25, 0x4A,
    0x94, 0x35, 0x6A, 0xD4, 0xB5, 0x77, 0xEE, 0xC1, 0x9F, 0x23, 0x46, 0x8C, 0x05, 0x0A, 0x14, 0x28, 0x50, 0xA0, 0x5D,
    0xBA, 0x69, 0xD2, 0xB9, 0x6F, 0xDE, 0xA1, 0x5F, 0xBE, 0x61, 0xC2, 0x99, 0x2F, 0x5E, 0xBC, 0x65, 0xCA, 0x89, 0x0F,
    0x1E, 0x3C, 0x78, 0xF0, 0xFD, 0xE7, 0xD3, 0xBB, 0x6B, 0xD6, 0xB1, 0x7F, 0xFE, 0xE1, 0xDF, 0xA3, 0x5B, 0xB6, 0x71,
    0xE2, 0xD9, 0xAF, 0x43, 0x86, 0x11, 0x22, 0x44, 0x88, 0x0D, 0x1A, 0x34, 0x68, 0xD0, 0xBD, 0x67, 0xCE, 0x81, 0x1F,
    0x3E, 0x7C, 0xF8, 0xED, 0xC7, 0x93, 0x3B, 0x76, 0xEC, 0xC5, 0x97, 0x33, 0x66, 0xCC, 0x85, 0x17, 0x2E, 0x5C, 0xB8,
    0x6D, 0xDA, 0xA9, 0x4F, 0x9E, 0x21, 0x42, 0x84, 0x15, 0x2A, 0x54, 0xA8, 0x4D, 0x9A, 0x29, 0x52, 0xA4, 0x55, 0xAA,
    0x49, 0x92, 0x39, 0x72, 0xE4, 0xD5, 0xB7, 0x73, 0xE6, 0xD1, 0xBF, 0x63, 0xC6, 0x91, 0x3F, 0x7E, 0xFC, 0xE5, 0xD7,
    0xB3, 0x7B, 0xF6, 0xF1, 0xFF, 0xE3, 0xDB, 0xAB, 0x4B, 0x96, 0x31, 0x62, 0xC4, 0x95, 0x37, 0x6E, 0xDC, 0xA5, 0x57,
    0xAE, 0x41, 0x82, 0x19, 0x32, 0x64, 0xC8, 0x8D, 0x07, 0x0E, 0x1C, 0x38, 0x70, 0xE0, 0xDD, 0xA7, 0x53, 0xA6, 0x51,
    0xA2, 0x59, 0xB2, 0x79, 0xF2, 0xF9, 0xEF, 0xC3, 0x9B, 0x2B, 0x56, 0xAC, 0x45, 0x8A, 0x09, 0x12, 0x24, 0x48, 0x90,
    0x3D, 0x7A, 0xF4, 0xF5, 0xF7, 0xF3, 0xFB, 0xEB, 0xCB, 0x8B, 0x0B, 0x16, 0x2C, 0x58, 0xB0, 0x7D, 0xFA, 0xE9, 0xCF,
    0x83, 0x1B, 0x36, 0x6C, 0xD8, 0xAD, 0x47, 0x8E, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1D, 0x3A, 0x74,
    0xE8, 0xCD, 0x87, 0x13, 0x26, 0x4C, 0x98, 0x2D, 0x5A, 0xB4, 0x75, 0xEA, 0xC9, 0x8F, 0x03, 0x06, 0x0C, 0x18, 0x30,
    0x60, 0xC0, 0x9D, 0x27, 0x4E, 0x9C, 0x25, 0x4A, 0x94, 0x35, 0x6A, 0xD4, 0xB5, 0x77, 0xEE, 0xC1, 0x9F, 0x23, 0x46,
    0x8C, 0x05, 0x0A, 0x14, 0x28, 0x50, 0xA0, 0x5D, 0xBA, 0x69, 0xD2, 0xB9, 0x6F, 0xDE, 0xA1, 0x5F, 0xBE, 0x61, 0xC2,
    0x99, 0x2F, 0x5E, 0xBC, 0x65, 0xCA, 0x89, 0x0F, 0x1E, 0x3C, 0x78, 0xF0, 0xFD, 0xE7, 0xD3, 0xBB, 0x6B, 0xD6, 0xB1,
    0x7F, 0xFE, 0xE1, 0xDF, 0xA3, 0x5B, 0xB6, 0x71, 0xE2, 0xD9, 0xAF, 0x43, 0x86, 0x11, 0x22, 0x44, 0x88, 0x0D, 0x1A,
    0x34, 0x68, 0xD0, 0xBD, 0x67, 0xCE, 0x81, 0x1F, 0x3E, 0x7C, 0xF8, 0xED, 0xC7, 0x93, 0x3B, 0x76, 0xEC, 0xC5, 0x97,
    0x33, 0x66, 0xCC, 0x85, 0x17, 0x2E, 0x5C, 0xB8, 0x6D, 0xDA, 0xA9, 0x4F, 0x9E, 0x21, 0x42, 0x84, 0x15, 0x2A, 0x54,
    0xA8, 0x4D, 0x9A, 0x29, 0x52, 0xA4, 0x55, 0xAA, 0x49, 0x92, 0x39, 0x72, 0xE4, 0xD5, 0xB7, 0x73, 0xE6, 0xD1, 0xBF,
    0x63, 0xC6, 0x91, 0x3F, 0x7E, 0xFC, 0xE5, 0xD7, 0xB3, 0x7B, 0xF6, 0xF1, 0xFF, 0xE3, 0xDB, 0xAB, 0x4B, 0x96, 0x31,
    0x62, 0xC4, 0x95, 0x37, 0x6E, 0xDC, 0xA5, 0x57, 0xAE, 0x41, 0x82, 0x19, 0x32, 0x64, 0xC8, 0x8D, 0x07, 0x0E, 0x1C,
    0x38, 0x70, 0xE0, 0xDD, 0xA7, 0x53, 0xA6, 0x51, 0xA2, 0x59, 0xB2, 0x79, 0xF2, 0xF9, 0xEF, 0xC3, 0x9B, 0x2B, 0x56,
    0xAC, 0x45, 0x8A, 0x09, 0x12, 0x24, 0x48, 0x90, 0x3D, 0x7A, 0xF4, 0xF5, 0xF7, 0xF3, 0xFB, 0xEB, 0xCB, 0x8B, 0x0B,
    0x16, 0x2C, 0x58, 0xB0, 0x7D, 0xFA, 0xE9, 0xCF, 0x83, 0x1B, 0x36, 0x6C, 0xD8, 0xAD, 0x47, 0x8E, 0x01, 0x02
};

const u8 glog[512] = {
    0x00, 0x00, 0x01, 0x19, 0x02, 0x32, 0x1A, 0xC6, 0x03, 0xDF, 0x33, 0xEE, 0x1B, 0x68, 0xC7, 0x4B, 0x04, 0x64, 0xE0,
    0x0E, 0x34, 0x8D, 0xEF, 0x81, 0x1C, 0xC1, 0x69, 0xF8, 0xC8, 0x08, 0x4C, 0x71, 0x05, 0x8A, 0x65, 0x2F, 0xE1, 0x24,
    0x0F, 0x21, 0x35, 0x93, 0x8E, 0xDA, 0xF0, 0x12, 0x82, 0x45, 0x1D, 0xB5, 0xC2, 0x7D, 0x6A, 0x27, 0xF9, 0xB9, 0xC9,
    0x9A, 0x09, 0x78, 0x4D, 0xE4, 0x72, 0xA6, 0x06, 0xBF, 0x8B, 0x62, 0x66, 0xDD, 0x30, 0xFD, 0xE2, 0x98, 0x25, 0xB3,
    0x10, 0x91, 0x22, 0x88, 0x36, 0xD0, 0x94, 0xCE, 0x8F, 0x96, 0xDB, 0xBD, 0xF1, 0xD2, 0x13, 0x5C, 0x83, 0x38, 0x46,
    0x40, 0x1E, 0x42, 0xB6, 0xA3, 0xC3, 0x48, 0x7E, 0x6E, 0x6B, 0x3A, 0x28, 0x54, 0xFA, 0x85, 0xBA, 0x3D, 0xCA, 0x5E,
    0x9B, 0x9F, 0x0A, 0x15, 0x79, 0x2B, 0x4E, 0xD4, 0xE5, 0xAC, 0x73, 0xF3, 0xA7, 0x57, 0x07, 0x70, 0xC0, 0xF7, 0x8C,
    0x80, 0x63, 0x0D, 0x67, 0x4A, 0xDE, 0xED, 0x31, 0xC5, 0xFE, 0x18, 0xE3, 0xA5, 0x99, 0x77, 0x26, 0xB8, 0xB4, 0x7C,
    0x11, 0x44, 0x92, 0xD9, 0x23, 0x20, 0x89, 0x2E, 0x37, 0x3F, 0xD1, 0x5B, 0x95, 0xBC, 0xCF, 0xCD, 0x90, 0x87, 0x97,
    0xB2, 0xDC, 0xFC, 0xBE, 0x61, 0xF2, 0x56, 0xD3, 0xAB, 0x14, 0x2A, 0x5D, 0x9E, 0x84, 0x3C, 0x39, 0x53, 0x47, 0x6D,
    0x41, 0xA2, 0x1F, 0x2D, 0x43, 0xD8, 0xB7, 0x7B, 0xA4, 0x76, 0xC4, 0x17, 0x49, 0xEC, 0x7F, 0x0C, 0x6F, 0xF6, 0x6C,
    0xA1, 0x3B, 0x52, 0x29, 0x9D, 0x55, 0xAA, 0xFB, 0x60, 0x86, 0xB1, 0xBB, 0xCC, 0x3E, 0x5A, 0xCB, 0x59, 0x5F, 0xB0,
    0x9C, 0xA9, 0xA0, 0x51, 0x0B, 0xF5, 0x16, 0xEB, 0x7A, 0x75, 0x2C, 0xD7, 0x4F, 0xAE, 0xD5, 0xE9, 0xE6, 0xE7, 0xAD,
    0xE8, 0x74, 0xD6, 0xF4, 0xEA, 0xA8, 0x50, 0x58, 0xAF, 0xFF, 0x01, 0x19, 0x02, 0x32, 0x1A, 0xC6, 0x03, 0xDF, 0x33,
    0xEE, 0x1B, 0x68, 0xC7, 0x4B, 0x04, 0x64, 0xE0, 0x0E, 0x34, 0x8D, 0xEF, 0x81, 0x1C, 0xC1, 0x69, 0xF8, 0xC8, 0x08,
    0x4C, 0x71, 0x05, 0x8A, 0x65, 0x2F, 0xE1, 0x24, 0x0F, 0x21, 0x35, 0x93, 0x8E, 0xDA, 0xF0, 0x12, 0x82, 0x45, 0x1D,
    0xB5, 0xC2, 0x7D, 0x6A, 0x27, 0xF9, 0xB9, 0xC9, 0x9A, 0x09, 0x78, 0x4D, 0xE4, 0x72, 0xA6, 0x06, 0xBF, 0x8B, 0x62,
    0x66, 0xDD, 0x30, 0xFD, 0xE2, 0x98, 0x25, 0xB3, 0x10, 0x91, 0x22, 0x88, 0x36, 0xD0, 0x94, 0xCE, 0x8F, 0x96, 0xDB,
    0xBD, 0xF1, 0xD2, 0x13, 0x5C, 0x83, 0x38, 0x46, 0x40, 0x1E, 0x42, 0xB6, 0xA3, 0xC3, 0x48, 0x7E, 0x6E, 0x6B, 0x3A,
    0x28, 0x54, 0xFA, 0x85, 0xBA, 0x3D, 0xCA, 0x5E, 0x9B, 0x9F, 0x0A, 0x15, 0x79, 0x2B, 0x4E, 0xD4, 0xE5, 0xAC, 0x73,
    0xF3, 0xA7, 0x57, 0x07, 0x70, 0xC0, 0xF7, 0x8C, 0x80, 0x63, 0x0D, 0x67, 0x4A, 0xDE, 0xED, 0x31, 0xC5, 0xFE, 0x18,
    0xE3, 0xA5, 0x99, 0x77, 0x26, 0xB8, 0xB4, 0x7C, 0x11, 0x44, 0x92, 0xD9, 0x23, 0x20, 0x89, 0x2E, 0x37, 0x3F, 0xD1,
    0x5B, 0x95, 0xBC, 0xCF, 0xCD, 0x90, 0x87, 0x97, 0xB2, 0xDC, 0xFC, 0xBE, 0x61, 0xF2, 0x56, 0xD3, 0xAB, 0x14, 0x2A,
    0x5D, 0x9E, 0x84, 0x3C, 0x39, 0x53, 0x47, 0x6D, 0x41, 0xA2, 0x1F, 0x2D, 0x43, 0xD8, 0xB7, 0x7B, 0xA4, 0x76, 0xC4,
    0x17, 0x49, 0xEC, 0x7F, 0x0C, 0x6F, 0xF6, 0x6C, 0xA1, 0x3B, 0x52, 0x29, 0x9D, 0x55, 0xAA, 0xFB, 0x60, 0x86, 0xB1,
    0xBB, 0xCC, 0x3E, 0x5A, 0xCB, 0x59, 0x5F, 0xB0, 0x9C, 0xA9, 0xA0, 0x51, 0x0B, 0xF5, 0x16, 0xEB, 0x7A, 0x75, 0x2C,
    0xD7, 0x4F, 0xAE, 0xD5, 0xE9, 0xE6, 0xE7, 0xAD, 0xE8, 0x74, 0xD6, 0xF4, 0xEA, 0xA8, 0x50, 0x58, 0xAF, 0xFF
};

block_param_form LEOc2_param;

s32 leoC2_Correction(void) {
    switch (LEOc2_param.err_num) {
        case 0:
            break;
        case 1:
            leoC2_single_ecc();
            break;
        case 2:
            leoC2_double_ecc();
            break;
        case 3:
            leoC2_3_ecc();
            break;
        case 4:
            leoC2_4_ecc();
            break;
        default:
            return 0xFFFF;
    }
    return 0;
}

// static
void leoC2_single_ecc(void) {
    u8* pointer;
    u32 byte;
    u8* p_s;

    if (LEOc2_param.err_pos[0] < 0x55) {
        byte = LEOc2_param.bytes;
        pointer = &LEOc2_param.pntr[(LEOc2_param.err_pos[0] + 1) * byte];
        p_s = LEOc2_param.c2buff_e;

        do {
            *(--pointer) ^= *(p_s -= 4);
        } while (--byte != 0);
    }
}

// static
void leoC2_double_ecc(void) {
    u32 s0;
    u32 error_k;
    u8* pointer1;
    u8* pointer2;
    u32 k;
    u32 m;
    u32 a;
    u32 d;
    u32 byte;
    u8* p_s;

    k = 0x58 - LEOc2_param.err_pos[0];
    m = 0x58 - LEOc2_param.err_pos[1];
    d = ganlog[k] ^ ganlog[m];
    d = glog[leoAlpha_div(1, d)];
    byte = LEOc2_param.bytes;

    if (LEOc2_param.err_pos[1] < 0x55) {
        goto c2_2_2;
    }
    pointer2 = &LEO_TempBuffer[sizeof(LEO_TempBuffer)];
    if (LEOc2_param.err_pos[0] < 0x55) {
        goto c2_2_1;
    }
    return;
c2_2_2:
    pointer2 = &LEOc2_param.pntr[(LEOc2_param.err_pos[1] + 1) * byte];
c2_2_1:
    pointer1 = &LEOc2_param.pntr[(LEOc2_param.err_pos[0] + 1) * byte];
    p_s = LEOc2_param.c2buff_e;

    do {
        p_s -= 4;
        s0 = p_s[0];
        if (s0 != 0) {
            a = ganlog[m + glog[s0]] ^ p_s[1];
        } else {
            a = p_s[1];
        }
        pointer1--;
        pointer2--;
        if (a != 0) {
            error_k = ganlog[glog[a] + d];
            *pointer1 ^= error_k;
            *pointer2 ^= error_k ^ s0;
        } else {
            *pointer2 ^= s0;
        }
    } while (--byte != 0);
}

// static
void leoC2_3_ecc(void) {
    u32 s0;
    u32 error_i;
    u32 error_j;
    u32 error_k;
    u8* pointer1;
    u8* pointer2;
    u8* pointer3;
    u32 byte;
    u32 ii;
    u32 jj;
    u32 kk;
    u32 c;
    u32 f;
    u32 o;
    u32 b;
    u32 d;
    u32 h;
    u32 a;
    u32 e;
    u32 g;
    u32 p;
    u8* p_s;

    ii = 0x58 - LEOc2_param.err_pos[0];
    jj = 0x58 - LEOc2_param.err_pos[1];
    kk = 0x58 - LEOc2_param.err_pos[2];
    ii = ganlog[ii];
    jj = ganlog[jj];
    kk = ganlog[kk];
    c = leoAlpha_mult(kk, kk);
    f = leoAlpha_mult(jj, jj);
    o = leoAlpha_mult(ii, ii);
    b = c ^ f;
    d = c ^ o;
    h = f ^ o;
    a = leoAlpha_mult(jj, c) ^ leoAlpha_mult(kk, f);
    e = leoAlpha_mult(kk, o) ^ leoAlpha_mult(ii, c);
    g = leoAlpha_mult(jj, o) ^ leoAlpha_mult(ii, f);
    c = jj ^ kk;
    f = kk ^ ii;
    o = ii ^ jj;
    p = a ^ e ^ g;
    p = leoAlpha_div(1, p);
    a = glog[a];
    b = glog[b];
    c = glog[c];
    d = glog[d];
    e = glog[e];
    f = glog[f];
    g = glog[g];
    h = glog[h];
    o = glog[o];
    p = glog[p];
    byte = LEOc2_param.bytes;
    if (LEOc2_param.err_pos[2] < 0x55) {
        goto c2_3_3;
    }
    pointer3 = &LEO_TempBuffer[sizeof(LEO_TempBuffer)];
    if (LEOc2_param.err_pos[1] < 0x55) {
        goto c2_3_2;
    }
    pointer2 = &LEO_TempBuffer[sizeof(LEO_TempBuffer)];
    if (LEOc2_param.err_pos[0] < 0x55) {
        goto c2_3_1;
    }
    return;
c2_3_3:
    pointer3 = &LEOc2_param.pntr[(LEOc2_param.err_pos[2] + 1) * byte];
c2_3_2:
    pointer2 = &LEOc2_param.pntr[(LEOc2_param.err_pos[1] + 1) * byte];
c2_3_1:
    pointer1 = &LEOc2_param.pntr[(LEOc2_param.err_pos[0] + 1) * byte];
    p_s = LEOc2_param.c2buff_e;

    do {
        p_s -= 4;
        s0 = p_s[0];
        if (s0) {
            s0 = glog[s0];
            error_i = ganlog[s0 + a];
            error_j = ganlog[s0 + e];
            error_k = ganlog[s0 + g];
        } else {
            error_i = error_j = error_k = 0;
        }
        s0 = p_s[1];
        if (s0) {
            s0 = glog[s0];
            error_i ^= ganlog[s0 + b];
            error_j ^= ganlog[s0 + d];
            error_k ^= ganlog[s0 + h];
        }
        s0 = p_s[2];
        if (s0) {
            s0 = glog[s0];
            error_i ^= ganlog[s0 + c];
            error_j ^= ganlog[s0 + f];
            error_k ^= ganlog[s0 + o];
        }
        pointer1--;
        pointer2--;
        pointer3--;
        if (error_i) {
            *pointer1 ^= ganlog[glog[error_i] + p];
        }
        if (error_j) {
            *pointer2 ^= ganlog[glog[error_j] + p];
        }
        if (error_k) {
            *pointer3 ^= ganlog[glog[error_k] + p];
        }
    } while (--byte != 0);
}

// static
void leoC2_4_ecc(void) {
    u32 s0;
    u32 R0;
    u32 R1;
    u32 R2;
    u32 R3;
    u8* pointer1;
    u8* pointer2;
    u8* pointer3;
    u8* pointer4;
    u32 aa;
    u32 bb;
    u32 dd;
    u32 ee;
    u32 gg;
    u32 hh;
    u32 pp;
    u32 qq;
    u32 ll;
    u32 ii;
    u32 jj;
    u32 kk;
    u32 byte;
    u32 s;
    u32 a;
    u32 e;
    u32 g;
    u32 p;
    u32 c;
    u32 f;
    u32 o;
    u32 r;
    u32 t;
    u32 u;
    u32 v;
    u32 b;
    u32 d;
    u32 h;
    u32 q;
    u8* p_s;

    ii = 0x58 - LEOc2_param.err_pos[0];
    jj = 0x58 - LEOc2_param.err_pos[1];
    kk = 0x58 - LEOc2_param.err_pos[2];
    ll = 0x58 - LEOc2_param.err_pos[3];

    ii = ganlog[ii];
    jj = ganlog[jj];
    kk = ganlog[kk];
    ll = ganlog[ll];
    s = ganlog[0];

    aa = leoAlpha_div(s, ii);
    bb = leoAlpha_div(s, jj);
    ee = leoAlpha_div(s, kk);
    dd = leoAlpha_div(s, ll);

    a = leoAlpha_mult(bb, ee);
    e = leoAlpha_mult(ee, dd);
    g = leoAlpha_mult(dd, bb);
    p = leoAlpha_mult(dd, aa);
    c = leoAlpha_mult(aa, ee);
    f = leoAlpha_mult(aa, bb);

    b = a ^ e ^ g;
    d = e ^ p ^ c;
    h = p ^ f ^ g;
    q = f ^ a ^ c;
    a = bb ^ ee ^ dd;
    e = ee ^ dd ^ aa;
    g = dd ^ aa ^ bb;
    p = aa ^ bb ^ ee;

    c = leoAlpha_mult(leoAlpha_mult(bb, ee), dd);
    f = leoAlpha_mult(leoAlpha_mult(ee, dd), aa);
    o = leoAlpha_mult(leoAlpha_mult(dd, aa), bb);
    r = leoAlpha_mult(leoAlpha_mult(aa, bb), ee);

    s = leoAlpha_mult(leoAlpha_mult(leoAlpha_div(ii, jj) ^ 1, leoAlpha_div(ii, kk) ^ 1), leoAlpha_div(ii, ll) ^ 1);
    s = leoAlpha_div(1, s);
    t = leoAlpha_mult(leoAlpha_mult(leoAlpha_div(jj, ii) ^ 1, leoAlpha_div(jj, kk) ^ 1), leoAlpha_div(jj, ll) ^ 1);
    t = leoAlpha_div(1, t);
    u = leoAlpha_mult(leoAlpha_mult(leoAlpha_div(kk, ii) ^ 1, leoAlpha_div(kk, jj) ^ 1), leoAlpha_div(kk, ll) ^ 1);
    u = leoAlpha_div(1, u);
    v = leoAlpha_mult(leoAlpha_mult(leoAlpha_div(ll, ii) ^ 1, leoAlpha_div(ll, jj) ^ 1), leoAlpha_div(ll, kk) ^ 1);
    v = leoAlpha_div(1, v);

    aa = glog[leoAlpha_mult(a, s)];
    bb = glog[leoAlpha_mult(b, s)];
    c = leoAlpha_mult(c, s);
    ee = glog[leoAlpha_mult(e, t)];
    dd = glog[leoAlpha_mult(d, t)];
    f = leoAlpha_mult(f, t);
    gg = glog[leoAlpha_mult(g, u)];
    hh = glog[leoAlpha_mult(h, u)];
    o = leoAlpha_mult(o, u);
    pp = glog[leoAlpha_mult(p, v)];
    qq = glog[leoAlpha_mult(q, v)];
    r = leoAlpha_mult(r, v);

    s = glog[s];
    c = glog[c];
    t = glog[t];
    f = glog[f];
    u = glog[u];
    o = glog[o];
    v = glog[v];
    r = glog[r];

    byte = LEOc2_param.bytes;

    if (LEOc2_param.err_pos[3] < 0x55) {
        goto c2_4_4;
    }
    pointer4 = &LEO_TempBuffer[sizeof(LEO_TempBuffer)];
    if (LEOc2_param.err_pos[2] < 0x55) {
        goto c2_4_3;
    }
    pointer3 = &LEO_TempBuffer[sizeof(LEO_TempBuffer)];
    if (LEOc2_param.err_pos[1] < 0x55) {
        goto c2_4_2;
    }
    pointer2 = &LEO_TempBuffer[sizeof(LEO_TempBuffer)];
    if (LEOc2_param.err_pos[0] < 0x55) {
        goto c2_4_1;
    }
    return;

c2_4_4:
    pointer4 = &LEOc2_param.pntr[(LEOc2_param.err_pos[3] + 1) * byte];
c2_4_3:
    pointer3 = &LEOc2_param.pntr[(LEOc2_param.err_pos[2] + 1) * byte];
c2_4_2:
    pointer2 = &LEOc2_param.pntr[(LEOc2_param.err_pos[1] + 1) * byte];
c2_4_1:
    pointer1 = &LEOc2_param.pntr[(LEOc2_param.err_pos[0] + 1) * byte];
    p_s = LEOc2_param.c2buff_e;

    do {
        p_s -= 4;
        s0 = p_s[0];
        if (!s0) {
            R0 = R1 = R2 = R3 = 0;
        } else {
            s0 = glog[s0];
            R0 = ganlog[s0 + s];
            R1 = ganlog[s0 + t];
            R2 = ganlog[s0 + u];
            R3 = ganlog[s0 + v];
        }
        s0 = p_s[1];
        if (s0) {
            s0 = glog[s0];
            R0 ^= (!a) ? 0 : ganlog[s0 + aa];
            R1 ^= (!e) ? 0 : ganlog[s0 + ee];
            R2 ^= (!g) ? 0 : ganlog[s0 + gg];
            R3 ^= (!p) ? 0 : ganlog[s0 + pp];
        }
        s0 = p_s[2];
        if (s0) {
            s0 = glog[s0];
            R0 ^= (!b) ? 0 : ganlog[s0 + bb];
            R1 ^= (!d) ? 0 : ganlog[s0 + dd];
            R2 ^= (!h) ? 0 : ganlog[s0 + hh];
            R3 ^= (!q) ? 0 : ganlog[s0 + qq];
        }
        s0 = p_s[3];
        if (s0) {
            s0 = glog[s0];
            R0 ^= ganlog[s0 + c];
            R1 ^= ganlog[s0 + f];
            R2 ^= ganlog[s0 + o];
            R3 ^= ganlog[s0 + r];
        }
        pointer1--;
        pointer2--;
        pointer3--;
        pointer4--;
        if (R0) {
            *pointer1 ^= R0;
        }
        if (R1) {
            *pointer2 ^= R1;
        }
        if (R2) {
            *pointer3 ^= R2;
        }
        if (R3) {
            *pointer4 ^= R3;
        }
    } while (--byte != 0);
}

// static
s32 leoAlpha_mult(s32 i, s32 k) {
    if (i == 0 || k == 0) {
        return 0;
    }
    return ganlog[glog[i] + glog[k]];
}

// static
s32 leoAlpha_div(s32 i, s32 k) {
    if (i == 0 || k == 0) {
        return 0;
    }
    return ganlog[0xFF + (glog[i] - glog[k])];
}
