/**
 * Sfx Item Bank
 *
 * DEFINE_SFX should be used for all sfx define in the item bank from sequence 0
 *    - Argument 0: Channel name for sequence 0
 *    - Argument 1: Enum value for this sfx
 *    - Argument 2: Importance for deciding which sfx to prioritize. Higher values have greater importance
 *    - Argument 3: Slows the decay of volume with distance (a 2-bit number ranging from 0-3)
 *    - Argument 4: Applies increasingly random offsets to frequency (a 2-bit number ranging from 0-3)
 *    - Argument 5: Various flags to add properties to the sfx
 */
/* 0x1800 */ DEFINE_SFX(CHAN_0F83, NA_SE_IT_SWORD_IMPACT, 0x30, 0, 1, SFX_FLAG_15)
/* 0x1801 */ DEFINE_SFX(CHAN_0F8D, NA_SE_IT_SWORD_SWING, 0x30, 0, 1, 0)
/* 0x1802 */ DEFINE_SFX(CHAN_0F9B, NA_SE_IT_SWORD_PUTAWAY, 0x30, 0, 0, 0)
/* 0x1803 */ DEFINE_SFX(CHAN_0FA5, NA_SE_IT_SWORD_PICKOUT, 0x30, 0, 0, 0)
/* 0x1804 */ DEFINE_SFX(CHAN_0FAF, NA_SE_IT_ARROW_SHOT, 0x30, 0, 1, SFX_FLAG_10)
/* 0x1805 */ DEFINE_SFX(CHAN_0FB9, NA_SE_IT_BOOMERANG_THROW, 0x30, 0, 1, SFX_FLAG_10)
/* 0x1806 */ DEFINE_SFX(CHAN_0FCB, NA_SE_IT_SHIELD_BOUND, 0x60, 3, 2, 0)
/* 0x1807 */ DEFINE_SFX(CHAN_0FDB, NA_SE_IT_BOW_DRAW, 0x30, 0, 1, SFX_FLAG_10)
/* 0x1808 */ DEFINE_SFX(CHAN_0FE9, NA_SE_IT_SHIELD_REFLECT_SW, 0x80, 3, 1, 0)
/* 0x1809 */ DEFINE_SFX(CHAN_1001, NA_SE_IT_ARROW_STICK_HRAD, 0x30, 0, 0, 0)
/* 0x180A */ DEFINE_SFX(CHAN_100B, NA_SE_IT_HAMMER_HIT, 0x30, 0, 1, 0)
/* 0x180B */ DEFINE_SFX(CHAN_1022, NA_SE_IT_HOOKSHOT_CHAIN, 0x30, 0, 0, SFX_FLAG_10)
/* 0x180C */ DEFINE_SFX(CHAN_103A, NA_SE_IT_SHIELD_REFLECT_MG, 0x30, 1, 0, SFX_FLAG_10)
/* 0x180D */ DEFINE_SFX(CHAN_106A, NA_SE_IT_BOMB_IGNIT, 0x50, 0, 0, 0)
/* 0x180E */ DEFINE_SFX(CHAN_1076, NA_SE_IT_BOMB_EXPLOSION, 0x90, 2, 0, 0)
/* 0x180F */ DEFINE_SFX(CHAN_1085, NA_SE_IT_BOMB_UNEXPLOSION, 0x50, 2, 0, 0)
/* 0x1810 */ DEFINE_SFX(CHAN_10A2, NA_SE_IT_BOOMERANG_FLY, 0x30, 0, 0, SFX_FLAG_10)
/* 0x1811 */ DEFINE_SFX(CHAN_10D2, NA_SE_IT_SWORD_STRIKE, 0x40, 2, 0, 0)
/* 0x1812 */ DEFINE_SFX(CHAN_10E6, NA_SE_IT_HAMMER_SWING, 0x30, 0, 1, 0)
#if AUDIO_LIBRARY_VERSION < 3
/* 0x1813 */ DEFINE_SFX(CHAN_10F4, NA_SE_IT_HOOKSHOT_REFLECT, 0x30, 0, 0, 0)
#else
/* 0x1813 */ DEFINE_SFX(CHAN_10F4, NA_SE_IT_HOOKSHOT_REFLECT, 0x20, 0, 0, 0)
#endif
/* 0x1814 */ DEFINE_SFX(CHAN_110B, NA_SE_IT_ARROW_STICK_CRE, 0x30, 0, 0, 0)
/* 0x1815 */ DEFINE_SFX(CHAN_1120, NA_SE_IT_ARROW_STICK_OBJ, 0x34, 0, 0, 0)
/* 0x1816 */ DEFINE_SFX(CHAN_1123, NA_SE_IT_DUMMY, 0x30, 0, 0, 0)
/* 0x1817 */ DEFINE_SFX(CHAN_1146, NA_SE_IT_DUMMY2, 0x30, 0, 0, 0)
/* 0x1818 */ DEFINE_SFX(CHAN_1169, NA_SE_IT_SWORD_SWING_HARD, 0x30, 0, 0, 0)
/* 0x1819 */ DEFINE_SFX(CHAN_1E10, NA_SE_IT_DUMMY3, 0x30, 0, 0, 0)
/* 0x181A */ DEFINE_SFX(CHAN_1187, NA_SE_IT_WALL_HIT_HARD, 0x40, 0, 0, 0)
/* 0x181B */ DEFINE_SFX(CHAN_119A, NA_SE_IT_WALL_HIT_SOFT, 0x30, 0, 0, 0)
/* 0x181C */ DEFINE_SFX(CHAN_11B3, NA_SE_IT_STONE_HIT, 0x30, 0, 0, 0)
/* 0x181D */ DEFINE_SFX(CHAN_11C4, NA_SE_IT_WOODSTICK_BROKEN, 0x30, 0, 0, 0)
/* 0x181E */ DEFINE_SFX(CHAN_11D5, NA_SE_IT_LASH, 0x30, 0, 2, 0)
/* 0x181F */ DEFINE_SFX(CHAN_11E8, NA_SE_IT_SHIELD_POSTURE, 0x30, 0, 1, 0)
/* 0x1820 */ DEFINE_SFX(CHAN_1208, NA_SE_IT_SLING_SHOT, 0x30, 0, 0, SFX_FLAG_10)
/* 0x1821 */ DEFINE_SFX(CHAN_1216, NA_SE_IT_SLING_DRAW, 0x20, 0, 0, SFX_FLAG_10)
/* 0x1822 */ DEFINE_SFX(CHAN_1224, NA_SE_IT_SWORD_CHARGE, 0x30, 0, 0, 0)
/* 0x1823 */ DEFINE_SFX(CHAN_125A, NA_SE_IT_ROLLING_CUT, 0x30, 0, 0, 0)
/* 0x1824 */ DEFINE_SFX(CHAN_1271, NA_SE_IT_SWORD_STRIKE_HARD, 0x30, 0, 0, 0)
/* 0x1825 */ DEFINE_SFX(CHAN_128A, NA_SE_IT_SLING_REFLECT, 0x30, 0, 0, 0)
/* 0x1826 */ DEFINE_SFX(CHAN_12A0, NA_SE_IT_SHIELD_REMOVE, 0x30, 0, 0, 0)
/* 0x1827 */ DEFINE_SFX(CHAN_12C0, NA_SE_IT_HOOKSHOT_READY, 0x30, 0, 0, SFX_FLAG_10)
/* 0x1828 */ DEFINE_SFX(CHAN_12DA, NA_SE_IT_HOOKSHOT_RECEIVE, 0x30, 0, 0, SFX_FLAG_10)
/* 0x1829 */ DEFINE_SFX(CHAN_12F4, NA_SE_IT_HOOKSHOT_STICK_OBJ, 0x60, 3, 1, 0)
/* 0x182A */ DEFINE_SFX(CHAN_1316, NA_SE_IT_SWORD_REFLECT_MG, 0x30, 1, 0, 0)
/* 0x182B */ DEFINE_SFX(CHAN_132D, NA_SE_IT_DEKU, 0x30, 1, 0, SFX_FLAG_10)
/* 0x182C */ DEFINE_SFX(CHAN_1350, NA_SE_IT_WALL_HIT_BUYO, 0x30, 0, 0, 0)
/* 0x182D */ DEFINE_SFX(CHAN_1396, NA_SE_IT_SWORD_PUTAWAY_STN, 0x30, 0, 0, 0)
/* 0x182E */ DEFINE_SFX(CHAN_13A7, NA_SE_IT_ROLLING_CUT_LV1, 0xA0, 2, 0, 0)
/* 0x182F */ DEFINE_SFX(CHAN_13CA, NA_SE_IT_ROLLING_CUT_LV2, 0xA0, 2, 0, 0)
/* 0x1830 */ DEFINE_SFX(CHAN_13E8, NA_SE_IT_BOW_FLICK, 0x30, 0, 0, SFX_FLAG_10)
/* 0x1831 */ DEFINE_SFX(CHAN_13FE, NA_SE_IT_BOMBCHU_MOVE, 0x30, 0, 0, 0)
/* 0x1832 */ DEFINE_SFX(CHAN_1411, NA_SE_IT_SHIELD_CHARGE_LV1, 0x60, 0, 0, 0)
/* 0x1833 */ DEFINE_SFX(CHAN_145D, NA_SE_IT_SHIELD_CHARGE_LV2, 0x60, 0, 0, 0)
/* 0x1834 */ DEFINE_SFX(CHAN_1462, NA_SE_IT_SHIELD_CHARGE_LV3, 0x60, 0, 0, 0)
/* 0x1835 */ DEFINE_SFX(CHAN_1467, NA_SE_IT_SLING_FLICK, 0x30, 0, 0, SFX_FLAG_10)
/* 0x1836 */ DEFINE_SFX(CHAN_147C, NA_SE_IT_SWORD_STICK_STN, 0x30, 0, 0, 0)
/* 0x1837 */ DEFINE_SFX(CHAN_1493, NA_SE_IT_REFLECTION_WOOD, 0x60, 1, 2, 0)
/* 0x1838 */ DEFINE_SFX(CHAN_14B0, NA_SE_IT_SHIELD_REFLECT_MG2, 0x30, 0, 0, 0)
/* 0x1839 */ DEFINE_SFX(CHAN_14B9, NA_SE_IT_MAGIC_ARROW_SHOT, 0x30, 0, 0, 0)
/* 0x183A */ DEFINE_SFX(CHAN_14CA, NA_SE_IT_EXPLOSION_FRAME, 0x60, 3, 0, SFX_FLAG_15)
/* 0x183B */ DEFINE_SFX(CHAN_14E5, NA_SE_IT_EXPLOSION_ICE, 0x60, 3, 0, SFX_FLAG_15)
/* 0x183C */ DEFINE_SFX(CHAN_14F6, NA_SE_IT_EXPLOSION_LIGHT, 0x60, 3, 0, SFX_FLAG_15)
/* 0x183D */ DEFINE_SFX(CHAN_1505, NA_SE_IT_FISHING_REEL_SLOW, 0x30, 0, 0, SFX_FLAG_14)
/* 0x183E */ DEFINE_SFX(CHAN_1510, NA_SE_IT_FISHING_REEL_HIGH, 0x30, 0, 0, SFX_FLAG_14)
/* 0x183F */ DEFINE_SFX(CHAN_0FDB, NA_SE_IT_PULL_FISHING_ROD, 0x30, 0, 1, 0)
/* 0x1840 */ DEFINE_SFX(CHAN_151B, NA_SE_IT_DM_FLYING_GOD_PASS, 0x80, 3, 0, 0)
/* 0x1841 */ DEFINE_SFX(CHAN_154A, NA_SE_IT_DM_FLYING_GOD_DASH, 0x80, 3, 0, 0)
/* 0x1842 */ DEFINE_SFX(CHAN_157D, NA_SE_IT_DM_RING_EXPLOSION, 0x30, 3, 0, 0)
/* 0x1843 */ DEFINE_SFX(CHAN_15BB, NA_SE_IT_DM_RING_GATHER, 0x30, 0, 0, 0)
/* 0x1844 */ DEFINE_SFX(CHAN_190A, NA_SE_IT_INGO_HORSE_NEIGH, 0x30, 0, 1, 0)
/* 0x1845 */ DEFINE_SFX(CHAN_15BB, NA_SE_IT_EARTHQUAKE, 0x30, 0, 0, 0)
/* 0x1846 */ DEFINE_SFX(CHAN_15D0, NA_SE_IT_DUMMY4, 0x30, 0, 0, 0)
/* 0x1847 */ DEFINE_SFX(CHAN_15DF, NA_SE_IT_KAKASHI_JUMP, 0x30, 0, 0, 0)
/* 0x1848 */ DEFINE_SFX(CHAN_15F3, NA_SE_IT_FLAME, 0x30, 0, 0, 0)
/* 0x1849 */ DEFINE_SFX(CHAN_2848, NA_SE_IT_SHIELD_BEAM, 0x30, 0, 0, 0)
/* 0x184A */ DEFINE_SFX(CHAN_15FA, NA_SE_IT_FISHING_HIT, 0x30, 0, 0, 0)
/* 0x184B */ DEFINE_SFX(CHAN_1617, NA_SE_IT_GOODS_APPEAR, 0x30, 0, 0, 0)
/* 0x184C */ DEFINE_SFX(CHAN_1624, NA_SE_IT_MAJIN_SWORD_BROKEN, 0x80, 0, 0, 0)
/* 0x184D */ DEFINE_SFX(CHAN_163E, NA_SE_IT_HAND_CLAP, 0x30, 0, 0, 0)
/* 0x184E */ DEFINE_SFX(CHAN_1648, NA_SE_IT_MASTER_SWORD_SWING, 0x30, 0, 0, 0)
/* 0x184F */ DEFINE_SFX(CHAN_1085, NA_SE_IT_DUMMY5, 0x30, 0, 0, 0)
