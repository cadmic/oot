/*
 * ROM spec file
 */

#include "include/versions.h"

beginseg
    name "makerom"
    include "$(BUILD_DIR)/src/makerom/rom_header.o"
    include "$(BUILD_DIR)/src/makerom/ipl3.o"
    include "$(BUILD_DIR)/src/makerom/entry.o"
endseg

beginseg
    name "boot"
    address 0x80000460

    include "$(BUILD_DIR)/src/boot/boot_main.o"
    include "$(BUILD_DIR)/src/boot/idle.o"
#if OOT_VERSION >= PAL_1_0
    include "$(BUILD_DIR)/src/boot/viconfig.o"
#endif
    include "$(BUILD_DIR)/src/boot/carthandle.o"
    include "$(BUILD_DIR)/src/boot/z_std_dma.o"
#if !PLATFORM_IQUE
    include "$(BUILD_DIR)/src/boot/yaz0.o"
#else
    include "$(BUILD_DIR)/src/boot/zlib.o"
#endif
    include "$(BUILD_DIR)/src/boot/z_locale.o"
#if PLATFORM_N64
    include "$(BUILD_DIR)/src/boot/cic6105.o"
#endif
#if DEBUG_FEATURES
    include "$(BUILD_DIR)/src/boot/assert.o"
#endif
    include "$(BUILD_DIR)/src/boot/is_debug.o"
    include "$(BUILD_DIR)/src/boot/driverominit.o"
    include "$(BUILD_DIR)/src/boot/mio0.o"

    // libu64
    include "$(BUILD_DIR)/src/libu64/stackcheck.o"
#if !PLATFORM_IQUE
    include "$(BUILD_DIR)/src/libu64/debug.o"
#endif

    // libc64
#if PLATFORM_N64
    include "$(BUILD_DIR)/src/libc64/sleep.o"
#endif
#if DEBUG_FEATURES
    include "$(BUILD_DIR)/src/libc64/sprintf.o"
#endif

    // libultra
#if PLATFORM_N64
#include "spec_includes/boot_libultra_n64.inc"
#elif PLATFORM_GC
#include "spec_includes/boot_libultra_gc.inc"
#elif PLATFORM_IQUE
#include "spec_includes/boot_libultra_ique.inc"
#endif

    // libgcc
#if PLATFORM_IQUE && !defined(COMPILER_GCC)
    include "$(BUILD_DIR)/src/libgcc/__divdi3.o"
    include "$(BUILD_DIR)/src/libgcc/__moddi3.o"
    include "$(BUILD_DIR)/src/libgcc/__udivdi3.o"
    include "$(BUILD_DIR)/src/libgcc/__umoddi3.o"
    include "$(BUILD_DIR)/src/libgcc/__cmpdi2.o"
    include "$(BUILD_DIR)/src/libgcc/__floatdidf.o"
    include "$(BUILD_DIR)/src/libgcc/__floatdisf.o"
    include "$(BUILD_DIR)/src/libgcc/__fixunsdfdi.o"
    include "$(BUILD_DIR)/src/libgcc/__fixdfdi.o"
    include "$(BUILD_DIR)/src/libgcc/__fixunssfdi.o"
    include "$(BUILD_DIR)/src/libgcc/__fixsfdi.o"
#endif

    // Build information
    include "$(BUILD_DIR)/src/boot/build.o"

    // RSP microcode
    include "$(BUILD_DIR)/data/rsp_boot.text.o"
    include "$(BUILD_DIR)/data/cic6105.text.o"

    // Extra files for non-matching debug builds
#if DEBUG_FEATURES
    include "$(BUILD_DIR)/src/libu64/debug.o"
    include "$(BUILD_DIR)/src/libultra/io/epiwrite.o"
    include "$(BUILD_DIR)/src/libultra/io/vimodefpallan1.o"
    include "$(BUILD_DIR)/src/libultra/libc/ldiv.o"
    include "$(BUILD_DIR)/src/libultra/libc/string.o"
    include "$(BUILD_DIR)/src/libultra/libc/xldtob.o"
    include "$(BUILD_DIR)/src/libultra/libc/xlitob.o"
    include "$(BUILD_DIR)/src/libultra/libc/xprintf.o"
#endif

    // Functions that GCC-compiled code may depend on, placed in boot so they will always be loaded
#ifdef COMPILER_GCC
    include "$(BUILD_DIR)/src/libultra/libc/string.o"
    include "$(BUILD_DIR)/src/libc/memset.o"
    include "$(BUILD_DIR)/src/libc/memmove.o"
    include "$(BUILD_DIR)/src/gcc_fix/missing_gcc_functions.o"
#endif

endseg

beginseg
    name "dmadata"
    include "$(BUILD_DIR)/src/dmadata/dmadata.o"
endseg

beginseg
    name "Audiobank"
    address 0
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_0.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_1.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_2.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_3.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_4.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_5.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_6.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_7.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_8.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_9.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_10.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_11.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_12.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_13.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_14.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_15.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_16.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_17.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_18.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_19.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_20.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_21.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_22.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_23.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_24.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_25.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_26.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_27.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_28.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_29.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_30.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_31.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_32.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_33.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_34.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_35.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_36.o"
    include "$(BUILD_DIR)/assets/audio/soundfonts/Soundfont_37.o"
#if OOT_VERSION >= PAL_1_0
    include "$(BUILD_DIR)/assets/audio/audiobank_padding.o"
#endif
endseg

beginseg
    name "Audioseq"
    address 0
    include "$(BUILD_DIR)/assets/audio/sequences/seq_0.prg.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_1.prg.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_2.prg.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_3.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_4.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_5.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_6.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_7.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_8.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_9.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_10.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_11.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_12.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_13.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_14.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_15.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_16.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_17.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_18.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_19.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_20.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_21.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_22.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_23.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_24.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_25.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_26.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_27.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_28.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_29.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_30.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_31.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_32.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_33.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_34.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_35.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_36.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_37.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_38.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_39.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_40.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_41.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_42.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_43.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_44.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_45.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_46.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_47.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_48.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_49.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_50.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_51.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_52.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_53.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_54.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_55.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_56.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_57.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_58.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_59.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_60.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_61.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_62.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_63.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_64.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_65.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_66.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_67.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_68.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_69.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_70.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_71.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_72.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_73.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_74.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_75.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_76.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_77.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_78.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_79.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_80.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_81.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_82.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_83.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_84.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_85.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_86.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_88.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_89.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_90.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_91.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_92.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_93.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_94.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_95.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_96.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_97.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_98.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_99.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_100.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_101.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_102.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_103.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_104.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_105.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_106.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_107.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_108.o"
    include "$(BUILD_DIR)/assets/audio/sequences/seq_109.prg.o"
endseg

beginseg
    name "Audiotable"
    address 0
    include "$(BUILD_DIR)/assets/audio/samplebanks/SampleBank_0.o"
    include "$(BUILD_DIR)/assets/audio/samplebanks/SampleBank_2.o"
    include "$(BUILD_DIR)/assets/audio/samplebanks/SampleBank_3.o"
    include "$(BUILD_DIR)/assets/audio/samplebanks/SampleBank_4.o"
    include "$(BUILD_DIR)/assets/audio/samplebanks/SampleBank_5.o"
    include "$(BUILD_DIR)/assets/audio/samplebanks/SampleBank_6.o"
endseg

#if OOT_NTSC
beginseg
    name "kanji"
    include "$(BUILD_DIR)/assets/textures/kanji/kanji.o"
endseg
#endif

beginseg
    name "link_animetion"
#if OOT_NTSC
    romalign 0x1000
#endif
    include "$(BUILD_DIR)/assets/misc/link_animetion/link_animetion.o"
    number 7
endseg

beginseg
    name "icon_item_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/icon_item_static/icon_item_static.o"
    number 8
endseg

beginseg
    name "icon_item_24_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/icon_item_24_static/icon_item_24_static.o"
    number 9
endseg

beginseg
    name "icon_item_field_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/icon_item_field_static/icon_item_field_static.o"
    number 12
endseg

beginseg
    name "icon_item_dungeon_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/icon_item_dungeon_static/icon_item_dungeon_static.o"
    number 12
endseg

beginseg
    name "icon_item_gameover_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/icon_item_gameover_static/icon_item_gameover_static.o"
    number 12
endseg

#if OOT_NTSC
beginseg
    name "icon_item_jpn_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/icon_item_jpn_static/icon_item_jpn_static.o"
    number 13
endseg
#endif

beginseg
    name "icon_item_nes_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/icon_item_nes_static/icon_item_nes_static.o"
    number 13
endseg

#if OOT_PAL
beginseg
    name "icon_item_ger_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/icon_item_ger_static/icon_item_ger_static.o"
    number 13
endseg

beginseg
    name "icon_item_fra_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/icon_item_fra_static/icon_item_fra_static.o"
    number 13
endseg
#endif

beginseg
    name "item_name_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/item_name_static/item_name_static.o"
    number 10
endseg

beginseg
    name "map_name_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/map_name_static/map_name_static.o"
    number 11
endseg

beginseg
    name "do_action_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/do_action_static/do_action_static.o"
    number 7
endseg

beginseg
    name "message_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/message_static/message_static.o"
    number 7
endseg

#if OOT_NTSC && OOT_VERSION < NTSC_1_2
beginseg
    name "jpn_message_data_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/text/jpn_message_data_static.o"
    number 8
endseg
#endif

beginseg
    name "message_texture_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/message_texture_static/message_texture_static.o"
    number 9
endseg

beginseg
    name "nes_font_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/nes_font_static/nes_font_static.o"
    number 10
endseg

#if OOT_NTSC && OOT_VERSION >= NTSC_1_2
beginseg
    name "jpn_message_data_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/text/jpn_message_data_static.o"
    number 8
endseg
#endif

beginseg
    name "nes_message_data_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/text/nes_message_data_static.o"
    number 7
endseg

#if OOT_PAL
beginseg
    name "ger_message_data_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/text/ger_message_data_static.o"
    number 7
endseg

beginseg
    name "fra_message_data_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/text/fra_message_data_static.o"
    number 7
endseg
#endif

beginseg
    name "staff_message_data_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/text/staff_message_data_static.o"
    number 7
endseg

beginseg
    name "map_grand_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/map_grand_static/map_grand_static.o"
    number 11
endseg

#if PLATFORM_N64
beginseg
    name "map_i_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/map_i_static/map_i_static.o"
    number 11
endseg
#endif

beginseg
    name "map_48x85_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/map_48x85_static/map_48x85_static.o"
    number 11
endseg

#if !PLATFORM_N64
beginseg
    name "map_i_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/map_i_static/map_i_static.o"
    number 11
endseg
#endif

beginseg
    name "code"
    compress
    after "dmadata"
    align 0x20

    include "$(BUILD_DIR)/src/code/z_en_a_keep.o"
    include "$(BUILD_DIR)/src/code/z_en_item00.o"
    include "$(BUILD_DIR)/src/code/z_eff_blure.o"
    include "$(BUILD_DIR)/src/code/z_eff_shield_particle.o"
    include "$(BUILD_DIR)/src/code/z_eff_spark.o"
    include "$(BUILD_DIR)/src/code/z_eff_ss_dead.o"
    include "$(BUILD_DIR)/src/code/z_effect.o"
    include "$(BUILD_DIR)/src/code/z_effect_soft_sprite.o"
    include "$(BUILD_DIR)/src/code/z_effect_soft_sprite_old_init.o"
    include "$(BUILD_DIR)/src/code/z_effect_soft_sprite_dlftbls.o"
    include "$(BUILD_DIR)/src/code/flg_set.o"
    include "$(BUILD_DIR)/src/code/z_DLF.o"
    include "$(BUILD_DIR)/src/code/z_actor.o"
    include "$(BUILD_DIR)/src/code/z_actor_dlftbls.o"
    include "$(BUILD_DIR)/src/code/z_bgcheck.o"
    include "$(BUILD_DIR)/src/code/z_bg_collect.o"
    include "$(BUILD_DIR)/src/code/z_bg_item.o"
    include "$(BUILD_DIR)/src/code/z_camera.o"
    include "$(BUILD_DIR)/src/code/z_collision_btltbls.o"
    include "$(BUILD_DIR)/src/code/z_collision_check.o"
    include "$(BUILD_DIR)/src/code/z_common_data.o"
    include "$(BUILD_DIR)/src/code/z_debug.o"
    include "$(BUILD_DIR)/src/code/z_debug_display.o"
    include "$(BUILD_DIR)/src/code/z_demo.o"
    include "$(BUILD_DIR)/src/code/z_memory_utils.o"
    include "$(BUILD_DIR)/src/code/z_draw.o"
    include "$(BUILD_DIR)/src/code/z_sfx_source.o"
    include "$(BUILD_DIR)/src/code/z_elf_message.o"
    include "$(BUILD_DIR)/src/code/z_face_reaction.o"
    include "$(BUILD_DIR)/src/code/z_env_flags.o"
    include "$(BUILD_DIR)/src/code/z_fcurve_data.o"
    include "$(BUILD_DIR)/src/code/z_fcurve_data_skelanime.o"
    include "$(BUILD_DIR)/src/code/z_game_dlftbls.o"
    include "$(BUILD_DIR)/src/code/z_horse.o"
    include "$(BUILD_DIR)/src/code/z_jpeg.o"
    include "$(BUILD_DIR)/src/code/z_kaleido_setup.o"
    include "$(BUILD_DIR)/src/code/z_kanfont.o"
    include "$(BUILD_DIR)/src/code/z_kankyo.o"
    include "$(BUILD_DIR)/src/code/z_lib.o"
    include "$(BUILD_DIR)/src/code/z_lifemeter.o"
    include "$(BUILD_DIR)/src/code/z_lights.o"
    include "$(BUILD_DIR)/src/code/z_malloc.o"
    include "$(BUILD_DIR)/src/code/z_map_mark.o"
#if DEBUG_ASSETS
    include "$(BUILD_DIR)/src/code/z_moji.o"
#endif
    include "$(BUILD_DIR)/src/code/z_prenmi_buff.o"
    include "$(BUILD_DIR)/src/code/z_nulltask.o"
    include "$(BUILD_DIR)/src/code/z_olib.o"
    include "$(BUILD_DIR)/src/code/z_onepointdemo.o"
    include "$(BUILD_DIR)/src/code/z_map_exp.o"
    include "$(BUILD_DIR)/src/code/z_map_data.o"
    include "$(BUILD_DIR)/src/code/z_parameter.o"
    include "$(BUILD_DIR)/src/code/z_path.o"
    include "$(BUILD_DIR)/src/code/z_frame_advance.o"
    include "$(BUILD_DIR)/src/code/z_player_lib.o"
    include "$(BUILD_DIR)/src/code/z_prenmi.o"
    include "$(BUILD_DIR)/src/code/z_quake.o"
    include "$(BUILD_DIR)/src/code/z_rcp.o"
    include "$(BUILD_DIR)/src/code/z_room.o"
    include "$(BUILD_DIR)/src/code/z_sample.o"
    include "$(BUILD_DIR)/src/code/z_inventory.o"
    include "$(BUILD_DIR)/src/code/z_scene.o"
    include "$(BUILD_DIR)/src/code/object_table.o"
    include "$(BUILD_DIR)/src/code/z_scene_table.o"
    include "$(BUILD_DIR)/src/code/z_skelanime.o"
    include "$(BUILD_DIR)/src/code/z_skin.o"
    include "$(BUILD_DIR)/src/code/z_skin_awb.o"
    include "$(BUILD_DIR)/src/code/z_skin_matrix.o"
    include "$(BUILD_DIR)/src/code/z_sram.o"
    include "$(BUILD_DIR)/src/code/z_ss_sram.o"
    include "$(BUILD_DIR)/src/code/z_rumble.o"
#if DEBUG_ASSETS
    include "$(BUILD_DIR)/data/z_text.data.o"
#endif
    include "$(BUILD_DIR)/data/unk_8012ABC0.data.o"
    include "$(BUILD_DIR)/src/code/z_view.o"
    include "$(BUILD_DIR)/src/code/z_vimode.o"
    include "$(BUILD_DIR)/src/code/z_viscvg.o"
    include "$(BUILD_DIR)/src/code/z_vismono.o"
    include "$(BUILD_DIR)/src/code/z_viszbuf.o"
    include "$(BUILD_DIR)/src/code/z_vr_box.o"
    include "$(BUILD_DIR)/src/code/z_vr_box_draw.o"
    include "$(BUILD_DIR)/src/code/z_player_call.o"
    include "$(BUILD_DIR)/src/code/z_fbdemo.o"
    include "$(BUILD_DIR)/src/code/z_fbdemo_triforce.o"
    include "$(BUILD_DIR)/src/code/z_fbdemo_wipe1.o"
    include "$(BUILD_DIR)/src/code/z_fbdemo_circle.o"
    include "$(BUILD_DIR)/src/code/z_fbdemo_fade.o"
    include "$(BUILD_DIR)/src/code/shrink_window.o"
#if DEBUG_FEATURES
    include "$(BUILD_DIR)/src/code/db_camera.o"
#endif
    include "$(BUILD_DIR)/src/code/z_cutscene_spline.o"
#if DEBUG_FEATURES
    include "$(BUILD_DIR)/src/code/mempak.o"
#endif
    include "$(BUILD_DIR)/src/code/z_kaleido_manager.o"
    include "$(BUILD_DIR)/src/code/z_kaleido_scope_call.o"
    include "$(BUILD_DIR)/src/code/z_play.o"
    include "$(BUILD_DIR)/src/code/PreRender.o"
    include "$(BUILD_DIR)/src/code/TwoHeadGfxArena.o"
    include "$(BUILD_DIR)/src/code/TwoHeadArena.o"
    include "$(BUILD_DIR)/src/code/audio_stop_all_sfx.o"
    include "$(BUILD_DIR)/src/code/audio_thread_manager.o"
    include "$(BUILD_DIR)/src/code/title_setup.o"
    include "$(BUILD_DIR)/src/code/game.o"
    include "$(BUILD_DIR)/src/code/gamealloc.o"
    include "$(BUILD_DIR)/src/code/graph.o"
    include "$(BUILD_DIR)/src/code/gfxalloc.o"
    include "$(BUILD_DIR)/src/code/listalloc.o"
    include "$(BUILD_DIR)/src/code/main.o"
    include "$(BUILD_DIR)/src/code/padmgr.o"
    include "$(BUILD_DIR)/src/code/sched.o"
    include "$(BUILD_DIR)/src/code/speed_meter.o"
    include "$(BUILD_DIR)/src/code/sys_cfb.o"
    include "$(BUILD_DIR)/src/code/sys_math.o"
    include "$(BUILD_DIR)/src/code/sys_math3d.o"
#if DEBUG_FEATURES
    include "$(BUILD_DIR)/src/code/sys_math3d_draw.o"
#endif
    include "$(BUILD_DIR)/src/code/sys_math_atan.o"
    include "$(BUILD_DIR)/src/code/sys_matrix.o"
    include "$(BUILD_DIR)/src/code/sys_ucode.o"
    include "$(BUILD_DIR)/src/code/sys_rumble.o"
    include "$(BUILD_DIR)/src/code/sys_freeze.o"
#if DEBUG_FEATURES
    include "$(BUILD_DIR)/src/code/sys_debug_controller.o"
#endif
    include "$(BUILD_DIR)/src/code/irqmgr.o"
#if PLATFORM_N64
    include "$(BUILD_DIR)/src/code/code_n64dd_800AD410.o"
    include "$(BUILD_DIR)/src/code/code_n64dd_800AD4C0.o"
#endif
#if DEBUG_FEATURES
    include "$(BUILD_DIR)/src/code/debug_malloc.o"
#endif
#if PLATFORM_N64
    include "$(BUILD_DIR)/src/code/fault_n64.o"
#else
    include "$(BUILD_DIR)/src/code/fault_gc.o"
    include "$(BUILD_DIR)/src/code/fault_gc_drawer.o"
#endif
    include "$(BUILD_DIR)/src/code/kanread.o"
#if DEBUG_FEATURES
    include "$(BUILD_DIR)/src/code/ucode_disas.o"
#endif

    // audio
#if OOT_VERSION < NTSC_1_1 || PLATFORM_GC
    pad_text
#endif
    include "$(BUILD_DIR)/src/audio/lib/data.o"
    include "$(BUILD_DIR)/src/audio/lib/synthesis.o"
    include "$(BUILD_DIR)/src/audio/lib/heap.o"
    include "$(BUILD_DIR)/src/audio/lib/load.o"
    include "$(BUILD_DIR)/src/audio/lib/thread.o"
    include "$(BUILD_DIR)/src/audio/lib/dcache.o"
    include "$(BUILD_DIR)/src/audio/lib/aisetnextbuf.o"
#if OOT_PAL_N64
    pad_text
    pad_text
    pad_text
#endif
    include "$(BUILD_DIR)/src/audio/lib/playback.o"
    include "$(BUILD_DIR)/src/audio/lib/effects.o"
    include "$(BUILD_DIR)/src/audio/lib/seqplayer.o"
    include "$(BUILD_DIR)/src/audio/general.o"
#if !PLATFORM_N64 && !DEBUG_FEATURES
    pad_text
#endif
    include "$(BUILD_DIR)/src/audio/sfx_params.o"
    include "$(BUILD_DIR)/src/audio/sfx.o"
    include "$(BUILD_DIR)/src/audio/sequence.o"
    include "$(BUILD_DIR)/src/audio/data.o"
    include "$(BUILD_DIR)/src/audio/session_config.o"
    include "$(BUILD_DIR)/src/audio/session_init.o"

    // libu64
#if PLATFORM_N64
    include "$(BUILD_DIR)/src/libu64/gfxprint.o"
    include "$(BUILD_DIR)/src/libu64/rcp_utils.o"
    include "$(BUILD_DIR)/src/libu64/loadfragment2_n64.o"
    include "$(BUILD_DIR)/src/libu64/pad.o"
    include "$(BUILD_DIR)/src/libu64/system_heap.o"
    include "$(BUILD_DIR)/src/libu64/padsetup.o"
#elif PLATFORM_GC
    include "$(BUILD_DIR)/src/libu64/logseverity_gc.o"
    include "$(BUILD_DIR)/src/libu64/gfxprint.o"
    include "$(BUILD_DIR)/src/libu64/rcp_utils.o"
    include "$(BUILD_DIR)/src/libu64/loadfragment2_gc.o"
#if DEBUG_FEATURES
    include "$(BUILD_DIR)/src/libu64/mtxuty-cvt.o"
#endif
    include "$(BUILD_DIR)/src/libu64/relocation_gc.o"
    include "$(BUILD_DIR)/src/libu64/load_gc.o"
    include "$(BUILD_DIR)/src/libu64/system_heap.o"
    include "$(BUILD_DIR)/src/libu64/pad.o"
    include "$(BUILD_DIR)/src/libu64/padsetup.o"
#elif PLATFORM_IQUE
    include "$(BUILD_DIR)/src/libu64/system_heap.o"
    include "$(BUILD_DIR)/src/libu64/debug.o"
    include "$(BUILD_DIR)/src/libu64/gfxprint.o"
    include "$(BUILD_DIR)/src/libu64/logseverity_gc.o"
    include "$(BUILD_DIR)/src/libu64/relocation_gc.o"
    include "$(BUILD_DIR)/src/libu64/loadfragment2_gc.o"
    include "$(BUILD_DIR)/src/libu64/load_gc.o"
    include "$(BUILD_DIR)/src/libu64/padsetup.o"
    include "$(BUILD_DIR)/src/libu64/pad.o"
    include "$(BUILD_DIR)/src/libu64/rcp_utils.o"
#endif

    // libc64
#if PLATFORM_N64
    include "$(BUILD_DIR)/src/libc64/math64.o"
    include "$(BUILD_DIR)/src/libc64/fp.o"
    include "$(BUILD_DIR)/src/libc64/malloc.o"
    include "$(BUILD_DIR)/src/libc64/qrand.o"
    include "$(BUILD_DIR)/src/libc64/__osMalloc_n64.o"
    include "$(BUILD_DIR)/src/libc64/sprintf.o"
    include "$(BUILD_DIR)/src/libc64/aprintf.o"
#elif PLATFORM_GC
    include "$(BUILD_DIR)/src/libc64/math64.o"
    include "$(BUILD_DIR)/src/libc64/fp.o"
    include "$(BUILD_DIR)/src/libc64/malloc.o"
    include "$(BUILD_DIR)/src/libc64/qrand.o"
    include "$(BUILD_DIR)/src/libc64/__osMalloc_gc.o"
    include "$(BUILD_DIR)/src/libc64/sprintf.o"
    include "$(BUILD_DIR)/src/libc64/aprintf.o"
    include "$(BUILD_DIR)/src/libc64/sleep.o"
#elif PLATFORM_IQUE
    include "$(BUILD_DIR)/src/libc64/__osMalloc_gc.o"
    include "$(BUILD_DIR)/src/libc64/aprintf.o"
    include "$(BUILD_DIR)/src/libc64/malloc.o"
    include "$(BUILD_DIR)/src/libc64/math64.o"
    include "$(BUILD_DIR)/src/libc64/fp.o"
    include "$(BUILD_DIR)/src/libc64/qrand.o"
    include "$(BUILD_DIR)/src/libc64/sleep.o"
    include "$(BUILD_DIR)/src/libc64/sprintf.o"
#endif

    // jpeg
    include "$(BUILD_DIR)/src/code/jpegutils.o"
    include "$(BUILD_DIR)/src/code/jpegdecoder.o"

    // libultra
#if PLATFORM_N64
#include "spec_includes/code_libultra_n64.inc"
#elif PLATFORM_GC
#include "spec_includes/code_libultra_gc.inc"
#elif PLATFORM_IQUE
#include "spec_includes/code_libultra_ique.inc"
#endif

    // libc
    include "$(BUILD_DIR)/src/libc/sqrt.o"
#if !PLATFORM_N64
    include "$(BUILD_DIR)/src/libc/absf.o"
#endif
    include "$(BUILD_DIR)/src/libc/fmodf.o"
    include "$(BUILD_DIR)/src/libc/memset.o"
    include "$(BUILD_DIR)/src/libc/memmove.o"

    // For some reason, the data sections of z_message and z_game_over are
    // placed near the rodata sections of other files, so we first build this
    // combined object before the final link.
    include "$(BUILD_DIR)/src/code/z_message_z_game_over.o"
    include "$(BUILD_DIR)/src/code/z_construct.o"

    // Audio tables
    include "$(BUILD_DIR)/src/audio/tables/soundfont_table.o"
    include "$(BUILD_DIR)/assets/audio/sequence_font_table.o"
    include "$(BUILD_DIR)/src/audio/tables/sequence_table.o"
    include "$(BUILD_DIR)/src/audio/tables/samplebank_table.o"

    // RSP microcode
    include "$(BUILD_DIR)/data/rsp.text.o"
    include "$(BUILD_DIR)/data/rsp.rodata.o"

    // Extra files for non-matching debug builds
#if DEBUG_FEATURES
    include "$(BUILD_DIR)/src/libu64/mtxuty-cvt.o"
    include "$(BUILD_DIR)/src/libultra/io/contpfs.o"
    include "$(BUILD_DIR)/src/libultra/io/pfsallocatefile.o"
    include "$(BUILD_DIR)/src/libultra/io/pfschecker.o"
    include "$(BUILD_DIR)/src/libultra/io/pfsdeletefile.o"
    include "$(BUILD_DIR)/src/libultra/io/pfsfilestate.o"
    include "$(BUILD_DIR)/src/libultra/io/pfsfindfile.o"
    include "$(BUILD_DIR)/src/libultra/io/pfsfreeblocks.o"
    include "$(BUILD_DIR)/src/libultra/io/pfsgetstatus.o"
    include "$(BUILD_DIR)/src/libultra/io/pfsinitpak.o"
    include "$(BUILD_DIR)/src/libultra/io/pfsisplug.o"
    include "$(BUILD_DIR)/src/libultra/io/pfsreadwritefile.o"
#endif

endseg

beginseg
    name "buffers"
    flags NOLOAD
    align 0x40
    include "$(BUILD_DIR)/src/buffers/zbuffer.o"
    include "$(BUILD_DIR)/src/buffers/gfxbuffers.o"
    include "$(BUILD_DIR)/src/buffers/audio_heap.o"
endseg

#if PLATFORM_N64
beginseg
    name "n64dd"
    compress
    align 0x40
    include "$(BUILD_DIR)/src/n64dd/z_n64dd.o"
    include "$(BUILD_DIR)/src/n64dd/n64dd_data_buffer.o"
    include "$(BUILD_DIR)/src/n64dd/n64dd_801C8000.o"
    include "$(BUILD_DIR)/src/n64dd/n64dd_801C8940.o"
    include "$(BUILD_DIR)/src/n64dd/n64dd_801C9440.o"
    include "$(BUILD_DIR)/src/n64dd/n64dd_801C9B70.o"
    include "$(BUILD_DIR)/src/n64dd/n64dd_error_headers.o"
    include "$(BUILD_DIR)/src/n64dd/n64dd_error_bodies.o"
    include "$(BUILD_DIR)/src/n64dd/n64dd_error_textures.o"
    include "$(BUILD_DIR)/src/n64dd/n64dd_801CA0B0.o"
    include "$(BUILD_DIR)/src/libleo/api/readwrite.o"
    include "$(BUILD_DIR)/src/libleo/leo/leofunc.o"
    include "$(BUILD_DIR)/src/libleo/leo/leoram.o"
    include "$(BUILD_DIR)/src/libleo/leo/leoint.o"
    include "$(BUILD_DIR)/src/libleo/leo/leocmdex.o"
    include "$(BUILD_DIR)/src/libleo/api/getaadr2.o"
    include "$(BUILD_DIR)/src/libleo/leo/leoread.o"
    include "$(BUILD_DIR)/src/libleo/api/lbatobyte.o"
    include "$(BUILD_DIR)/src/libleo/leo/leoinquiry.o"
    include "$(BUILD_DIR)/src/libleo/leo/leodiskinit.o"
    include "$(BUILD_DIR)/src/libleo/api/seek.o"
    include "$(BUILD_DIR)/src/libleo/leo/leord_diskid.o"
    include "$(BUILD_DIR)/src/libleo/leo/leomecha.o"
    include "$(BUILD_DIR)/src/libleo/api/spdlmotor.o"
    include "$(BUILD_DIR)/src/libleo/leo/leo_tbl.o"
    include "$(BUILD_DIR)/src/libleo/leo/leotempbuffer.o"
    include "$(BUILD_DIR)/src/libleo/leo/leoc2_syndrome.o"
    include "$(BUILD_DIR)/src/libleo/leo/leoc2ecc.o"
    include "$(BUILD_DIR)/src/libleo/leo/leomseq_tbl.o"
    include "$(BUILD_DIR)/src/libleo/leo/leomotor.o"
    include "$(BUILD_DIR)/src/libleo/api/driveexist.o"
    include "$(BUILD_DIR)/src/libleo/leo/leomode_sel.o"
    include "$(BUILD_DIR)/src/libleo/leo/leord_capa.o"
    include "$(BUILD_DIR)/src/libleo/leo/leoutil.o"
    include "$(BUILD_DIR)/src/libleo/leo/leorezero.o"
    include "$(BUILD_DIR)/src/libleo/api/clearqueue.o"
    include "$(BUILD_DIR)/src/libleo/api/bytetolba.o"
    include "$(BUILD_DIR)/src/libleo/leo/leoreset.o"
    include "$(BUILD_DIR)/src/libleo/leo/leotranslat.o"
    include "$(BUILD_DIR)/src/libleo/leo/leotimer.o"
    include "$(BUILD_DIR)/src/libleo/api/getkadr.o"
    include "$(BUILD_DIR)/src/libleo/api/getaadr.o"
    include "$(BUILD_DIR)/src/libleo/leo/leoglobals.o"
    include "$(BUILD_DIR)/src/libleo/leo/leowrite.o"
    include "$(BUILD_DIR)/src/libleo/api/cjcreateleomanager.o"
    include "$(BUILD_DIR)/src/libleo/leo/leointerrupt.o"
    include "$(BUILD_DIR)/src/libleo/api/cacreateleomanager.o"
    include "$(BUILD_DIR)/src/libleo/api/testunitready.o"
    include "$(BUILD_DIR)/src/libleo/leo/leotestunit.o"
    include "$(BUILD_DIR)/src/libleo/leo/leoseek.o"
endseg
#endif

beginseg
    name "ovl_title"
    compress
    address 0x80800000
    include "$(BUILD_DIR)/src/overlays/gamestates/ovl_title/z_title.o"
    include "$(BUILD_DIR)/src/overlays/gamestates/ovl_title/ovl_title_reloc.o"
endseg

beginseg
    name "ovl_select"
    compress
    include "$(BUILD_DIR)/src/overlays/gamestates/ovl_select/z_select.o"
    include "$(BUILD_DIR)/src/overlays/gamestates/ovl_select/ovl_select_reloc.o"
endseg

beginseg
    name "ovl_opening"
    compress
    include "$(BUILD_DIR)/src/overlays/gamestates/ovl_opening/z_opening.o"
    include "$(BUILD_DIR)/src/overlays/gamestates/ovl_opening/ovl_opening_reloc.o"
endseg

beginseg
    name "ovl_file_choose"
    compress
    include "$(BUILD_DIR)/src/overlays/gamestates/ovl_file_choose/z_file_nameset_data.o"
    include "$(BUILD_DIR)/src/overlays/gamestates/ovl_file_choose/z_file_copy_erase.o"
    include "$(BUILD_DIR)/src/overlays/gamestates/ovl_file_choose/z_file_nameset.o"
    include "$(BUILD_DIR)/src/overlays/gamestates/ovl_file_choose/z_file_choose.o"
    include "$(BUILD_DIR)/src/overlays/gamestates/ovl_file_choose/ovl_file_choose_reloc.o"
endseg

beginseg
    name "ovl_kaleido_scope"
    compress
    include "$(BUILD_DIR)/src/overlays/misc/ovl_kaleido_scope/z_kaleido_collect.o"
    include "$(BUILD_DIR)/src/overlays/misc/ovl_kaleido_scope/z_kaleido_debug.o"
    include "$(BUILD_DIR)/src/overlays/misc/ovl_kaleido_scope/z_kaleido_equipment.o"
    include "$(BUILD_DIR)/src/overlays/misc/ovl_kaleido_scope/z_kaleido_item.o"
    include "$(BUILD_DIR)/src/overlays/misc/ovl_kaleido_scope/z_kaleido_map.o"
    include "$(BUILD_DIR)/src/overlays/misc/ovl_kaleido_scope/z_kaleido_prompt.o"
    include "$(BUILD_DIR)/src/overlays/misc/ovl_kaleido_scope/z_kaleido_scope.o"
    include "$(BUILD_DIR)/src/overlays/misc/ovl_kaleido_scope/z_lmap_mark.o"
#if !OOT_MQ
    include "$(BUILD_DIR)/src/overlays/misc/ovl_kaleido_scope/z_lmap_mark_data.o"
#else
    include "$(BUILD_DIR)/src/overlays/misc/ovl_kaleido_scope/z_lmap_mark_data_mq.o"
#endif
    include "$(BUILD_DIR)/src/overlays/misc/ovl_kaleido_scope/ovl_kaleido_scope_reloc.o"
endseg

beginseg
    name "ovl_player_actor"
    compress
    include "$(BUILD_DIR)/src/overlays/actors/ovl_player_actor/z_player.o"
    include "$(BUILD_DIR)/src/overlays/actors/ovl_player_actor/ovl_player_actor_reloc.o"
endseg

beginseg
    name "ovl_map_mark_data"
    compress
#if !OOT_MQ
    include "$(BUILD_DIR)/src/overlays/misc/ovl_map_mark_data/z_map_mark_data.o"
#else
    include "$(BUILD_DIR)/src/overlays/misc/ovl_map_mark_data/z_map_mark_data_mq.o"
#endif
    include "$(BUILD_DIR)/src/overlays/misc/ovl_map_mark_data/ovl_map_mark_data_reloc.o"
endseg

beginseg
    name "ovl_En_Test"
    compress
    include "$(BUILD_DIR)/src/overlays/actors/ovl_En_Test/z_en_test.o"
    include "$(BUILD_DIR)/src/overlays/actors/ovl_En_Test/ovl_En_Test_reloc.o"
endseg

// Overlays for most actors and effects are reordered between versions. On N64 and iQue,
// the overlays are in some arbitrary order, while on GameCube they are sorted alphabetically.
#if !PLATFORM_GC
#include "spec_includes/overlays_n64_ique.inc"
#else
#include "spec_includes/overlays_gc.inc"
#endif

beginseg
    name "gameplay_keep"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/gameplay_keep/gameplay_keep.o"
    number 4
endseg

beginseg
    name "gameplay_field_keep"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/gameplay_field_keep/gameplay_field_keep.o"
    number 5
endseg

beginseg
    name "gameplay_dangeon_keep"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/gameplay_dangeon_keep/gameplay_dangeon_keep.o"
    number 5
endseg

beginseg
    name "gameplay_object_exchange_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/baserom/gameplay_object_exchange_static.o"
endseg

beginseg
    name "object_link_boy"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_link_boy/object_link_boy.o"
    number 6
endseg

beginseg
    name "object_link_child"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_link_child/object_link_child.o"
    number 6
endseg

beginseg
    name "object_box"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_box/object_box.o"
    number 6
endseg

beginseg
    name "object_human"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_human/object_human.o"
    number 6
endseg

beginseg
    name "object_okuta"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_okuta/object_okuta.o"
    number 6
endseg

beginseg
    name "object_poh"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_poh/object_poh.o"
    number 6
endseg

beginseg
    name "object_wallmaster"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_wallmaster/object_wallmaster.o"
    number 6
endseg

beginseg
    name "object_dy_obj"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_dy_obj/object_dy_obj.o"
    number 6
endseg

beginseg
    name "object_firefly"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_firefly/object_firefly.o"
    number 6
endseg

beginseg
    name "object_dodongo"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_dodongo/object_dodongo.o"
    number 6
endseg

beginseg
    name "object_fire"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_fire/object_fire.o"
    number 6
endseg

beginseg
    name "object_niw"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_niw/object_niw.o"
    number 6
endseg

beginseg
    name "object_tite"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_tite/object_tite.o"
    number 6
endseg

beginseg
    name "object_reeba"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_reeba/object_reeba.o"
    number 6
endseg

beginseg
    name "object_peehat"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_peehat/object_peehat.o"
    number 6
endseg

beginseg
    name "object_kingdodongo"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_kingdodongo/object_kingdodongo.o"
    number 6
endseg

beginseg
    name "object_horse"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_horse/object_horse.o"
    number 6
endseg

beginseg
    name "object_zf"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_zf/object_zf.o"
    number 6
endseg

beginseg
    name "object_goma"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_goma/object_goma.o"
    number 6
endseg

beginseg
    name "object_zl1"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_zl1/object_zl1.o"
    number 6
endseg

beginseg
    name "object_gol"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gol/object_gol.o"
    number 6
endseg

beginseg
    name "object_bubble"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_bubble/object_bubble.o"
    number 6
endseg

beginseg
    name "object_dodojr"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_dodojr/object_dodojr.o"
    number 6
endseg

beginseg
    name "object_torch2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_torch2/object_torch2.o"
    number 6
endseg

beginseg
    name "object_bl"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_bl/object_bl.o"
    number 6
endseg

beginseg
    name "object_tp"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_tp/object_tp.o"
    number 6
endseg

beginseg
    name "object_oA1"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oA1/object_oA1.o"
    number 6
endseg

beginseg
    name "object_st"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_st/object_st.o"
    number 6
endseg

beginseg
    name "object_bw"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_bw/object_bw.o"
    number 6
endseg

beginseg
    name "object_ei"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ei/object_ei.o"
    number 6
endseg

beginseg
    name "object_horse_normal"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_horse_normal/object_horse_normal.o"
    number 6
endseg

beginseg
    name "object_oB1"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oB1/object_oB1.o"
    number 6
endseg

beginseg
    name "object_o_anime"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_o_anime/object_o_anime.o"
    number 6
endseg

beginseg
    name "object_spot04_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot04_objects/object_spot04_objects.o"
    number 6
endseg

beginseg
    name "object_ddan_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ddan_objects/object_ddan_objects.o"
    number 6
endseg

beginseg
    name "object_hidan_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_hidan_objects/object_hidan_objects.o"
    number 6
endseg

beginseg
    name "object_horse_ganon"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_horse_ganon/object_horse_ganon.o"
    number 6
endseg

beginseg
    name "object_oA2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oA2/object_oA2.o"
    number 6
endseg

beginseg
    name "object_spot00_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot00_objects/object_spot00_objects.o"
    number 6
endseg

beginseg
    name "object_mb"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mb/object_mb.o"
    number 6
endseg

beginseg
    name "object_bombf"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_bombf/object_bombf.o"
    number 6
endseg

beginseg
    name "object_sk2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_sk2/object_sk2.o"
    number 6
endseg

beginseg
    name "object_oE1"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oE1/object_oE1.o"
    number 6
endseg

beginseg
    name "object_oE_anime"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oE_anime/object_oE_anime.o"
    number 6
endseg

beginseg
    name "object_oE2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oE2/object_oE2.o"
    number 6
endseg

beginseg
    name "object_ydan_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ydan_objects/object_ydan_objects.o"
    number 6
endseg

beginseg
    name "object_gnd"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gnd/object_gnd.o"
    number 6
endseg

beginseg
    name "object_am"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_am/object_am.o"
    number 6
endseg

beginseg
    name "object_dekubaba"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_dekubaba/object_dekubaba.o"
    number 6
endseg

beginseg
    name "object_oA3"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oA3/object_oA3.o"
    number 6
endseg

beginseg
    name "object_oA4"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oA4/object_oA4.o"
    number 6
endseg

beginseg
    name "object_oA5"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oA5/object_oA5.o"
    number 6
endseg

beginseg
    name "object_oA6"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oA6/object_oA6.o"
    number 6
endseg

beginseg
    name "object_oA7"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oA7/object_oA7.o"
    number 6
endseg

beginseg
    name "object_jj"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_jj/object_jj.o"
    number 6
endseg

beginseg
    name "object_oA8"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oA8/object_oA8.o"
    number 6
endseg

beginseg
    name "object_oA9"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oA9/object_oA9.o"
    number 6
endseg

beginseg
    name "object_oB2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oB2/object_oB2.o"
    number 6
endseg

beginseg
    name "object_oB3"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oB3/object_oB3.o"
    number 6
endseg

beginseg
    name "object_oB4"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oB4/object_oB4.o"
    number 6
endseg

beginseg
    name "object_horse_zelda"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_horse_zelda/object_horse_zelda.o"
    number 6
endseg

beginseg
    name "object_opening_demo1"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_opening_demo1/object_opening_demo1.o"
    number 6
endseg

beginseg
    name "object_warp1"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_warp1/object_warp1.o"
    number 6
endseg

beginseg
    name "object_b_heart"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_b_heart/object_b_heart.o"
    number 6
endseg

beginseg
    name "object_dekunuts"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_dekunuts/object_dekunuts.o"
    number 6
endseg

beginseg
    name "object_oE3"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oE3/object_oE3.o"
    number 6
endseg

beginseg
    name "object_oE4"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oE4/object_oE4.o"
    number 6
endseg

beginseg
    name "object_menkuri_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_menkuri_objects/object_menkuri_objects.o"
    number 6
endseg

beginseg
    name "object_oE5"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oE5/object_oE5.o"
    number 6
endseg

beginseg
    name "object_oE6"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oE6/object_oE6.o"
    number 6
endseg

beginseg
    name "object_oE7"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oE7/object_oE7.o"
    number 6
endseg

beginseg
    name "object_oE8"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oE8/object_oE8.o"
    number 6
endseg

beginseg
    name "object_oE9"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oE9/object_oE9.o"
    number 6
endseg

beginseg
    name "object_oE10"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oE10/object_oE10.o"
    number 6
endseg

beginseg
    name "object_oE11"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oE11/object_oE11.o"
    number 6
endseg

beginseg
    name "object_oE12"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oE12/object_oE12.o"
    number 6
endseg

beginseg
    name "object_vali"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_vali/object_vali.o"
    number 6
endseg

beginseg
    name "object_oA10"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oA10/object_oA10.o"
    number 6
endseg

beginseg
    name "object_oA11"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oA11/object_oA11.o"
    number 6
endseg

beginseg
    name "object_mizu_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mizu_objects/object_mizu_objects.o"
    number 6
endseg

beginseg
    name "object_fhg"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_fhg/object_fhg.o"
    number 6
endseg

beginseg
    name "object_ossan"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ossan/object_ossan.o"
    number 6
endseg

beginseg
    name "object_mori_hineri1"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mori_hineri1/object_mori_hineri1.o"
    number 6
endseg

beginseg
    name "object_Bb"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_Bb/object_Bb.o"
    number 6
endseg

beginseg
    name "object_toki_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_toki_objects/object_toki_objects.o"
    number 6
endseg

beginseg
    name "object_yukabyun"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_yukabyun/object_yukabyun.o"
    number 6
endseg

beginseg
    name "object_zl2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_zl2/object_zl2.o"
    number 6
endseg

beginseg
    name "object_mjin"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mjin/object_mjin.o"
    number 6
endseg

beginseg
    name "object_mjin_flash"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mjin_flash/object_mjin_flash.o"
    number 6
endseg

beginseg
    name "object_mjin_dark"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mjin_dark/object_mjin_dark.o"
    number 6
endseg

beginseg
    name "object_mjin_flame"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mjin_flame/object_mjin_flame.o"
    number 6
endseg

beginseg
    name "object_mjin_ice"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mjin_ice/object_mjin_ice.o"
    number 6
endseg

beginseg
    name "object_mjin_soul"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mjin_soul/object_mjin_soul.o"
    number 6
endseg

beginseg
    name "object_mjin_wind"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mjin_wind/object_mjin_wind.o"
    number 6
endseg

beginseg
    name "object_mjin_oka"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mjin_oka/object_mjin_oka.o"
    number 6
endseg

beginseg
    name "object_haka_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_haka_objects/object_haka_objects.o"
    number 6
endseg

beginseg
    name "object_spot06_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot06_objects/object_spot06_objects.o"
    number 6
endseg

beginseg
    name "object_ice_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ice_objects/object_ice_objects.o"
    number 6
endseg

beginseg
    name "object_relay_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_relay_objects/object_relay_objects.o"
    number 6
endseg

beginseg
    name "object_mori_hineri1a"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mori_hineri1a/object_mori_hineri1a.o"
    number 6
endseg

beginseg
    name "object_mori_hineri2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mori_hineri2/object_mori_hineri2.o"
    number 6
endseg

beginseg
    name "object_mori_hineri2a"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mori_hineri2a/object_mori_hineri2a.o"
    number 6
endseg

beginseg
    name "object_mori_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mori_objects/object_mori_objects.o"
    number 6
endseg

beginseg
    name "object_mori_tex"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mori_tex/object_mori_tex.o"
    number 8
endseg

beginseg
    name "object_spot08_obj"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot08_obj/object_spot08_obj.o"
    number 6
endseg

beginseg
    name "object_warp2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_warp2/object_warp2.o"
    number 6
endseg

beginseg
    name "object_hata"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_hata/object_hata.o"
    number 6
endseg

beginseg
    name "object_bird"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_bird/object_bird.o"
    number 6
endseg

beginseg
    name "object_wood02"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_wood02/object_wood02.o"
    number 6
endseg

beginseg
    name "object_lightbox"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_lightbox/object_lightbox.o"
    number 6
endseg

beginseg
    name "object_pu_box"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_pu_box/object_pu_box.o"
    number 6
endseg

beginseg
    name "object_trap"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_trap/object_trap.o"
    number 6
endseg

beginseg
    name "object_vase"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_vase/object_vase.o"
    number 6
endseg

beginseg
    name "object_im"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_im/object_im.o"
    number 6
endseg

beginseg
    name "object_ta"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ta/object_ta.o"
    number 6
endseg

beginseg
    name "object_tk"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_tk/object_tk.o"
    number 6
endseg

beginseg
    name "object_xc"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_xc/object_xc.o"
    number 6
endseg

beginseg
    name "object_vm"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_vm/object_vm.o"
    number 6
endseg

beginseg
    name "object_bv"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_bv/object_bv.o"
    number 6
endseg

beginseg
    name "object_hakach_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_hakach_objects/object_hakach_objects.o"
    number 6
endseg

beginseg
    name "object_efc_crystal_light"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_efc_crystal_light/object_efc_crystal_light.o"
    number 6
endseg

beginseg
    name "object_efc_fire_ball"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_efc_fire_ball/object_efc_fire_ball.o"
    number 6
endseg

beginseg
    name "object_efc_flash"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_efc_flash/object_efc_flash.o"
    number 6
endseg

beginseg
    name "object_efc_lgt_shower"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_efc_lgt_shower/object_efc_lgt_shower.o"
    number 6
endseg

beginseg
    name "object_efc_star_field"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_efc_star_field/object_efc_star_field.o"
    number 6
endseg

beginseg
    name "object_god_lgt"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_god_lgt/object_god_lgt.o"
    number 6
endseg

beginseg
    name "object_light_ring"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_light_ring/object_light_ring.o"
    number 6
endseg

beginseg
    name "object_triforce_spot"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_triforce_spot/object_triforce_spot.o"
    number 6
endseg

beginseg
    name "object_medal"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_medal/object_medal.o"
    number 6
endseg

beginseg
    name "object_bdan_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_bdan_objects/object_bdan_objects.o"
    number 6
endseg

beginseg
    name "object_sd"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_sd/object_sd.o"
    number 6
endseg

beginseg
    name "object_rd"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_rd/object_rd.o"
    number 6
endseg

beginseg
    name "object_po_sisters"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_po_sisters/object_po_sisters.o"
    number 6
endseg

beginseg
    name "object_heavy_object"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_heavy_object/object_heavy_object.o"
    number 6
endseg

beginseg
    name "object_gndd"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gndd/object_gndd.o"
    number 6
endseg

beginseg
    name "object_fd"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_fd/object_fd.o"
    number 6
endseg

beginseg
    name "object_du"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_du/object_du.o"
    number 6
endseg

beginseg
    name "object_fw"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_fw/object_fw.o"
    number 6
endseg

beginseg
    name "object_horse_link_child"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_horse_link_child/object_horse_link_child.o"
    number 6
endseg

beginseg
    name "object_spot02_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot02_objects/object_spot02_objects.o"
    number 6
endseg

beginseg
    name "object_haka"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_haka/object_haka.o"
    number 6
endseg

beginseg
    name "object_ru1"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ru1/object_ru1.o"
    number 6
endseg

beginseg
    name "object_syokudai"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_syokudai/object_syokudai.o"
    number 6
endseg

beginseg
    name "object_fd2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_fd2/object_fd2.o"
    number 6
endseg

beginseg
    name "object_dh"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_dh/object_dh.o"
    number 6
endseg

beginseg
    name "object_rl"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_rl/object_rl.o"
    number 6
endseg

beginseg
    name "object_efc_tw"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_efc_tw/object_efc_tw.o"
    number 6
endseg

beginseg
    name "object_demo_tre_lgt"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_demo_tre_lgt/object_demo_tre_lgt.o"
    number 6
endseg

beginseg
    name "object_gi_key"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_key/object_gi_key.o"
    number 6
endseg

beginseg
    name "object_mir_ray"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mir_ray/object_mir_ray.o"
    number 6
endseg

beginseg
    name "object_brob"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_brob/object_brob.o"
    number 6
endseg

beginseg
    name "object_gi_jewel"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_jewel/object_gi_jewel.o"
    number 6
endseg

beginseg
    name "object_spot09_obj"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot09_obj/object_spot09_obj.o"
    number 6
endseg

beginseg
    name "object_spot18_obj"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot18_obj/object_spot18_obj.o"
    number 6
endseg

beginseg
    name "object_bdoor"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_bdoor/object_bdoor.o"
    number 6
endseg

beginseg
    name "object_spot17_obj"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot17_obj/object_spot17_obj.o"
    number 6
endseg

beginseg
    name "object_shop_dungen"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_shop_dungen/object_shop_dungen.o"
    number 6
endseg

beginseg
    name "object_nb"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_nb/object_nb.o"
    number 6
endseg

beginseg
    name "object_mo"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mo/object_mo.o"
    number 6
endseg

beginseg
    name "object_sb"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_sb/object_sb.o"
    number 6
endseg

beginseg
    name "object_gi_melody"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_melody/object_gi_melody.o"
    number 6
endseg

beginseg
    name "object_gi_heart"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_heart/object_gi_heart.o"
    number 6
endseg

beginseg
    name "object_gi_compass"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_compass/object_gi_compass.o"
    number 6
endseg

beginseg
    name "object_gi_bosskey"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_bosskey/object_gi_bosskey.o"
    number 6
endseg

beginseg
    name "object_gi_medal"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_medal/object_gi_medal.o"
    number 6
endseg

beginseg
    name "object_gi_nuts"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_nuts/object_gi_nuts.o"
    number 6
endseg

beginseg
    name "object_sa"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_sa/object_sa.o"
    number 6
endseg

beginseg
    name "object_gi_hearts"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_hearts/object_gi_hearts.o"
    number 6
endseg

beginseg
    name "object_gi_arrowcase"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_arrowcase/object_gi_arrowcase.o"
    number 6
endseg

beginseg
    name "object_gi_bombpouch"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_bombpouch/object_gi_bombpouch.o"
    number 6
endseg

beginseg
    name "object_in"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_in/object_in.o"
    number 6
endseg

beginseg
    name "object_tr"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_tr/object_tr.o"
    number 6
endseg

beginseg
    name "object_spot16_obj"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot16_obj/object_spot16_obj.o"
    number 6
endseg

beginseg
    name "object_oE1s"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oE1s/object_oE1s.o"
    number 6
endseg

beginseg
    name "object_oE4s"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oE4s/object_oE4s.o"
    number 6
endseg

beginseg
    name "object_os_anime"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_os_anime/object_os_anime.o"
    number 6
endseg

beginseg
    name "object_gi_bottle"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_bottle/object_gi_bottle.o"
    number 6
endseg

beginseg
    name "object_gi_stick"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_stick/object_gi_stick.o"
    number 6
endseg

beginseg
    name "object_gi_map"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_map/object_gi_map.o"
    number 6
endseg

beginseg
    name "object_oF1d_map"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oF1d_map/object_oF1d_map.o"
    number 6
endseg

beginseg
    name "object_ru2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ru2/object_ru2.o"
    number 6
endseg

beginseg
    name "object_gi_shield_1"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_shield_1/object_gi_shield_1.o"
    number 6
endseg

beginseg
    name "object_dekujr"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_dekujr/object_dekujr.o"
    number 6
endseg

beginseg
    name "object_gi_magicpot"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_magicpot/object_gi_magicpot.o"
    number 6
endseg

beginseg
    name "object_gi_bomb_1"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_bomb_1/object_gi_bomb_1.o"
    number 6
endseg

beginseg
    name "object_oF1s"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_oF1s/object_oF1s.o"
    number 6
endseg

beginseg
    name "object_ma2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ma2/object_ma2.o"
    number 6
endseg

beginseg
    name "object_gi_purse"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_purse/object_gi_purse.o"
    number 6
endseg

beginseg
    name "object_hni"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_hni/object_hni.o"
    number 6
endseg

beginseg
    name "object_tw"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_tw/object_tw.o"
    number 6
endseg

beginseg
    name "object_rr"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_rr/object_rr.o"
    number 6
endseg

beginseg
    name "object_bxa"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_bxa/object_bxa.o"
    number 6
endseg

beginseg
    name "object_anubice"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_anubice/object_anubice.o"
    number 6
endseg

beginseg
    name "object_gi_gerudo"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_gerudo/object_gi_gerudo.o"
    number 6
endseg

beginseg
    name "object_gi_arrow"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_arrow/object_gi_arrow.o"
    number 6
endseg

beginseg
    name "object_gi_bomb_2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_bomb_2/object_gi_bomb_2.o"
    number 6
endseg

beginseg
    name "object_gi_egg"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_egg/object_gi_egg.o"
    number 6
endseg

beginseg
    name "object_gi_scale"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_scale/object_gi_scale.o"
    number 6
endseg

beginseg
    name "object_gi_shield_2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_shield_2/object_gi_shield_2.o"
    number 6
endseg

beginseg
    name "object_gi_hookshot"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_hookshot/object_gi_hookshot.o"
    number 6
endseg

beginseg
    name "object_gi_ocarina"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_ocarina/object_gi_ocarina.o"
    number 6
endseg

beginseg
    name "object_gi_milk"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_milk/object_gi_milk.o"
    number 6
endseg

beginseg
    name "object_ma1"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ma1/object_ma1.o"
    number 6
endseg

beginseg
    name "object_ganon"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ganon/object_ganon.o"
    number 6
endseg

beginseg
    name "object_sst"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_sst/object_sst.o"
    number 6
endseg

beginseg
    name "object_ny"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ny/object_ny.o"
    number 6
endseg

beginseg
    name "object_fr"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_fr/object_fr.o"
    number 6
endseg

beginseg
    name "object_gi_pachinko"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_pachinko/object_gi_pachinko.o"
    number 6
endseg

beginseg
    name "object_gi_boomerang"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_boomerang/object_gi_boomerang.o"
    number 6
endseg

beginseg
    name "object_gi_bow"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_bow/object_gi_bow.o"
    number 6
endseg

beginseg
    name "object_gi_glasses"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_glasses/object_gi_glasses.o"
    number 6
endseg

beginseg
    name "object_gi_liquid"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_liquid/object_gi_liquid.o"
    number 6
endseg

beginseg
    name "object_ani"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ani/object_ani.o"
    number 6
endseg

beginseg
    name "object_demo_6k"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_demo_6k/object_demo_6k.o"
    number 6
endseg

beginseg
    name "object_gi_shield_3"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_shield_3/object_gi_shield_3.o"
    number 6
endseg

beginseg
    name "object_gi_letter"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_letter/object_gi_letter.o"
    number 6
endseg

beginseg
    name "object_spot15_obj"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot15_obj/object_spot15_obj.o"
    number 6
endseg

beginseg
    name "object_jya_obj"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_jya_obj/object_jya_obj.o"
    number 6
endseg

beginseg
    name "object_gi_clothes"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_clothes/object_gi_clothes.o"
    number 6
endseg

beginseg
    name "object_gi_bean"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_bean/object_gi_bean.o"
    number 6
endseg

beginseg
    name "object_gi_fish"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_fish/object_gi_fish.o"
    number 6
endseg

beginseg
    name "object_gi_saw"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_saw/object_gi_saw.o"
    number 6
endseg

beginseg
    name "object_gi_hammer"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_hammer/object_gi_hammer.o"
    number 6
endseg

beginseg
    name "object_gi_grass"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_grass/object_gi_grass.o"
    number 6
endseg

beginseg
    name "object_gi_longsword"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_longsword/object_gi_longsword.o"
    number 6
endseg

beginseg
    name "object_spot01_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot01_objects/object_spot01_objects.o"
    number 6
endseg

beginseg
    name "object_md"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_md/object_md.o"
    number 6
endseg

beginseg
    name "object_km1"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_km1/object_km1.o"
    number 6
endseg

beginseg
    name "object_kw1"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_kw1/object_kw1.o"
    number 6
endseg

beginseg
    name "object_zo"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_zo/object_zo.o"
    number 6
endseg

beginseg
    name "object_kz"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_kz/object_kz.o"
    number 6
endseg

beginseg
    name "object_umajump"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_umajump/object_umajump.o"
    number 6
endseg

beginseg
    name "object_masterkokiri"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_masterkokiri/object_masterkokiri.o"
    number 6
endseg

beginseg
    name "object_masterkokirihead"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_masterkokirihead/object_masterkokirihead.o"
    number 6
endseg

beginseg
    name "object_mastergolon"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mastergolon/object_mastergolon.o"
    number 6
endseg

beginseg
    name "object_masterzoora"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_masterzoora/object_masterzoora.o"
    number 6
endseg

beginseg
    name "object_aob"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_aob/object_aob.o"
    number 6
endseg

beginseg
    name "object_ik"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ik/object_ik.o"
    number 6
endseg

beginseg
    name "object_ahg"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ahg/object_ahg.o"
    number 6
endseg

beginseg
    name "object_cne"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_cne/object_cne.o"
    number 6
endseg

beginseg
    name "object_gi_niwatori"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_niwatori/object_gi_niwatori.o"
    number 6
endseg

beginseg
    name "object_skj"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_skj/object_skj.o"
    number 6
endseg

beginseg
    name "object_gi_bottle_letter"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_bottle_letter/object_gi_bottle_letter.o"
    number 6
endseg

beginseg
    name "object_bji"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_bji/object_bji.o"
    number 6
endseg

beginseg
    name "object_bba"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_bba/object_bba.o"
    number 6
endseg

beginseg
    name "object_gi_ocarina_0"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_ocarina_0/object_gi_ocarina_0.o"
    number 6
endseg

beginseg
    name "object_ds"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ds/object_ds.o"
    number 6
endseg

beginseg
    name "object_ane"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ane/object_ane.o"
    number 6
endseg

beginseg
    name "object_boj"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_boj/object_boj.o"
    number 6
endseg

beginseg
    name "object_spot03_object"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot03_object/object_spot03_object.o"
    number 6
endseg

beginseg
    name "object_spot07_object"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot07_object/object_spot07_object.o"
    number 6
endseg

beginseg
    name "object_fz"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_fz/object_fz.o"
    number 6
endseg

beginseg
    name "object_bob"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_bob/object_bob.o"
    number 6
endseg

beginseg
    name "object_ge1"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ge1/object_ge1.o"
    number 6
endseg

beginseg
    name "object_yabusame_point"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_yabusame_point/object_yabusame_point.o"
    number 6
endseg

beginseg
    name "object_gi_boots_2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_boots_2/object_gi_boots_2.o"
    number 6
endseg

beginseg
    name "object_gi_seed"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_seed/object_gi_seed.o"
    number 6
endseg

beginseg
    name "object_gnd_magic"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gnd_magic/object_gnd_magic.o"
    number 6
endseg

beginseg
    name "object_d_elevator"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_d_elevator/object_d_elevator.o"
    number 6
endseg

beginseg
    name "object_d_hsblock"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_d_hsblock/object_d_hsblock.o"
    number 6
endseg

beginseg
    name "object_d_lift"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_d_lift/object_d_lift.o"
    number 6
endseg

beginseg
    name "object_mamenoki"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mamenoki/object_mamenoki.o"
    number 6
endseg

beginseg
    name "object_goroiwa"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_goroiwa/object_goroiwa.o"
    number 6
endseg

beginseg
    name "object_toryo"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_toryo/object_toryo.o"
    number 6
endseg

beginseg
    name "object_daiku"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_daiku/object_daiku.o"
    number 6
endseg

beginseg
    name "object_nwc"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_nwc/object_nwc.o"
    number 6
endseg

beginseg
    name "object_blkobj"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_blkobj/object_blkobj.o"
    number 6
endseg

beginseg
    name "object_gm"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gm/object_gm.o"
    number 6
endseg

beginseg
    name "object_ms"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ms/object_ms.o"
    number 6
endseg

beginseg
    name "object_hs"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_hs/object_hs.o"
    number 6
endseg

beginseg
    name "object_ingate"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ingate/object_ingate.o"
    number 6
endseg

beginseg
    name "object_lightswitch"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_lightswitch/object_lightswitch.o"
    number 6
endseg

beginseg
    name "object_kusa"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_kusa/object_kusa.o"
    number 6
endseg

beginseg
    name "object_tsubo"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_tsubo/object_tsubo.o"
    number 6
endseg

beginseg
    name "object_gi_gloves"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_gloves/object_gi_gloves.o"
    number 6
endseg

beginseg
    name "object_gi_coin"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_coin/object_gi_coin.o"
    number 6
endseg

beginseg
    name "object_kanban"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_kanban/object_kanban.o"
    number 6
endseg

beginseg
    name "object_gjyo_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gjyo_objects/object_gjyo_objects.o"
    number 6
endseg

beginseg
    name "object_owl"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_owl/object_owl.o"
    number 6
endseg

beginseg
    name "object_mk"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mk/object_mk.o"
    number 6
endseg

beginseg
    name "object_fu"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_fu/object_fu.o"
    number 6
endseg

beginseg
    name "object_gi_ki_tan_mask"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_ki_tan_mask/object_gi_ki_tan_mask.o"
    number 6
endseg

beginseg
    name "object_gi_redead_mask"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_redead_mask/object_gi_redead_mask.o"
    number 6
endseg

beginseg
    name "object_gi_skj_mask"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_skj_mask/object_gi_skj_mask.o"
    number 6
endseg

beginseg
    name "object_gi_rabit_mask"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_rabit_mask/object_gi_rabit_mask.o"
    number 6
endseg

beginseg
    name "object_gi_truth_mask"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_truth_mask/object_gi_truth_mask.o"
    number 6
endseg

beginseg
    name "object_ganon_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ganon_objects/object_ganon_objects.o"
    number 6
endseg

beginseg
    name "object_siofuki"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_siofuki/object_siofuki.o"
    number 6
endseg

beginseg
    name "object_stream"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_stream/object_stream.o"
    number 6
endseg

beginseg
    name "object_mm"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mm/object_mm.o"
    number 6
endseg

beginseg
    name "object_fa"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_fa/object_fa.o"
    number 6
endseg

beginseg
    name "object_os"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_os/object_os.o"
    number 6
endseg

beginseg
    name "object_gi_eye_lotion"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_eye_lotion/object_gi_eye_lotion.o"
    number 6
endseg

beginseg
    name "object_gi_powder"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_powder/object_gi_powder.o"
    number 6
endseg

beginseg
    name "object_gi_mushroom"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_mushroom/object_gi_mushroom.o"
    number 6
endseg

beginseg
    name "object_gi_ticketstone"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_ticketstone/object_gi_ticketstone.o"
    number 6
endseg

beginseg
    name "object_gi_brokensword"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_brokensword/object_gi_brokensword.o"
    number 6
endseg

beginseg
    name "object_js"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_js/object_js.o"
    number 6
endseg

beginseg
    name "object_cs"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_cs/object_cs.o"
    number 6
endseg

beginseg
    name "object_gi_prescription"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_prescription/object_gi_prescription.o"
    number 6
endseg

beginseg
    name "object_gi_bracelet"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_bracelet/object_gi_bracelet.o"
    number 6
endseg

beginseg
    name "object_gi_soldout"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_soldout/object_gi_soldout.o"
    number 6
endseg

beginseg
    name "object_gi_frog"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_frog/object_gi_frog.o"
    number 6
endseg

beginseg
    name "object_mag"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mag/object_mag.o"
    number 6
endseg

beginseg
    name "object_door_gerudo"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_door_gerudo/object_door_gerudo.o"
    number 6
endseg

beginseg
    name "object_gt"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gt/object_gt.o"
    number 6
endseg

beginseg
    name "object_efc_erupc"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_efc_erupc/object_efc_erupc.o"
    number 6
endseg

beginseg
    name "object_zl2_anime1"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_zl2_anime1/object_zl2_anime1.o"
    number 6
endseg

beginseg
    name "object_zl2_anime2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_zl2_anime2/object_zl2_anime2.o"
    number 6
endseg

beginseg
    name "object_gi_golonmask"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_golonmask/object_gi_golonmask.o"
    number 6
endseg

beginseg
    name "object_gi_zoramask"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_zoramask/object_gi_zoramask.o"
    number 6
endseg

beginseg
    name "object_gi_gerudomask"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_gerudomask/object_gi_gerudomask.o"
    number 6
endseg

beginseg
    name "object_ganon2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ganon2/object_ganon2.o"
    number 6
endseg

beginseg
    name "object_ka"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ka/object_ka.o"
    number 6
endseg

beginseg
    name "object_ts"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ts/object_ts.o"
    number 6
endseg

beginseg
    name "object_zg"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_zg/object_zg.o"
    number 6
endseg

beginseg
    name "object_gi_hoverboots"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_hoverboots/object_gi_hoverboots.o"
    number 6
endseg

beginseg
    name "object_gi_m_arrow"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_m_arrow/object_gi_m_arrow.o"
    number 6
endseg

beginseg
    name "object_ds2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ds2/object_ds2.o"
    number 6
endseg

beginseg
    name "object_ec"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ec/object_ec.o"
    number 6
endseg

beginseg
    name "object_fish"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_fish/object_fish.o"
    number 6
endseg

beginseg
    name "object_gi_sutaru"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_sutaru/object_gi_sutaru.o"
    number 6
endseg

beginseg
    name "object_gi_goddess"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_goddess/object_gi_goddess.o"
    number 6
endseg

beginseg
    name "object_ssh"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ssh/object_ssh.o"
    number 6
endseg

beginseg
    name "object_bigokuta"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_bigokuta/object_bigokuta.o"
    number 6
endseg

beginseg
    name "object_bg"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_bg/object_bg.o"
    number 6
endseg

beginseg
    name "object_spot05_objects"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot05_objects/object_spot05_objects.o"
    number 6
endseg

beginseg
    name "object_spot12_obj"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot12_obj/object_spot12_obj.o"
    number 6
endseg

beginseg
    name "object_bombiwa"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_bombiwa/object_bombiwa.o"
    number 6
endseg

beginseg
    name "object_hintnuts"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_hintnuts/object_hintnuts.o"
    number 6
endseg

beginseg
    name "object_rs"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_rs/object_rs.o"
    number 6
endseg

beginseg
    name "object_spot00_break"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot00_break/object_spot00_break.o"
    number 6
endseg

beginseg
    name "object_gla"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gla/object_gla.o"
    number 6
endseg

beginseg
    name "object_shopnuts"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_shopnuts/object_shopnuts.o"
    number 6
endseg

beginseg
    name "object_geldb"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_geldb/object_geldb.o"
    number 6
endseg

beginseg
    name "object_gr"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gr/object_gr.o"
    number 6
endseg

beginseg
    name "object_dog"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_dog/object_dog.o"
    number 6
endseg

beginseg
    name "object_jya_iron"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_jya_iron/object_jya_iron.o"
    number 6
endseg

beginseg
    name "object_jya_door"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_jya_door/object_jya_door.o"
    number 6
endseg

beginseg
    name "object_spot01_objects2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot01_objects2/object_spot01_objects2.o"
    number 6
endseg

beginseg
    name "object_spot11_obj"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot11_obj/object_spot11_obj.o"
    number 6
endseg

beginseg
    name "object_kibako2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_kibako2/object_kibako2.o"
    number 6
endseg

beginseg
    name "object_dns"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_dns/object_dns.o"
    number 6
endseg

beginseg
    name "object_dnk"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_dnk/object_dnk.o"
    number 6
endseg

beginseg
    name "object_gi_fire"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_fire/object_gi_fire.o"
    number 6
endseg

beginseg
    name "object_gi_insect"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_insect/object_gi_insect.o"
    number 6
endseg

beginseg
    name "object_gi_butterfly"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_butterfly/object_gi_butterfly.o"
    number 6
endseg

beginseg
    name "object_gi_ghost"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_ghost/object_gi_ghost.o"
    number 6
endseg

beginseg
    name "object_gi_soul"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_soul/object_gi_soul.o"
    number 6
endseg

beginseg
    name "object_bowl"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_bowl/object_bowl.o"
    number 6
endseg

beginseg
    name "object_po_field"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_po_field/object_po_field.o"
    number 6
endseg

beginseg
    name "object_demo_kekkai"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_demo_kekkai/object_demo_kekkai.o"
    number 6
endseg

beginseg
    name "object_efc_doughnut"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_efc_doughnut/object_efc_doughnut.o"
    number 6
endseg

beginseg
    name "object_gi_dekupouch"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_dekupouch/object_gi_dekupouch.o"
    number 6
endseg

beginseg
    name "object_ganon_anime1"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ganon_anime1/object_ganon_anime1.o"
    number 6
endseg

beginseg
    name "object_ganon_anime2"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ganon_anime2/object_ganon_anime2.o"
    number 6
endseg

beginseg
    name "object_ganon_anime3"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ganon_anime3/object_ganon_anime3.o"
    number 6
endseg

beginseg
    name "object_gi_rupy"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_rupy/object_gi_rupy.o"
    number 6
endseg

beginseg
    name "object_spot01_matoya"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot01_matoya/object_spot01_matoya.o"
    number 6
endseg

beginseg
    name "object_spot01_matoyab"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_spot01_matoyab/object_spot01_matoyab.o"
    number 6
endseg

beginseg
    name "object_po_composer"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_po_composer/object_po_composer.o"
    number 6
endseg

beginseg
    name "object_mu"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_mu/object_mu.o"
    number 6
endseg

beginseg
    name "object_wf"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_wf/object_wf.o"
    number 6
endseg

beginseg
    name "object_skb"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_skb/object_skb.o"
    number 6
endseg

beginseg
    name "object_gj"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gj/object_gj.o"
    number 6
endseg

beginseg
    name "object_geff"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_geff/object_geff.o"
    number 6
endseg

beginseg
    name "object_haka_door"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_haka_door/object_haka_door.o"
    number 6
endseg

beginseg
    name "object_gs"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gs/object_gs.o"
    number 6
endseg

beginseg
    name "object_ps"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ps/object_ps.o"
    number 6
endseg

beginseg
    name "object_bwall"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_bwall/object_bwall.o"
    number 6
endseg

beginseg
    name "object_crow"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_crow/object_crow.o"
    number 6
endseg

beginseg
    name "object_cow"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_cow/object_cow.o"
    number 6
endseg

beginseg
    name "object_cob"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_cob/object_cob.o"
    number 6
endseg

beginseg
    name "object_gi_sword_1"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_gi_sword_1/object_gi_sword_1.o"
    number 6
endseg

beginseg
    name "object_door_killer"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_door_killer/object_door_killer.o"
    number 6
endseg

beginseg
    name "object_ouke_haka"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_ouke_haka/object_ouke_haka.o"
    number 6
endseg

beginseg
    name "object_timeblock"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_timeblock/object_timeblock.o"
    number 6
endseg

beginseg
    name "object_zl4"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/objects/object_zl4/object_zl4.o"
    number 6
endseg

beginseg
    name "g_pn_01"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_01.o"
endseg

beginseg
    name "g_pn_02"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_02.o"
endseg

beginseg
    name "g_pn_03"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_03.o"
endseg

beginseg
    name "g_pn_04"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_04.o"
endseg

beginseg
    name "g_pn_05"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_05.o"
endseg

beginseg
    name "g_pn_06"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_06.o"
endseg

beginseg
    name "g_pn_07"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_07.o"
endseg

beginseg
    name "g_pn_08"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_08.o"
endseg

beginseg
    name "g_pn_09"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_09.o"
endseg

beginseg
    name "g_pn_10"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_10.o"
endseg

beginseg
    name "g_pn_11"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_11.o"
endseg

beginseg
    name "g_pn_12"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_12.o"
endseg

beginseg
    name "g_pn_13"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_13.o"
endseg

beginseg
    name "g_pn_14"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_14.o"
endseg

beginseg
    name "g_pn_15"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_15.o"
endseg

beginseg
    name "g_pn_16"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_16.o"
endseg

beginseg
    name "g_pn_17"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_17.o"
endseg

beginseg
    name "g_pn_18"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_18.o"
endseg

beginseg
    name "g_pn_19"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_19.o"
endseg

beginseg
    name "g_pn_20"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_20.o"
endseg

beginseg
    name "g_pn_21"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_21.o"
endseg

beginseg
    name "g_pn_22"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_22.o"
endseg

beginseg
    name "g_pn_23"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_23.o"
endseg

beginseg
    name "g_pn_24"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_24.o"
endseg

beginseg
    name "g_pn_25"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_25.o"
endseg

beginseg
    name "g_pn_26"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_26.o"
endseg

beginseg
    name "g_pn_27"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_27.o"
endseg

beginseg
    name "g_pn_28"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_28.o"
endseg

beginseg
    name "g_pn_29"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_29.o"
endseg

beginseg
    name "g_pn_30"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_30.o"
endseg

beginseg
    name "g_pn_31"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_31.o"
endseg

beginseg
    name "g_pn_32"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_32.o"
endseg

beginseg
    name "g_pn_33"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_33.o"
endseg

beginseg
    name "g_pn_34"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_34.o"
endseg

beginseg
    name "g_pn_35"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_35.o"
endseg

beginseg
    name "g_pn_36"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_36.o"
endseg

beginseg
    name "g_pn_37"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_37.o"
endseg

beginseg
    name "g_pn_38"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_38.o"
endseg

beginseg
    name "g_pn_39"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_39.o"
endseg

beginseg
    name "g_pn_40"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_40.o"
endseg

beginseg
    name "g_pn_41"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_41.o"
endseg

beginseg
    name "g_pn_42"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_42.o"
endseg

beginseg
    name "g_pn_43"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_43.o"
endseg

beginseg
    name "g_pn_44"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_44.o"
endseg

beginseg
    name "g_pn_45"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_45.o"
endseg

beginseg
    name "g_pn_46"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_46.o"
endseg

beginseg
    name "g_pn_47"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_47.o"
endseg

beginseg
    name "g_pn_48"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_48.o"
endseg

beginseg
    name "g_pn_49"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_49.o"
endseg

beginseg
    name "g_pn_50"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_50.o"
endseg

beginseg
    name "g_pn_51"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_51.o"
endseg

beginseg
    name "g_pn_52"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_52.o"
endseg

beginseg
    name "g_pn_53"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_53.o"
endseg

beginseg
    name "g_pn_54"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_54.o"
endseg

beginseg
    name "g_pn_55"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_55.o"
endseg

beginseg
    name "g_pn_56"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_56.o"
endseg

beginseg
    name "g_pn_57"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/place_title_cards/g_pn_57.o"
endseg

beginseg
    name "z_select_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/misc/z_select_static/z_select_static.o"
    number 1
endseg

beginseg
    name "nintendo_rogo_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/nintendo_rogo_static/nintendo_rogo_static.o"
    number 1
endseg

beginseg
    name "title_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/title_static/title_static.o"
    number 1
endseg

beginseg
    name "parameter_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/parameter_static/parameter_static.o"
    number 2
endseg

beginseg
    name "vr_fine0_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_fine0_static.o"
endseg

beginseg
    name "vr_fine0_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_fine0_pal_static.o"
endseg

beginseg
    name "vr_fine1_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_fine1_static.o"
endseg

beginseg
    name "vr_fine1_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_fine1_pal_static.o"
endseg

beginseg
    name "vr_fine2_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_fine2_static.o"
endseg

beginseg
    name "vr_fine2_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_fine2_pal_static.o"
endseg

beginseg
    name "vr_fine3_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_fine3_static.o"
endseg

beginseg
    name "vr_fine3_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_fine3_pal_static.o"
endseg

beginseg
    name "vr_cloud0_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_cloud0_static.o"
endseg

beginseg
    name "vr_cloud0_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_cloud0_pal_static.o"
endseg

beginseg
    name "vr_cloud1_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_cloud1_static.o"
endseg

beginseg
    name "vr_cloud1_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_cloud1_pal_static.o"
endseg

beginseg
    name "vr_cloud2_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_cloud2_static.o"
endseg

beginseg
    name "vr_cloud2_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_cloud2_pal_static.o"
endseg

beginseg
    name "vr_cloud3_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_cloud3_static.o"
endseg

beginseg
    name "vr_cloud3_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_cloud3_pal_static.o"
endseg

beginseg
    name "vr_holy0_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_holy0_static.o"
endseg

beginseg
    name "vr_holy0_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_holy0_pal_static.o"
endseg

beginseg
    name "vr_holy1_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_holy1_static.o"
endseg

beginseg
    name "vr_holy1_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/skyboxes/vr_holy1_pal_static.o"
endseg

beginseg
    name "vr_MDVR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_MDVR_static.o"
endseg

beginseg
    name "vr_MDVR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_MDVR_pal_static.o"
endseg

beginseg
    name "vr_MNVR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_MNVR_static.o"
endseg

beginseg
    name "vr_MNVR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_MNVR_pal_static.o"
endseg

beginseg
    name "vr_RUVR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_RUVR_static.o"
endseg

beginseg
    name "vr_RUVR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_RUVR_pal_static.o"
endseg

beginseg
    name "vr_LHVR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_LHVR_static.o"
endseg

beginseg
    name "vr_LHVR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_LHVR_pal_static.o"
endseg

beginseg
    name "vr_KHVR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_KHVR_static.o"
endseg

beginseg
    name "vr_KHVR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_KHVR_pal_static.o"
endseg

beginseg
    name "vr_K3VR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_K3VR_static.o"
endseg

beginseg
    name "vr_K3VR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_K3VR_pal_static.o"
endseg

beginseg
    name "vr_K4VR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_K4VR_static.o"
endseg

beginseg
    name "vr_K4VR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_K4VR_pal_static.o"
endseg

beginseg
    name "vr_K5VR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_K5VR_static.o"
endseg

beginseg
    name "vr_K5VR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_K5VR_pal_static.o"
endseg

beginseg
    name "vr_SP1a_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_SP1a_static.o"
endseg

beginseg
    name "vr_SP1a_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_SP1a_pal_static.o"
endseg

beginseg
    name "vr_MLVR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_MLVR_static.o"
endseg

beginseg
    name "vr_MLVR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_MLVR_pal_static.o"
endseg

beginseg
    name "vr_KKRVR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_KKRVR_static.o"
endseg

beginseg
    name "vr_KKRVR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_KKRVR_pal_static.o"
endseg

beginseg
    name "vr_KR3VR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_KR3VR_static.o"
endseg

beginseg
    name "vr_KR3VR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_KR3VR_pal_static.o"
endseg

beginseg
    name "vr_IPVR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_IPVR_static.o"
endseg

beginseg
    name "vr_IPVR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_IPVR_pal_static.o"
endseg

beginseg
    name "vr_KSVR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_KSVR_static.o"
endseg

beginseg
    name "vr_KSVR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_KSVR_pal_static.o"
endseg

beginseg
    name "vr_GLVR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_GLVR_static.o"
endseg

beginseg
    name "vr_GLVR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_GLVR_pal_static.o"
endseg

beginseg
    name "vr_ZRVR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_ZRVR_static.o"
endseg

beginseg
    name "vr_ZRVR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_ZRVR_pal_static.o"
endseg

beginseg
    name "vr_DGVR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_DGVR_static.o"
endseg

beginseg
    name "vr_DGVR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_DGVR_pal_static.o"
endseg

beginseg
    name "vr_ALVR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_ALVR_static.o"
endseg

beginseg
    name "vr_ALVR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_ALVR_pal_static.o"
endseg

beginseg
    name "vr_NSVR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_NSVR_static.o"
endseg

beginseg
    name "vr_NSVR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_NSVR_pal_static.o"
endseg

beginseg
    name "vr_LBVR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_LBVR_static.o"
endseg

beginseg
    name "vr_LBVR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_LBVR_pal_static.o"
endseg

beginseg
    name "vr_TTVR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_TTVR_static.o"
endseg

beginseg
    name "vr_TTVR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_TTVR_pal_static.o"
endseg

beginseg
    name "vr_FCVR_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_FCVR_static.o"
endseg

beginseg
    name "vr_FCVR_pal_static"
    romalign 0x1000
    include "$(BUILD_DIR)/assets/textures/backgrounds/vr_FCVR_pal_static.o"
endseg

beginseg
    name "elf_message_field"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/src/elf_message/elf_message_field.o"
    number 0
endseg

beginseg
    name "elf_message_ydan"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/src/elf_message/elf_message_ydan.o"
    number 0
endseg

// Scene files are reordered between versions. On GameCube and iQue, dungeon scenes
// have been moved to the beginning.
#if PLATFORM_N64
#include "spec_includes/scenes_n64.inc"
#else
#include "spec_includes/scenes_gc_ique.inc"
#endif

beginseg
    name "bump_texture_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/baserom/bump_texture_static.o"
endseg

beginseg
    name "anime_model_1_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/baserom/anime_model_1_static.o"
endseg

beginseg
    name "anime_model_2_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/baserom/anime_model_2_static.o"
endseg

beginseg
    name "anime_model_3_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/baserom/anime_model_3_static.o"
endseg

beginseg
    name "anime_model_4_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/baserom/anime_model_4_static.o"
endseg

beginseg
    name "anime_model_5_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/baserom/anime_model_5_static.o"
endseg

beginseg
    name "anime_model_6_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/baserom/anime_model_6_static.o"
endseg

beginseg
    name "anime_texture_1_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/baserom/anime_texture_1_static.o"
endseg

beginseg
    name "anime_texture_2_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/baserom/anime_texture_2_static.o"
endseg

beginseg
    name "anime_texture_3_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/baserom/anime_texture_3_static.o"
endseg

beginseg
    name "anime_texture_4_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/baserom/anime_texture_4_static.o"
endseg

beginseg
    name "anime_texture_5_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/baserom/anime_texture_5_static.o"
endseg

beginseg
    name "anime_texture_6_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/baserom/anime_texture_6_static.o"
endseg

beginseg
    name "softsprite_matrix_static"
    compress
    romalign 0x1000
    include "$(BUILD_DIR)/baserom/softsprite_matrix_static.o"
endseg
