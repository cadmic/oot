#!/usr/bin/env python3
import csv

DUNGEON_SCENES = [
    "Bmori1",
    "FIRE_bs",
    "HAKAdan",
    "HAKAdanCH",
    "HAKAdan_bs",
    "HIDAN",
    "MIZUsin",
    "MIZUsin_bs",
    "bdan",
    "bdan_boss",
    "ddan",
    "ddan_boss",
    "ganon",
    "ganon_boss",
    "ganon_demo",
    "ganon_final",
    "ganon_sonogo",
    "ganontika",
    "ganontikasonogo",
    "gerudoway",
    "ice_doukutu",
    "jyasinboss",
    "jyasinzou",
    "men",
    "moribossroom",
    "ydan",
    "ydan_boss",
]

INDOOR_SCENES = [
    "bowling",
    "daiyousei_izumi",
    "hairal_niwa",
    "hairal_niwa_n",
    "hakasitarelay",
    "hut",
    "hylia_labo",
    "impa",
    "kakariko",
    "kenjyanoma",
    "kokiri_home",
    "kokiri_home3",
    "kokiri_home4",
    "kokiri_home5",
    "labo",
    "link_home",
    "mahouya",
    "malon_stable",
    "miharigoya",
    "nakaniwa",
    "souko",
    "syatekijyou",
    "takaraya",
    "tent",
    "tokinoma",
    "yousei_izumi_tate",
    "yousei_izumi_yoko",
]

MISC_SCENES = [
    "enrui",
    "entra",
    "entra_n",
    "hakaana",
    "hakaana2",
    "hakaana_ouke",
    "hiral_demo",
    "kakariko3",
    "kakusiana",
    "kinsuta",
    "market_alley",
    "market_alley_n",
    "market_day",
    "market_night",
    "market_ruins",
    "shrine",
    "shrine_n",
    "shrine_r",
    "turibori",
]

OVERWORLD_SCENES = [
    "ganon_tou",
    "spot00",
    "spot01",
    "spot02",
    "spot03",
    "spot04",
    "spot05",
    "spot06",
    "spot07",
    "spot08",
    "spot09",
    "spot10",
    "spot11",
    "spot12",
    "spot13",
    "spot15",
    "spot16",
    "spot17",
    "spot18",
    "spot20",
]

SHOP_SCENES = [
    "alley_shop",
    "drag",
    "face_shop",
    "golon",
    "kokiri_shop",
    "night_shop",
    "shop1",
    "zoora",
]


def get_z_name_for_overlay(filename: str) -> str:
    if filename == "ovl_player_actor":
        return "z_player"
    elif filename.startswith("ovl_Effect_"):
        return "z_eff_" + filename[len("ovl_Effect_") :].lower()
    else:
        return "z_" + filename[len("ovl_") :].lower()

def gen_overlay_spec():
    segments_csv = "baseroms/ntsc-1.2/segments.csv"
    with open(segments_csv, "r") as f:
        reader = csv.reader(f)
        first = True
        for row in reader:
            name = row[0]
            if not name.startswith("ovl_"):
                continue
            if name in ("ovl_title", "ovl_select", "ovl_opening", "ovl_file_choose", "ovl_kaleido_scope", "ovl_player_actor", "ovl_map_mark_data"):
                continue
            if not first:
                print()
            first = False

            category = "effects" if name.startswith("ovl_Effect_") else "actors"
            z_name = get_z_name_for_overlay(name)

            print("beginseg")
            print(f"    name \"{name}\"")
            print(f"    compress")
            if name == "ovl_Bg_Toki_Swd":
                print(f"include \"$(BUILD_DIR)/src/overlays/actors/ovl_Bg_Toki_Swd/z_bg_toki_swd_cutscene_data_1.o\"")
                print(f"include \"$(BUILD_DIR)/src/overlays/actors/ovl_Bg_Toki_Swd/z_bg_toki_swd_cutscene_data_2.o\"")
                print(f"include \"$(BUILD_DIR)/src/overlays/actors/ovl_Bg_Toki_Swd/z_bg_toki_swd_cutscene_data_3.o\"")
            elif name == "ovl_Bg_Treemouth":
                print(f"include \"$(BUILD_DIR)/src/overlays/actors/ovl_Bg_Treemouth/z_bg_treemouth_cutscene_data.o\"")
            elif name == "ovl_Demo_Kankyo":
                print(f"include \"$(BUILD_DIR)/src/overlays/actors/ovl_Demo_Kankyo/z_demo_kankyo_cutscene_data1.o\"")
                print(f"include \"$(BUILD_DIR)/src/overlays/actors/ovl_Demo_Kankyo/z_demo_kankyo_cutscene_data2.o\"")
                print(f"include \"$(BUILD_DIR)/src/overlays/actors/ovl_Demo_Kankyo/z_demo_kankyo_cutscene_data3.o\"")
                print(f"include \"$(BUILD_DIR)/src/overlays/actors/ovl_Demo_Kankyo/z_demo_kankyo_cutscene_data4.o\"")
                print(f"include \"$(BUILD_DIR)/src/overlays/actors/ovl_Demo_Kankyo/z_demo_kankyo_cutscene_data5.o\"")
                print(f"include \"$(BUILD_DIR)/src/overlays/actors/ovl_Demo_Kankyo/z_demo_kankyo_cutscene_data6.o\"")
                print(f"include \"$(BUILD_DIR)/src/overlays/actors/ovl_Demo_Kankyo/z_demo_kankyo_cutscene_data7.o\"")
                print(f"include \"$(BUILD_DIR)/src/overlays/actors/ovl_Demo_Kankyo/z_demo_kankyo_cutscene_data8.o\"")
            elif name == "ovl_En_Okarina_Tag":
                print(f"include \"$(BUILD_DIR)/src/overlays/actors/ovl_En_Okarina_Tag/z_en_okarina_tag_cutscene_data.o\"")
            elif name == "ovl_En_Zl1":
                print(f"include \"$(BUILD_DIR)/src/overlays/actors/ovl_En_Zl1/z_en_zl1_cutscene_data.o\"")
            print(f"    include \"$(BUILD_DIR)/src/overlays/{category}/{name}/{z_name}.o\"")
            print(f"    include \"$(BUILD_DIR)/src/overlays/{category}/{name}/{name}_reloc.o\"")
            print("endseg")

def gen_scene_spec():
    segments_csv = "baseroms/ntsc-1.2/segments.csv"
    with open(segments_csv, "r") as f:
        reader = csv.reader(f)
        first = True
        for row in reader:
            name = row[0]
            if not (name.endswith("_scene") or "_room_" in name):
                continue
            if not first:
                print()
            first = False

            if name.endswith("_scene"):
                stem = name[:-len("_scene")]
                number = 2
            else:
                stem = name.split("_room_")[0]
                number = 3

            if stem in DUNGEON_SCENES:
                category = "dungeons"
            elif stem in INDOOR_SCENES:
                category = "indoors"
            elif stem in MISC_SCENES:
                category = "misc"
            elif stem in OVERWORLD_SCENES:
                category = "overworld"
            elif stem in SHOP_SCENES:
                category = "shops"
            else:
                raise Exception(f"Unknown scene category for {name}")

            print("beginseg")
            print(f"    name \"{name}\"")
            print(f"    compress")
            print(f"    romalign 0x1000")
            print(f"    include \"$(BUILD_DIR)/assets/scenes/{category}/{stem}/{name}.o\"")
            print(f"    number {number}")
            print("endseg")

if __name__ == "__main__":
    # gen_overlay_spec()
    gen_scene_spec()
