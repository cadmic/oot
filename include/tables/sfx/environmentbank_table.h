/**
 * Sfx Environment Bank
 *
 * DEFINE_SFX should be used for all sfx define in the environment bank from sequence 0
 *    - Argument 1: Enum value for this sfx
 *    - Argument 2: Importance for deciding which sfx to prioritize. Higher values have greater importance
 *    - Argument 3: Slows the decay of volume with distance (a 2-bit number ranging from 0-3)
 *    - Argument 4: Applies increasingly random offsets to frequency (a 2-bit number ranging from 0-3)
 *    - Argument 5: Various flags to add properties to the sfx
 *
 * WARNING: entries must align with the table defined for the environment bank in sequence 0
 */
/* 0x2800 */ DEFINE_SFX(NA_SE_EV_DOOR_OPEN, 0x70, 0, 1, SFX_FLAG_10 | SFX_FLAG_9)
/* 0x2801 */ DEFINE_SFX(NA_SE_EV_DOOR_CLOSE, 0x80, 0, 1, 0)
/* 0x2802 */ DEFINE_SFX(NA_SE_EV_EXPLOSION, 0x30, 0, 0, 0)
/* 0x2803 */ DEFINE_SFX(NA_SE_EV_HORSE_WALK, 0x30, 0, 1, 0)
/* 0x2804 */ DEFINE_SFX(NA_SE_EV_HORSE_RUN, 0x30, 0, 1, 0)
/* 0x2805 */ DEFINE_SFX(NA_SE_EV_HORSE_NEIGH, 0x40, 0, 1, 0)
/* 0x2806 */ DEFINE_SFX(NA_SE_EV_RIVER_STREAM, 0x30, 0, 2, SFX_FLAG_10)
/* 0x2807 */ DEFINE_SFX(NA_SE_EV_WATER_WALL_BIG, 0x38, 2, 0, 0)
/* 0x2808 */ DEFINE_SFX(NA_SE_EV_OUT_OF_WATER, 0x30, 0, 1, 0)
/* 0x2809 */ DEFINE_SFX(NA_SE_EV_DIVE_WATER, 0x30, 0, 1, 0)
/* 0x280A */ DEFINE_SFX(NA_SE_EV_ROCK_SLIDE, 0x80, 2, 0, 0)
/* 0x280B */ DEFINE_SFX(NA_SE_EV_MAGMA_LEVEL, 0xA0, 3, 0, 0)
/* 0x280C */ DEFINE_SFX(NA_SE_EV_BRIDGE_OPEN, 0x30, 3, 0, 0)
/* 0x280D */ DEFINE_SFX(NA_SE_EV_BRIDGE_CLOSE, 0x30, 3, 0, 0)
/* 0x280E */ DEFINE_SFX(NA_SE_EV_BRIDGE_OPEN_STOP, 0x30, 3, 0, 0)
/* 0x280F */ DEFINE_SFX(NA_SE_EV_BRIDGE_CLOSE_STOP, 0x30, 3, 0, 0)
/* 0x2810 */ DEFINE_SFX(NA_SE_EV_WALL_BROKEN, 0x30, 2, 0, 0)
/* 0x2811 */ DEFINE_SFX(NA_SE_EV_CHICKEN_CRY_N, 0x30, 0, 1, 0)
/* 0x2812 */ DEFINE_SFX(NA_SE_EV_CHICKEN_CRY_A, 0x30, 0, 1, 0)
/* 0x2813 */ DEFINE_SFX(NA_SE_EV_CHICKEN_CRY_M, 0x30, 0, 0, 0)
/* 0x2814 */ DEFINE_SFX(NA_SE_EV_SLIDE_DOOR_OPEN, 0x60, 0, 0, 0)
/* 0x2815 */ DEFINE_SFX(NA_SE_EV_FOOT_SWITCH, 0x30, 3, 0, 0)
/* 0x2816 */ DEFINE_SFX(NA_SE_EV_HORSE_GROAN, 0x30, 0, 0, 0)
/* 0x2817 */ DEFINE_SFX(NA_SE_EV_BOMB_DROP_WATER, 0x30, 2, 2, 0)
/* 0x2818 */ DEFINE_SFX(NA_SE_EV_HORSE_JUMP, 0x30, 0, 0, 0)
/* 0x2819 */ DEFINE_SFX(NA_SE_EV_HORSE_LAND, 0x40, 0, 0, 0)
/* 0x281A */ DEFINE_SFX(NA_SE_EV_HORSE_SLIP, 0x38, 0, 0, 0)
/* 0x281B */ DEFINE_SFX(NA_SE_EV_FAIRY_DASH, 0x28, 0, 0, 0)
/* 0x281C */ DEFINE_SFX(NA_SE_EV_SLIDE_DOOR_CLOSE, 0x60, 0, 0, 0)
/* 0x281D */ DEFINE_SFX(NA_SE_EV_STONE_BOUND, 0x70, 3, 0, 0)
/* 0x281E */ DEFINE_SFX(NA_SE_EV_STONE_STATUE_OPEN, 0x30, 3, 0, 0)
/* 0x281F */ DEFINE_SFX(NA_SE_EV_TBOX_UNLOCK, 0x30, 0, 0, 0)
/* 0x2820 */ DEFINE_SFX(NA_SE_EV_TBOX_OPEN, 0x30, 0, 0, 0)
/* 0x2821 */ DEFINE_SFX(NA_SE_SY_TIMER, 0xA0, 0, 0, SFX_FLAG_13 | SFX_FLAG_3)
#if PLATFORM_N64
/* 0x2822 */ DEFINE_SFX(NA_SE_EV_FLAME_IGNITION, 0x2D, 2, 0, 0)
#else
/* 0x2822 */ DEFINE_SFX(NA_SE_EV_FLAME_IGNITION, 0x20, 2, 0, 0)
#endif
/* 0x2823 */ DEFINE_SFX(NA_SE_EV_SPEAR_HIT, 0x30, 0, 0, 0)
/* 0x2824 */ DEFINE_SFX(NA_SE_EV_ELEVATOR_MOVE, 0x30, 0, 0, SFX_FLAG_11)
/* 0x2825 */ DEFINE_SFX(NA_SE_EV_WARP_HOLE, 0x30, 0, 0, SFX_FLAG_15 | SFX_FLAG_11)
/* 0x2826 */ DEFINE_SFX(NA_SE_EV_LINK_WARP, 0x30, 0, 0, SFX_FLAG_15)
/* 0x2827 */ DEFINE_SFX(NA_SE_EV_PILLAR_SINK, 0x30, 2, 0, 0)
/* 0x2828 */ DEFINE_SFX(NA_SE_EV_WATER_WALL, 0x30, 0, 0, 0)
/* 0x2829 */ DEFINE_SFX(NA_SE_EV_RIVER_STREAM_S, 0x30, 0, 0, 0)
/* 0x282A */ DEFINE_SFX(NA_SE_EV_RIVER_STREAM_F, 0x30, 0, 0, 0)
/* 0x282B */ DEFINE_SFX(NA_SE_EV_HORSE_LAND2, 0x30, 0, 0, 0)
/* 0x282C */ DEFINE_SFX(NA_SE_EV_HORSE_SANDDUST, 0x30, 0, 0, SFX_FLAG_10)
/* 0x282D */ DEFINE_SFX(NA_SE_EV_DUMMY45, 0x30, 0, 0, 0)
/* 0x282E */ DEFINE_SFX(NA_SE_EV_LIGHTNING, 0x30, 0, 0, 0)
/* 0x282F */ DEFINE_SFX(NA_SE_EV_BOMB_BOUND, 0x30, 0, 2, 0)
/* 0x2830 */ DEFINE_SFX(NA_SE_EV_WATERDROP, 0x60, 2, 1, 0)
/* 0x2831 */ DEFINE_SFX(NA_SE_EV_TORCH, 0x10, 0, 0, 0)
/* 0x2832 */ DEFINE_SFX(NA_SE_EV_MAGMA_LEVEL_M, 0xA0, 3, 0, 0)
/* 0x2833 */ DEFINE_SFX(NA_SE_EV_FIRE_PILLAR, 0x30, 0, 0, 0)
/* 0x2834 */ DEFINE_SFX(NA_SE_EV_FIRE_PLATE, 0x30, 0, 0, SFX_FLAG_4)
/* 0x2835 */ DEFINE_SFX(NA_SE_EV_BLOCK_BOUND, 0x30, 3, 0, 0)
/* 0x2836 */ DEFINE_SFX(NA_SE_EV_METALDOOR_SLIDE, 0x30, 0, 0, 0)
/* 0x2837 */ DEFINE_SFX(NA_SE_EV_METALDOOR_STOP, 0x30, 0, 0, 0)
/* 0x2838 */ DEFINE_SFX(NA_SE_EV_BLOCK_SHAKE, 0x30, 0, 0, 0)
/* 0x2839 */ DEFINE_SFX(NA_SE_EV_BOX_BREAK, 0x30, 2, 0, 0)
/* 0x283A */ DEFINE_SFX(NA_SE_EV_HAMMER_SWITCH, 0x30, 0, 0, 0)
/* 0x283B */ DEFINE_SFX(NA_SE_EV_MAGMA_LEVEL_L, 0xA0, 3, 0, 0)
/* 0x283C */ DEFINE_SFX(NA_SE_EV_SPEAR_FENCE, 0x30, 0, 0, 0)
/* 0x283D */ DEFINE_SFX(NA_SE_EV_GANON_HORSE_NEIGH, 0x30, 0, 0, SFX_FLAG_10)
/* 0x283E */ DEFINE_SFX(NA_SE_EV_GANON_HORSE_GROAN, 0x30, 0, 0, SFX_FLAG_10)
/* 0x283F */ DEFINE_SFX(NA_SE_EV_FANTOM_WARP_S, 0x70, 3, 0, SFX_FLAG_4)
/* 0x2840 */ DEFINE_SFX(NA_SE_EV_FANTOM_WARP_L, 0x60, 0, 0, SFX_FLAG_15)
/* 0x2841 */ DEFINE_SFX(NA_SE_EV_FOUNTAIN, 0x30, 0, 0, SFX_FLAG_15)
/* 0x2842 */ DEFINE_SFX(NA_SE_EV_KID_HORSE_WALK, 0x30, 0, 0, 0)
/* 0x2843 */ DEFINE_SFX(NA_SE_EV_KID_HORSE_RUN, 0x30, 0, 0, 0)
/* 0x2844 */ DEFINE_SFX(NA_SE_EV_KID_HORSE_NEIGH, 0x30, 0, 0, 0)
/* 0x2845 */ DEFINE_SFX(NA_SE_EV_KID_HORSE_GROAN, 0x30, 0, 0, 0)
/* 0x2846 */ DEFINE_SFX(NA_SE_EV_WHITE_OUT, 0x30, 3, 0, SFX_FLAG_13)
/* 0x2847 */ DEFINE_SFX(NA_SE_EV_LIGHT_GATHER, 0x30, 0, 0, 0)
/* 0x2848 */ DEFINE_SFX(NA_SE_EV_TREE_CUT, 0x30, 0, 0, 0)
/* 0x2849 */ DEFINE_SFX(NA_SE_EV_VOLCANO, 0x30, 0, 0, SFX_FLAG_13 | SFX_FLAG_4)
/* 0x284A */ DEFINE_SFX(NA_SE_EV_GUILLOTINE_UP, 0x30, 0, 0, 0)
/* 0x284B */ DEFINE_SFX(NA_SE_EV_GUILLOTINE_BOUND, 0x30, 0, 0, 0)
/* 0x284C */ DEFINE_SFX(NA_SE_EV_ROLLCUTTER_MOTOR, 0x30, 0, 0, 0)
/* 0x284D */ DEFINE_SFX(NA_SE_EV_CHINETRAP_DOWN, 0x30, 0, 0, 0)
/* 0x284E */ DEFINE_SFX(NA_SE_EV_PLANT_BROKEN, 0x30, 1, 0, 0)
/* 0x284F */ DEFINE_SFX(NA_SE_EV_SHIP_BELL, 0x30, 0, 0, 0)
/* 0x2850 */ DEFINE_SFX(NA_SE_EV_FLUTTER_FLAG, 0x30, 0, 0, 0)
/* 0x2851 */ DEFINE_SFX(NA_SE_EV_TRAP_BOUND, 0x40, 0, 0, 0)
/* 0x2852 */ DEFINE_SFX(NA_SE_EV_ROCK_BROKEN, 0x30, 2, 3, 0)
/* 0x2853 */ DEFINE_SFX(NA_SE_EV_FANTOM_WARP_S2, 0x70, 2, 0, 0)
/* 0x2854 */ DEFINE_SFX(NA_SE_EV_FANTOM_WARP_L2, 0x60, 2, 0, 0)
/* 0x2855 */ DEFINE_SFX(NA_SE_EV_COFFIN_CAP_OPEN, 0x30, 0, 0, 0)
/* 0x2856 */ DEFINE_SFX(NA_SE_EV_COFFIN_CAP_BOUND, 0x60, 1, 0, 0)
/* 0x2857 */ DEFINE_SFX(NA_SE_EV_WIND_TRAP, 0x30, 2, 0, 0)
/* 0x2858 */ DEFINE_SFX(NA_SE_EV_TRAP_OBJ_SLIDE, 0x30, 0, 0, 0)
/* 0x2859 */ DEFINE_SFX(NA_SE_EV_METALDOOR_OPEN, 0x90, 3, 0, 0)
/* 0x285A */ DEFINE_SFX(NA_SE_EV_METALDOOR_CLOSE, 0x90, 3, 0, 0)
/* 0x285B */ DEFINE_SFX(NA_SE_EV_BURN_OUT, 0x30, 0, 0, 0)
/* 0x285C */ DEFINE_SFX(NA_SE_EV_BLOCKSINK, 0x30, 2, 0, 0)
/* 0x285D */ DEFINE_SFX(NA_SE_EV_CROWD, 0x30, 0, 0, SFX_FLAG_13 | SFX_FLAG_12 | SFX_FLAG_11)
/* 0x285E */ DEFINE_SFX(NA_SE_EV_WATER_LEVEL_DOWN, 0x30, 0, 0, 0)
#if PLATFORM_N64
/* 0x285F */ DEFINE_SFX(NA_SE_EV_NAVY_VANISH, 0x2C, 0, 0, 0)
#else
/* 0x285F */ DEFINE_SFX(NA_SE_EV_NAVY_VANISH, 0x30, 0, 0, 0)
#endif
/* 0x2860 */ DEFINE_SFX(NA_SE_EV_LADDER_DOUND, 0x30, 3, 0, 0)
/* 0x2861 */ DEFINE_SFX(NA_SE_EV_WEB_VIBRATION, 0x30, 0, 0, 0)
/* 0x2862 */ DEFINE_SFX(NA_SE_EV_WEB_BROKEN, 0x30, 0, 0, 0)
/* 0x2863 */ DEFINE_SFX(NA_SE_EV_ROLL_STAND, 0x30, 3, 0, 0)
/* 0x2864 */ DEFINE_SFX(NA_SE_EV_BUYODOOR_OPEN, 0x30, 0, 0, 0)
/* 0x2865 */ DEFINE_SFX(NA_SE_EV_BUYODOOR_CLOSE, 0x30, 0, 0, 0)
/* 0x2866 */ DEFINE_SFX(NA_SE_EV_WOODDOOR_OPEN, 0x30, 0, 0, 0)
/* 0x2867 */ DEFINE_SFX(NA_SE_EV_METALGATE_OPEN, 0x30, 0, 0, 0)
/* 0x2868 */ DEFINE_SFX(NA_SE_IT_SCOOP_UP_WATER, 0x30, 0, 0, 0)
/* 0x2869 */ DEFINE_SFX(NA_SE_EV_FISH_LEAP, 0x30, 0, 0, 0)
/* 0x286A */ DEFINE_SFX(NA_SE_EV_KAKASHI_SWING, 0x30, 0, 0, 0)
/* 0x286B */ DEFINE_SFX(NA_SE_EV_KAKASHI_ROLL, 0x30, 0, 0, 0)
/* 0x286C */ DEFINE_SFX(NA_SE_EV_BOTTLE_CAP_OPEN, 0x30, 0, 0, 0)
/* 0x286D */ DEFINE_SFX(NA_SE_EV_JABJAB_BREATHE, 0x30, 3, 0, SFX_FLAG_11)
/* 0x286E */ DEFINE_SFX(NA_SE_EV_SPIRIT_STONE, 0x30, 0, 0, 0)
/* 0x286F */ DEFINE_SFX(NA_SE_EV_TRIFORCE_FLASH, 0x30, 3, 0, 0)
/* 0x2870 */ DEFINE_SFX(NA_SE_EV_FALL_DOWN_DIRT, 0x30, 0, 0, 0)
/* 0x2871 */ DEFINE_SFX(NA_SE_EV_NAVY_FLY, 0x30, 0, 0, 0)
/* 0x2872 */ DEFINE_SFX(NA_SE_EV_NAVY_CRASH, 0x30, 0, 0, 0)
/* 0x2873 */ DEFINE_SFX(NA_SE_EV_WOOD_HIT, 0x30, 0, 0, 0)
/* 0x2874 */ DEFINE_SFX(NA_SE_EV_SCOOPUP_WATER, 0x30, 0, 0, 0)
/* 0x2875 */ DEFINE_SFX(NA_SE_EV_DROP_FALL, 0x30, 0, 0, 0)
/* 0x2876 */ DEFINE_SFX(NA_SE_EV_WOOD_GEAR, 0x30, 2, 0, 0)
/* 0x2877 */ DEFINE_SFX(NA_SE_EV_TREE_SWING, 0x30, 0, 0, 0)
/* 0x2878 */ DEFINE_SFX(NA_SE_EV_HORSE_RUN_LEVEL, 0x30, 0, 0, 0)
/* 0x2879 */ DEFINE_SFX(NA_SE_EV_ELEVATOR_MOVE2, 0x30, 2, 0, 0)
/* 0x287A */ DEFINE_SFX(NA_SE_EV_ELEVATOR_STOP, 0x30, 2, 0, 0)
/* 0x287B */ DEFINE_SFX(NA_SE_EV_TRE_BOX_APPEAR, 0x30, 2, 0, 0)
/* 0x287C */ DEFINE_SFX(NA_SE_EV_CHAIN_KEY_UNLOCK, 0x40, 0, 0, 0)
/* 0x287D */ DEFINE_SFX(NA_SE_EV_SPINE_TRAP_MOVE, 0x1C, 0, 0, 0)
/* 0x287E */ DEFINE_SFX(NA_SE_EV_HEALING, 0x30, 0, 0, 0)
/* 0x287F */ DEFINE_SFX(NA_SE_EV_GREAT_FAIRY_APPEAR, 0x30, 0, 0, 0)
/* 0x2880 */ DEFINE_SFX(NA_SE_EV_GREAT_FAIRY_VANISH, 0x30, 0, 0, 0)
/* 0x2881 */ DEFINE_SFX(NA_SE_EV_RED_EYE, 0x30, 0, 0, 0)
/* 0x2882 */ DEFINE_SFX(NA_SE_EV_ROLL_STAND_2, 0x30, 0, 0, 0)
/* 0x2883 */ DEFINE_SFX(NA_SE_EV_WALL_SLIDE, 0x30, 0, 0, 0)
/* 0x2884 */ DEFINE_SFX(NA_SE_EV_TRE_BOX_FLASH, 0x30, 0, 0, 0)
/* 0x2885 */ DEFINE_SFX(NA_SE_EV_WINDMILL_LEVEL, 0x60, 0, 0, SFX_FLAG_9)
/* 0x2886 */ DEFINE_SFX(NA_SE_EV_GOTO_HEAVEN, 0x30, 0, 0, SFX_FLAG_11)
/* 0x2887 */ DEFINE_SFX(NA_SE_EV_POT_BROKEN, 0x30, 0, 0, 0)
/* 0x2888 */ DEFINE_SFX(NA_SE_PL_PUT_DOWN_POT, 0x30, 0, 0, 0)
/* 0x2889 */ DEFINE_SFX(NA_SE_EV_DIVE_INTO_WATER, 0x30, 0, 0, 0)
/* 0x288A */ DEFINE_SFX(NA_SE_EV_JUMP_OUT_WATER, 0x30, 0, 0, 0)
/* 0x288B */ DEFINE_SFX(NA_SE_EV_GOD_FLYING, 0x30, 3, 0, 0)
/* 0x288C */ DEFINE_SFX(NA_SE_EV_TRIFORCE, 0x30, 0, 0, 0)
/* 0x288D */ DEFINE_SFX(NA_SE_EV_AURORA, 0x30, 0, 0, 0)
/* 0x288E */ DEFINE_SFX(NA_SE_EV_DEKU_DEATH, 0x30, 0, 0, 0)
/* 0x288F */ DEFINE_SFX(NA_SE_EV_BUYOSTAND_RISING, 0x30, 3, 0, 0)
/* 0x2890 */ DEFINE_SFX(NA_SE_EV_BUYOSTAND_FALL, 0x30, 3, 0, 0)
/* 0x2891 */ DEFINE_SFX(NA_SE_EV_BUYOSHUTTER_OPEN, 0x30, 0, 0, SFX_FLAG_13)
/* 0x2892 */ DEFINE_SFX(NA_SE_EV_BUYOSHUTTER_CLOSE, 0x30, 0, 0, SFX_FLAG_13)
/* 0x2893 */ DEFINE_SFX(NA_SE_EV_STONEDOOR_STOP, 0x30, 3, 0, 0)
/* 0x2894 */ DEFINE_SFX(NA_SE_EV_S_STONE_REVIVAL, 0x30, 0, 0, 0)
/* 0x2895 */ DEFINE_SFX(NA_SE_EV_MEDAL_APPEAR_S, 0x30, 0, 0, 0)
/* 0x2896 */ DEFINE_SFX(NA_SE_EV_HUMAN_BOUND, 0x30, 0, 2, 0)
/* 0x2897 */ DEFINE_SFX(NA_SE_EV_MEDAL_APPEAR_L, 0x30, 0, 0, 0)
/* 0x2898 */ DEFINE_SFX(NA_SE_EV_EARTHQUAKE, 0x30, 0, 0, 0)
/* 0x2899 */ DEFINE_SFX(NA_SE_EV_SHUT_BY_CRYSTAL, 0x30, 0, 0, 0)
/* 0x289A */ DEFINE_SFX(NA_SE_EV_GOD_LIGHTBALL_2, 0x30, 0, 0, 0)
/* 0x289B */ DEFINE_SFX(NA_SE_EV_RUN_AROUND, 0x30, 0, 0, 0)
/* 0x289C */ DEFINE_SFX(NA_SE_EV_CONSENTRATION, 0x30, 0, 0, SFX_FLAG_11)
/* 0x289D */ DEFINE_SFX(NA_SE_EV_TIMETRIP_LIGHT, 0x30, 0, 0, SFX_FLAG_11)
/* 0x289E */ DEFINE_SFX(NA_SE_EV_BUYOSTAND_STOP_A, 0x30, 2, 0, 0)
/* 0x289F */ DEFINE_SFX(NA_SE_EV_BUYOSTAND_STOP_U, 0x30, 3, 0, 0)
/* 0x28A0 */ DEFINE_SFX(NA_SE_EV_OBJECT_FALL, 0x30, 0, 0, 0)
/* 0x28A1 */ DEFINE_SFX(NA_SE_EV_JUMP_CONC, 0x30, 0, 0, 0)
/* 0x28A2 */ DEFINE_SFX(NA_SE_EV_ICE_MELT, 0x30, 0, 0, 0)
/* 0x28A3 */ DEFINE_SFX(NA_SE_EV_FIRE_PILLAR_S, 0x30, 0, 0, 0)
/* 0x28A4 */ DEFINE_SFX(NA_SE_EV_BLOCK_RISING, 0x20, 3, 0, 0)
/* 0x28A5 */ DEFINE_SFX(NA_SE_EV_NABALL_VANISH, 0x30, 0, 0, 0)
/* 0x28A6 */ DEFINE_SFX(NA_SE_EV_SARIA_MELODY, 0x30, 0, 0, SFX_FLAG_15)
/* 0x28A7 */ DEFINE_SFX(NA_SE_EV_LINK_WARP_OUT, 0x30, 0, 0, 0)
/* 0x28A8 */ DEFINE_SFX(NA_SE_EV_FIATY_HEAL, 0x30, 0, 0, 0)
/* 0x28A9 */ DEFINE_SFX(NA_SE_EV_CHAIN_KEY_UNLOCK_B, 0x30, 0, 0, 0)
/* 0x28AA */ DEFINE_SFX(NA_SE_EV_WOODBOX_BREAK, 0x30, 2, 0, 0)
/* 0x28AB */ DEFINE_SFX(NA_SE_EV_PUT_DOWN_WOODBOX, 0x30, 0, 0, 0)
/* 0x28AC */ DEFINE_SFX(NA_SE_EV_LAND_DIRT, 0x30, 0, 0, 0)
/* 0x28AD */ DEFINE_SFX(NA_SE_EV_FLOOR_ROLLING, 0x30, 0, 0, 0)
/* 0x28AE */ DEFINE_SFX(NA_SE_EV_DOG_CRY_EVENING, 0x30, 0, 0, 0)
/* 0x28AF */ DEFINE_SFX(NA_SE_EV_JABJAB_HICCUP, 0x30, 0, 0, 0)
/* 0x28B0 */ DEFINE_SFX(NA_SE_EV_NALE_MAGIC, 0x30, 0, 0, 0)
/* 0x28B1 */ DEFINE_SFX(NA_SE_EV_FROG_JUMP, 0x30, 0, 0, 0)
/* 0x28B2 */ DEFINE_SFX(NA_SE_EV_ICE_FREEZE, 0x30, 3, 0, 0)
/* 0x28B3 */ DEFINE_SFX(NA_SE_EV_BURNING, 0x60, 3, 0, 0)
/* 0x28B4 */ DEFINE_SFX(NA_SE_EV_WOODPLATE_BOUND, 0x30, 0, 2, 0)
/* 0x28B5 */ DEFINE_SFX(NA_SE_EV_GORON_WATER_DROP, 0x30, 0, 0, SFX_FLAG_13)
/* 0x28B6 */ DEFINE_SFX(NA_SE_EV_JABJAB_GROAN, 0x30, 0, 0, 0)
/* 0x28B7 */ DEFINE_SFX(NA_SE_EV_DARUMA_VANISH, 0x30, 1, 0, 0)
/* 0x28B8 */ DEFINE_SFX(NA_SE_EV_BIGBALL_ROLL, 0x30, 0, 0, 0)
/* 0x28B9 */ DEFINE_SFX(NA_SE_EV_ELEVATOR_MOVE3, 0x30, 0, 0, 0)
/* 0x28BA */ DEFINE_SFX(NA_SE_EV_DIAMOND_SWITCH, 0x30, 2, 0, 0)
/* 0x28BB */ DEFINE_SFX(NA_SE_EV_FLAME_OF_FIRE, 0x30, 3, 0, 0)
/* 0x28BC */ DEFINE_SFX(NA_SE_EV_RAINBOW_SHOWER, 0x30, 0, 0, 0)
/* 0x28BD */ DEFINE_SFX(NA_SE_EV_FLYING_AIR, 0x30, 0, 0, 0)
/* 0x28BE */ DEFINE_SFX(NA_SE_EV_PASS_AIR, 0x30, 0, 0, 0)
/* 0x28BF */ DEFINE_SFX(NA_SE_EV_COME_UP_DEKU_JR, 0x30, 0, 0, 0)
/* 0x28C0 */ DEFINE_SFX(NA_SE_EV_SAND_STORM, 0x30, 0, 0, 0)
/* 0x28C1 */ DEFINE_SFX(NA_SE_EV_TRIFORCE_MARK, 0x30, 0, 0, 0)
/* 0x28C2 */ DEFINE_SFX(NA_SE_EV_GRAVE_EXPLOSION, 0xA0, 3, 0, 0)
/* 0x28C3 */ DEFINE_SFX(NA_SE_EV_LURE_MOVE_W, 0x30, 0, 0, 0)
/* 0x28C4 */ DEFINE_SFX(NA_SE_EV_POT_MOVE_START, 0x30, 0, 0, 0)
/* 0x28C5 */ DEFINE_SFX(NA_SE_EV_DIVE_INTO_WATER_L, 0x30, 0, 0, 0)
/* 0x28C6 */ DEFINE_SFX(NA_SE_EV_OUT_OF_WATER_L, 0x30, 0, 0, 0)
/* 0x28C7 */ DEFINE_SFX(NA_SE_EV_GANON_MANTLE, 0x30, 0, 0, 0)
/* 0x28C8 */ DEFINE_SFX(NA_SE_EV_DIG_UP, 0x30, 0, 0, 0)
/* 0x28C9 */ DEFINE_SFX(NA_SE_EV_WOOD_BOUND, 0x30, 0, 0, 0)
/* 0x28CA */ DEFINE_SFX(NA_SE_EV_WATER_BUBBLE, 0x30, 0, 3, 0)
/* 0x28CB */ DEFINE_SFX(NA_SE_EV_ICE_BROKEN, 0x30, 2, 0, 0)
/* 0x28CC */ DEFINE_SFX(NA_SE_EV_FROG_GROW_UP, 0x30, 2, 0, 0)
/* 0x28CD */ DEFINE_SFX(NA_SE_EV_WATER_CONVECTION, 0x30, 0, 0, 0)
/* 0x28CE */ DEFINE_SFX(NA_SE_EV_GROUND_GATE_OPEN, 0x30, 3, 0, 0)
/* 0x28CF */ DEFINE_SFX(NA_SE_EV_FACE_BREAKDOWN, 0x30, 3, 0, 0)
/* 0x28D0 */ DEFINE_SFX(NA_SE_EV_FACE_EXPLOSION, 0x30, 0, 0, 0)
/* 0x28D1 */ DEFINE_SFX(NA_SE_EV_FACE_CRUMBLE_SLOW, 0x30, 3, 2, SFX_FLAG_14)
/* 0x28D2 */ DEFINE_SFX(NA_SE_EV_ROUND_TRAP_MOVE, 0x30, 0, 0, 0)
/* 0x28D3 */ DEFINE_SFX(NA_SE_EV_HIT_SOUND, 0x30, 0, 0, 0)
/* 0x28D4 */ DEFINE_SFX(NA_SE_EV_ICE_SWING, 0x30, 0, 0, 0)
/* 0x28D5 */ DEFINE_SFX(NA_SE_EV_DOWN_TO_GROUND, 0x30, 0, 0, 0)
/* 0x28D6 */ DEFINE_SFX(NA_SE_EV_KENJA_ENVIROMENT_0, 0x30, 0, 0, 0)
/* 0x28D7 */ DEFINE_SFX(NA_SE_EV_KENJA_ENVIROMENT_1, 0x30, 0, 0, 0)
/* 0x28D8 */ DEFINE_SFX(NA_SE_EV_SMALL_DOG_BARK, 0x80, 0, 0, 0)
/* 0x28D9 */ DEFINE_SFX(NA_SE_EV_ZELDA_POWER, 0x60, 0, 0, 0)
/* 0x28DA */ DEFINE_SFX(NA_SE_EV_RAIN, 0x90, 0, 0, 0)
/* 0x28DB */ DEFINE_SFX(NA_SE_EV_IRON_DOOR_OPEN, 0x30, 0, 0, 0)
/* 0x28DC */ DEFINE_SFX(NA_SE_EV_IRON_DOOR_CLOSE, 0x30, 0, 0, 0)
/* 0x28DD */ DEFINE_SFX(NA_SE_EV_WHIRLPOOL, 0x30, 0, 0, 0)
/* 0x28DE */ DEFINE_SFX(NA_SE_EV_TOWER_PARTS_BROKEN, 0x60, 3, 3, 0)
/* 0x28DF */ DEFINE_SFX(NA_SE_EV_COW_CRY, 0x30, 0, 0, 0)
/* 0x28E0 */ DEFINE_SFX(NA_SE_EV_METAL_BOX_BOUND, 0x30, 0, 0, 0)
/* 0x28E1 */ DEFINE_SFX(NA_SE_EV_ELECTRIC_EXPLOSION, 0x30, 3, 0, 0)
/* 0x28E2 */ DEFINE_SFX(NA_SE_EV_HEAVY_THROW, 0x30, 3, 0, 0)
/* 0x28E3 */ DEFINE_SFX(NA_SE_EV_FROG_CRY_0, 0x30, 0, 0, 0)
/* 0x28E4 */ DEFINE_SFX(NA_SE_EV_FROG_CRY_1, 0x30, 0, 0, 0)
/* 0x28E5 */ DEFINE_SFX(NA_SE_EV_COW_CRY_LV, 0x30, 0, 0, 0)
/* 0x28E6 */ DEFINE_SFX(NA_SE_EV_RONRON_DOOR_CLOSE, 0x30, 0, 0, 0)
/* 0x28E7 */ DEFINE_SFX(NA_SE_EV_BUTTERFRY_TO_FAIRY, 0x30, 0, 0, 0)
/* 0x28E8 */ DEFINE_SFX(NA_SE_EV_FIVE_COUNT_LUPY, 0xA0, 0, 0, SFX_FLAG_11)
/* 0x28E9 */ DEFINE_SFX(NA_SE_EV_STONE_GROW_UP, 0x30, 0, 0, 0)
/* 0x28EA */ DEFINE_SFX(NA_SE_EV_STONE_LAUNCH, 0x30, 0, 0, 0)
/* 0x28EB */ DEFINE_SFX(NA_SE_EV_STONE_ROLLING, 0x30, 0, 0, 0)
/* 0x28EC */ DEFINE_SFX(NA_SE_EV_TOGE_STICK_ROLLING, 0x30, 2, 0, 0)
/* 0x28ED */ DEFINE_SFX(NA_SE_EV_TOWER_ENERGY, 0x30, 0, 0, 0)
/* 0x28EE */ DEFINE_SFX(NA_SE_EV_TOWER_BARRIER, 0x30, 3, 0, 0)
/* 0x28EF */ DEFINE_SFX(NA_SE_EV_CHIBI_WALK, 0x20, 0, 0, 0)
/* 0x28F0 */ DEFINE_SFX(NA_SE_EV_KNIGHT_WALK, 0x30, 0, 0, 0)
/* 0x28F1 */ DEFINE_SFX(NA_SE_EV_PILLAR_MOVE_STOP, 0x30, 0, 0, 0)
/* 0x28F2 */ DEFINE_SFX(NA_SE_EV_ERUPTION_CLOUD, 0x30, 0, 0, 0)
/* 0x28F3 */ DEFINE_SFX(NA_SE_EV_LINK_WARP_OUT_LV, 0x30, 0, 0, 0)
/* 0x28F4 */ DEFINE_SFX(NA_SE_EV_LINK_WARP_IN, 0x30, 0, 0, 0)
/* 0x28F5 */ DEFINE_SFX(NA_SE_EV_OCARINA_BMELO_0, 0x30, 0, 0, 0)
/* 0x28F6 */ DEFINE_SFX(NA_SE_EV_OCARINA_BMELO_1, 0x30, 0, 0, 0)
/* 0x28F7 */ DEFINE_SFX(NA_SE_EV_EXPLOSION_FOR_RENZOKU, 0x30, 0, 0, 0)
