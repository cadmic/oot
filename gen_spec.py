#!/usr/bin/env python3
import csv

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


if __name__ == "__main__":
    gen_overlay_spec()
