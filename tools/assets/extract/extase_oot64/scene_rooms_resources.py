import enum
import struct
import io

from ..extase import File, Resource, SegmentedAddressResolution
from ..extase.cdata_resources import (
    CDataArrayResource,
    CDataArrayNamedLengthResource,
    CDataExt_Struct,
    CDataExt_Array,
    CDataExt_Value,
    cdata_ext_Vec3s,
    INDENT,
    Vec3sArrayResource,
)

from .. import oot64_data

from . import collision_resources
from . import room_shape_resources
from . import misc_resources


def _SHIFTR(v: int, s: int, w: int):
    assert isinstance(v, int)
    assert isinstance(s, int)
    assert isinstance(w, int)
    assert v >= 0
    assert s >= 0
    assert w >= 1
    return (v >> s) & ((1 << w) - 1)


VERBOSE_NOT_FULLY_PARSED_SCENECMD = False


class SceneCmdId(enum.Enum):
    # keep the SCENE_CMD_ID_ prefix for grepability
    SCENE_CMD_ID_SPAWN_LIST = 0
    SCENE_CMD_ID_ACTOR_LIST = enum.auto()
    SCENE_CMD_ID_UNUSED_2 = enum.auto()
    SCENE_CMD_ID_COLLISION_HEADER = enum.auto()
    SCENE_CMD_ID_ROOM_LIST = enum.auto()
    SCENE_CMD_ID_WIND_SETTINGS = enum.auto()
    SCENE_CMD_ID_ENTRANCE_LIST = enum.auto()
    SCENE_CMD_ID_SPECIAL_FILES = enum.auto()
    SCENE_CMD_ID_ROOM_BEHAVIOR = enum.auto()
    SCENE_CMD_ID_UNDEFINED_9 = enum.auto()
    SCENE_CMD_ID_ROOM_SHAPE = enum.auto()
    SCENE_CMD_ID_OBJECT_LIST = enum.auto()
    SCENE_CMD_ID_LIGHT_LIST = enum.auto()
    SCENE_CMD_ID_PATH_LIST = enum.auto()
    SCENE_CMD_ID_TRANSITION_ACTOR_LIST = enum.auto()
    SCENE_CMD_ID_LIGHT_SETTINGS_LIST = enum.auto()
    SCENE_CMD_ID_TIME_SETTINGS = enum.auto()
    SCENE_CMD_ID_SKYBOX_SETTINGS = enum.auto()
    SCENE_CMD_ID_SKYBOX_DISABLES = enum.auto()
    SCENE_CMD_ID_EXIT_LIST = enum.auto()
    SCENE_CMD_ID_END = enum.auto()
    SCENE_CMD_ID_SOUND_SETTINGS = enum.auto()
    SCENE_CMD_ID_ECHO_SETTINGS = enum.auto()
    SCENE_CMD_ID_CUTSCENE_DATA = enum.auto()
    SCENE_CMD_ID_ALTERNATE_HEADER_LIST = enum.auto()
    SCENE_CMD_ID_MISC_SETTINGS = enum.auto()


class Data1Handler:
    ...


class Data1Handlers:
    RAW = Data1Handler()


scene_cmd_macro_name_by_cmd_id = {
    SceneCmdId.SCENE_CMD_ID_SPAWN_LIST: "SCENE_CMD_SPAWN_LIST",
    SceneCmdId.SCENE_CMD_ID_ACTOR_LIST: "SCENE_CMD_ACTOR_LIST",
    SceneCmdId.SCENE_CMD_ID_UNUSED_2: "SCENE_CMD_UNUSED_02",
    SceneCmdId.SCENE_CMD_ID_COLLISION_HEADER: "SCENE_CMD_COL_HEADER",
    SceneCmdId.SCENE_CMD_ID_ROOM_LIST: "SCENE_CMD_ROOM_LIST",
    SceneCmdId.SCENE_CMD_ID_WIND_SETTINGS: "SCENE_CMD_WIND_SETTINGS",
    SceneCmdId.SCENE_CMD_ID_ENTRANCE_LIST: "SCENE_CMD_ENTRANCE_LIST",
    SceneCmdId.SCENE_CMD_ID_SPECIAL_FILES: "SCENE_CMD_SPECIAL_FILES",
    SceneCmdId.SCENE_CMD_ID_ROOM_BEHAVIOR: "SCENE_CMD_ROOM_BEHAVIOR",
    SceneCmdId.SCENE_CMD_ID_UNDEFINED_9: "SCENE_CMD_UNK_09",
    SceneCmdId.SCENE_CMD_ID_ROOM_SHAPE: "SCENE_CMD_ROOM_SHAPE",
    SceneCmdId.SCENE_CMD_ID_OBJECT_LIST: "SCENE_CMD_OBJECT_LIST",
    SceneCmdId.SCENE_CMD_ID_LIGHT_LIST: "SCENE_CMD_LIGHT_LIST",
    SceneCmdId.SCENE_CMD_ID_PATH_LIST: "SCENE_CMD_PATH_LIST",
    SceneCmdId.SCENE_CMD_ID_TRANSITION_ACTOR_LIST: "SCENE_CMD_TRANSITION_ACTOR_LIST",
    SceneCmdId.SCENE_CMD_ID_LIGHT_SETTINGS_LIST: "SCENE_CMD_ENV_LIGHT_SETTINGS",
    SceneCmdId.SCENE_CMD_ID_TIME_SETTINGS: "SCENE_CMD_TIME_SETTINGS",
    SceneCmdId.SCENE_CMD_ID_SKYBOX_SETTINGS: "SCENE_CMD_SKYBOX_SETTINGS",
    SceneCmdId.SCENE_CMD_ID_SKYBOX_DISABLES: "SCENE_CMD_SKYBOX_DISABLES",
    SceneCmdId.SCENE_CMD_ID_EXIT_LIST: "SCENE_CMD_EXIT_LIST",
    SceneCmdId.SCENE_CMD_ID_END: "SCENE_CMD_END",
    SceneCmdId.SCENE_CMD_ID_SOUND_SETTINGS: "SCENE_CMD_SOUND_SETTINGS",
    SceneCmdId.SCENE_CMD_ID_ECHO_SETTINGS: "SCENE_CMD_ECHO_SETTINGS",
    SceneCmdId.SCENE_CMD_ID_CUTSCENE_DATA: "SCENE_CMD_CUTSCENE_DATA",
    SceneCmdId.SCENE_CMD_ID_ALTERNATE_HEADER_LIST: "SCENE_CMD_ALTERNATE_HEADER_LIST",
    SceneCmdId.SCENE_CMD_ID_MISC_SETTINGS: "SCENE_CMD_MISC_SETTINGS",
}


class SceneCommandsResource(Resource, can_size_be_unknown=True):
    def __init__(self, file: File, range_start: int, name: str):
        super().__init__(file, range_start, None, name)
        self.parsed_commands: set[SceneCmdId] = set()
        self.player_entry_list_length = None
        self.room_list_length = None
        self.exit_list_length = None

    def try_parse_data(self):
        data = self.file.data[self.range_start :]

        offset = 0
        cmd_id = None
        end_offset = None

        found_commands: set[SceneCmdId] = set()

        while offset + 8 <= len(data):
            (cmd_id_int, data1, pad2, data2_I) = struct.unpack_from(
                ">BBHI", data, offset
            )
            (_, data2_H0, data2_H1) = struct.unpack_from(">IHH", data, offset)
            (_, data2_B0, data2_B1, data2_B2, data2_B3) = struct.unpack_from(
                ">IBBBB", data, offset
            )

            offset += 8
            cmd_id = SceneCmdId(cmd_id_int)
            assert pad2 == 0

            found_commands.add(cmd_id)

            if cmd_id == SceneCmdId.SCENE_CMD_ID_END:
                assert data1 == 0
                assert data2_I == 0
                end_offset = offset
                self.parsed_commands.add(cmd_id)
                break

            if cmd_id in self.parsed_commands:
                continue

            if cmd_id == SceneCmdId.SCENE_CMD_ID_ACTOR_LIST:
                resource, _ = self.file.memory_context.report_resource_at_segmented(
                    data2_I,
                    lambda file, offset: ActorEntryListResource(
                        file, offset, f"{self.name}_{data2_I:08X}_ActorEntryList"
                    ),
                )
                assert isinstance(resource, ActorEntryListResource)
                resource.set_length(data1)
                self.parsed_commands.add(cmd_id)

            if cmd_id == SceneCmdId.SCENE_CMD_ID_OBJECT_LIST:
                resource, _ = self.file.memory_context.report_resource_at_segmented(
                    data2_I,
                    lambda file, offset: ObjectListResource(
                        file, offset, f"{self.name}_{data2_I:08X}_ObjectList"
                    ),
                )
                assert isinstance(resource, ObjectListResource)
                resource.set_length(data1)
                self.parsed_commands.add(cmd_id)

            if cmd_id == SceneCmdId.SCENE_CMD_ID_ROOM_SHAPE:
                room_shape_resources.report_room_shape_at_segmented(
                    self.file.memory_context, data2_I, self.name
                )
                self.parsed_commands.add(cmd_id)

            if cmd_id == SceneCmdId.SCENE_CMD_ID_ROOM_LIST:
                self.room_list_length = data1
                resource, _ = self.file.memory_context.report_resource_at_segmented(
                    data2_I,
                    lambda file, offset: RoomListResource(
                        file, offset, f"{self.name}_{data2_I:08X}_RoomList"
                    ),
                )
                assert isinstance(resource, RoomListResource)
                resource.set_length(data1)
                self.parsed_commands.add(cmd_id)

            if cmd_id == SceneCmdId.SCENE_CMD_ID_COLLISION_HEADER:
                assert data1 == 0
                resource, _ = self.file.memory_context.report_resource_at_segmented(
                    data2_I,
                    lambda file, offset: collision_resources.CollisionResource(
                        file, offset, f"{self.name}_{data2_I:08X}_Col"
                    ),
                )
                assert isinstance(resource, collision_resources.CollisionResource)
                if resource.is_data_parsed:
                    self.exit_list_length = resource.length_exitList
                    self.parsed_commands.add(cmd_id)

            if cmd_id == SceneCmdId.SCENE_CMD_ID_ENTRANCE_LIST:
                assert data1 == 0
                resource, _ = self.file.memory_context.report_resource_at_segmented(
                    data2_I,
                    lambda file, offset: SpawnListResource(
                        file, offset, f"{self.name}_{data2_I:08X}_SpawnList"
                    ),
                )
                assert isinstance(resource, SpawnListResource)
                if (
                    self.player_entry_list_length is not None
                    and self.room_list_length is not None
                ):
                    resource.player_entry_list_length = self.player_entry_list_length
                    resource.room_list_length = self.room_list_length
                    self.parsed_commands.add(cmd_id)

            if cmd_id == SceneCmdId.SCENE_CMD_ID_SPAWN_LIST:
                self.player_entry_list_length = data1
                resource, _ = self.file.memory_context.report_resource_at_segmented(
                    data2_I,
                    lambda file, offset: ActorEntryListResource(
                        file, offset, f"{self.name}_{data2_I:08X}_PlayerEntryList"
                    ),
                )
                assert isinstance(resource, ActorEntryListResource)
                resource.set_length(data1)
                self.parsed_commands.add(cmd_id)

            if cmd_id == SceneCmdId.SCENE_CMD_ID_EXIT_LIST:
                # TODO length from collision
                assert data1 == 0
                resource, _ = self.file.memory_context.report_resource_at_segmented(
                    data2_I,
                    lambda file, offset: ExitListResource(
                        file, offset, f"{self.name}_{data2_I:08X}_ExitList"
                    ),
                )
                assert isinstance(resource, ExitListResource)
                if self.exit_list_length is not None:
                    # TODO this doesnt work very well, eg need to trim to avoid overlaps
                    length = self.exit_list_length
                    # blindly align length to 2 (could/should check for zeros)
                    length = max(2, (length + 1) // 2 * 2)
                    # trim based on overlaps
                    while True:
                        _, other_resource = resource.file.get_resource_at(
                            resource.range_start
                            + length * resource.elem_cdata_ext.size
                            - 1
                        )
                        if other_resource is resource:
                            break
                        length -= 2
                    assert length > 0
                    resource.set_length(length)
                    self.parsed_commands.add(cmd_id)

            if cmd_id == SceneCmdId.SCENE_CMD_ID_LIGHT_SETTINGS_LIST:
                resource, _ = self.file.memory_context.report_resource_at_segmented(
                    data2_I,
                    lambda file, offset: EnvLightSettingsListResource(
                        file, offset, f"{self.name}_{data2_I:08X}_EnvLightSettingsList"
                    ),
                )
                assert isinstance(resource, EnvLightSettingsListResource)
                resource.set_length(data1)
                self.parsed_commands.add(cmd_id)

            if cmd_id == SceneCmdId.SCENE_CMD_ID_TRANSITION_ACTOR_LIST:
                resource, _ = self.file.memory_context.report_resource_at_segmented(
                    data2_I,
                    lambda file, offset: TransitionActorEntryListResource(
                        file,
                        offset,
                        f"{self.name}_{data2_I:08X}_TransitionActorEntryList",
                    ),
                )
                assert isinstance(resource, TransitionActorEntryListResource)
                resource.set_length(data1)
                self.parsed_commands.add(cmd_id)

            if cmd_id == SceneCmdId.SCENE_CMD_ID_PATH_LIST:
                # TODO guess length, no other way I think
                assert data1 == 0
                self.file.memory_context.report_resource_at_segmented(
                    data2_I,
                    lambda file, offset: PathListResource(
                        file, offset, f"{self.name}_{data2_I:08X}_PathList"
                    ),
                )
                self.parsed_commands.add(cmd_id)

            if cmd_id == SceneCmdId.SCENE_CMD_ID_ALTERNATE_HEADER_LIST:
                # TODO guess length, no other way I think
                assert data1 == 0
                self.file.memory_context.report_resource_at_segmented(
                    data2_I,
                    lambda file, offset: AltHeadersResource(
                        file, offset, f"{self.name}_{data2_I:08X}_AltHeaders"
                    ),
                )
                self.parsed_commands.add(cmd_id)

            if cmd_id == SceneCmdId.SCENE_CMD_ID_CUTSCENE_DATA:
                assert data1 == 0
                self.file.memory_context.report_resource_at_segmented(
                    data2_I,
                    lambda file, offset: misc_resources.CutsceneResource(
                        file, offset, f"{self.name}_{data2_I:08X}_Cs"
                    ),
                )
                self.parsed_commands.add(cmd_id)

        if cmd_id != SceneCmdId.SCENE_CMD_ID_END:
            raise Exception("reached end of data without encountering end marker")
        assert end_offset is not None

        # TODO hack until I have a clearer view of stuff once all cmds are loosely implemented
        found_commands.discard(SceneCmdId.SCENE_CMD_ID_SOUND_SETTINGS)
        found_commands.discard(SceneCmdId.SCENE_CMD_ID_MISC_SETTINGS)
        found_commands.discard(SceneCmdId.SCENE_CMD_ID_SPECIAL_FILES)
        found_commands.discard(SceneCmdId.SCENE_CMD_ID_SKYBOX_SETTINGS)
        found_commands.discard(SceneCmdId.SCENE_CMD_ID_TIME_SETTINGS)
        found_commands.discard(SceneCmdId.SCENE_CMD_ID_ROOM_BEHAVIOR)
        found_commands.discard(SceneCmdId.SCENE_CMD_ID_ECHO_SETTINGS)
        found_commands.discard(SceneCmdId.SCENE_CMD_ID_SKYBOX_DISABLES)
        found_commands.discard(SceneCmdId.SCENE_CMD_ID_UNDEFINED_9)
        found_commands.discard(SceneCmdId.SCENE_CMD_ID_WIND_SETTINGS)

        self.range_end = self.range_start + end_offset
        assert self.parsed_commands.issubset(found_commands)
        self.is_data_parsed = self.parsed_commands == found_commands
        if found_commands - self.parsed_commands:
            if VERBOSE_NOT_FULLY_PARSED_SCENECMD:
                print(
                    "NOT FULLY PARSED:",
                    self,
                    "Found commands:",
                    found_commands,
                    "Parsed commands:",
                    self.parsed_commands,
                    "FOUND BUT NOT PARSED:",
                    found_commands - self.parsed_commands,
                )

    def get_c_declaration_base(self):
        return f"SceneCmd {self.symbol_name}[]"

    def write_extracted(self):
        data = self.file.data[self.range_start : self.range_end]
        with self.extract_to_path.open("w") as f:
            f.write("{\n")
            for offset in range(0, len(data), 8):
                (cmd_id_int, data1, pad2, data2_I) = struct.unpack_from(
                    ">BBHI", data, offset
                )
                (_, data2_H0, data2_H1) = struct.unpack_from(">IHH", data, offset)
                (_, data2_B0, data2_B1, data2_B2, data2_B3) = struct.unpack_from(
                    ">IBBBB", data, offset
                )
                cmd_id = SceneCmdId(cmd_id_int)
                f.write(" " * 4)
                f.write(scene_cmd_macro_name_by_cmd_id[cmd_id])
                f.write("(")
                if cmd_id == SceneCmdId.SCENE_CMD_ID_SPAWN_LIST:
                    address = data2_I
                    f.write(
                        self.file.memory_context.get_c_expression_length_at_segmented(
                            address
                        )
                    )
                    f.write(", ")
                    f.write(
                        self.file.memory_context.get_c_reference_at_segmented(address)
                    )
                if cmd_id == SceneCmdId.SCENE_CMD_ID_ACTOR_LIST:
                    address = data2_I
                    f.write(
                        self.file.memory_context.get_c_expression_length_at_segmented(
                            address
                        )
                    )
                    f.write(", ")
                    f.write(
                        self.file.memory_context.get_c_reference_at_segmented(address)
                    )
                if cmd_id == SceneCmdId.SCENE_CMD_ID_UNUSED_2:
                    raise NotImplementedError(cmd_id)
                if cmd_id == SceneCmdId.SCENE_CMD_ID_COLLISION_HEADER:
                    assert data1 == 0
                    address = data2_I
                    f.write(
                        self.file.memory_context.get_c_reference_at_segmented(address)
                    )
                if cmd_id == SceneCmdId.SCENE_CMD_ID_ROOM_LIST:
                    address = data2_I
                    f.write(
                        self.file.memory_context.get_c_expression_length_at_segmented(
                            address
                        )
                    )
                    f.write(", ")
                    f.write(
                        self.file.memory_context.get_c_reference_at_segmented(address)
                    )
                if cmd_id == SceneCmdId.SCENE_CMD_ID_WIND_SETTINGS:
                    assert data1 == 0
                    # TODO cast x,y,z to s8
                    xDir = data2_B0
                    yDir = data2_B1
                    zDir = data2_B2
                    strength = data2_B3
                    f.write(f"{xDir}, {yDir}, {zDir}, {strength}")
                if cmd_id == SceneCmdId.SCENE_CMD_ID_ENTRANCE_LIST:
                    assert data1 == 0
                    address = data2_I
                    f.write(
                        self.file.memory_context.get_c_reference_at_segmented(address)
                    )
                if cmd_id == SceneCmdId.SCENE_CMD_ID_SPECIAL_FILES:
                    naviQuestHintFileId = data1
                    keepObjectId = data2_I
                    f.write(f"{naviQuestHintFileId}, {keepObjectId}")
                if cmd_id == SceneCmdId.SCENE_CMD_ID_ROOM_BEHAVIOR:
                    gpFlags1 = data1
                    gpFlags2 = data2_I
                    behaviorType1 = gpFlags1
                    behaviorType2 = _SHIFTR(gpFlags2, 0, 8)
                    lensMode = _SHIFTR(gpFlags2, 8, 1)
                    disableWarpSongs = _SHIFTR(gpFlags2, 10, 1)
                    behaviorType1_name = oot64_data.get_room_behavior_type1_name(
                        behaviorType1
                    )
                    behaviorType2_name = oot64_data.get_room_behavior_type2_name(
                        behaviorType2
                    )
                    lensMode_name = oot64_data.get_lens_mode_name(lensMode)
                    disableWarpSongs_name = (
                        "true /* no warp songs */"
                        if disableWarpSongs
                        else "false /* warp songs enabled */"
                    )
                    f.write(
                        f"{behaviorType1_name}, {behaviorType2_name}, {lensMode_name}, {disableWarpSongs_name}"
                    )
                if cmd_id == SceneCmdId.SCENE_CMD_ID_UNDEFINED_9:
                    assert data1 == 0
                    assert data2_I == 0
                if cmd_id == SceneCmdId.SCENE_CMD_ID_ROOM_SHAPE:
                    assert data1 == 0  # TODO these asserts should be done on parse?
                    address = data2_I
                    f.write(
                        self.file.memory_context.get_c_reference_at_segmented(address)
                    )
                if cmd_id == SceneCmdId.SCENE_CMD_ID_OBJECT_LIST:
                    address = data2_I
                    f.write(
                        self.file.memory_context.get_c_expression_length_at_segmented(
                            address
                        )
                    )
                    f.write(", ")
                    f.write(
                        self.file.memory_context.get_c_reference_at_segmented(address)
                    )
                if cmd_id == SceneCmdId.SCENE_CMD_ID_LIGHT_LIST:
                    raise NotImplementedError(cmd_id)
                if cmd_id == SceneCmdId.SCENE_CMD_ID_PATH_LIST:
                    assert data1 == 0
                    address = data2_I
                    f.write(
                        self.file.memory_context.get_c_reference_at_segmented(address)
                    )
                if cmd_id == SceneCmdId.SCENE_CMD_ID_TRANSITION_ACTOR_LIST:
                    address = data2_I
                    f.write(
                        self.file.memory_context.get_c_expression_length_at_segmented(
                            address
                        )
                    )
                    f.write(", ")
                    f.write(
                        self.file.memory_context.get_c_reference_at_segmented(address)
                    )
                if cmd_id == SceneCmdId.SCENE_CMD_ID_LIGHT_SETTINGS_LIST:
                    address = data2_I
                    f.write(
                        self.file.memory_context.get_c_expression_length_at_segmented(
                            address
                        )
                    )
                    f.write(", ")
                    f.write(
                        self.file.memory_context.get_c_reference_at_segmented(address)
                    )
                if cmd_id == SceneCmdId.SCENE_CMD_ID_TIME_SETTINGS:
                    assert data1 == 0
                    hour = data2_B0
                    min_ = data2_B1
                    timeSpeed = data2_B2
                    assert data2_B3 == 0

                    hour_str = "0xFF" if hour == 0xFF else str(hour)
                    min_str = "0xFF" if min_ == 0xFF else str(min_)
                    timeSpeed_str = "0xFF" if timeSpeed == 0xFF else str(timeSpeed)

                    if hour == 0xFF or min_ == 0xFF:
                        f.write("/* don't set time */ ")
                    f.write(f"{hour_str}, {min_str}, {timeSpeed_str}")
                    if timeSpeed == 0xFF or timeSpeed == 0:
                        f.write(" /* time doesn't move */")
                if cmd_id == SceneCmdId.SCENE_CMD_ID_SKYBOX_SETTINGS:
                    assert data1 == 0
                    skyboxId = data2_B0
                    skyboxConfig = data2_B1
                    envLightMode = data2_B2
                    assert data2_B3 == 0
                    f.write(f"{skyboxId}, {skyboxConfig}, {envLightMode}")
                if cmd_id == SceneCmdId.SCENE_CMD_ID_SKYBOX_DISABLES:
                    assert data1 == 0
                    skyboxDisabled = data2_B0
                    sunMoonDisabled = data2_B1
                    assert data2_B2 == data2_B3 == 0
                    skyboxDisabled_name = (
                        "true /* no skybox */"
                        if skyboxDisabled
                        else "false /* skybox enabled */"
                    )
                    sunMoonDisabled_name = (
                        "true /* no sun/moon */"
                        if sunMoonDisabled
                        else "false /* sun/moon enabled */"
                    )
                    f.write(f"{skyboxDisabled_name}, {sunMoonDisabled_name}")
                if cmd_id == SceneCmdId.SCENE_CMD_ID_EXIT_LIST:
                    assert data1 == 0
                    address = data2_I
                    f.write(
                        self.file.memory_context.get_c_reference_at_segmented(address)
                    )
                if cmd_id == SceneCmdId.SCENE_CMD_ID_END:
                    assert data1 == 0
                    assert data2_I == 0
                if cmd_id == SceneCmdId.SCENE_CMD_ID_SOUND_SETTINGS:
                    specId = data1
                    assert data2_B0 == 0
                    assert data2_B1 == 0
                    natureAmbienceId = data2_B2
                    seqId = data2_B3
                    natureAmbienceId_name = oot64_data.get_nature_ambience_id_name(
                        natureAmbienceId
                    )
                    seqId_name = oot64_data.get_sequence_id_name(seqId)
                    f.write(f"{specId}, {natureAmbienceId_name}, {seqId_name}")
                if cmd_id == SceneCmdId.SCENE_CMD_ID_ECHO_SETTINGS:
                    assert data1 == 0
                    assert data2_B0 == data2_B1 == data2_B2 == 0
                    echo = data2_B3
                    f.write(f"{echo}")
                if cmd_id == SceneCmdId.SCENE_CMD_ID_CUTSCENE_DATA:
                    assert data1 == 0
                    address = data2_I
                    f.write(
                        self.file.memory_context.get_c_reference_at_segmented(address)
                    )
                if cmd_id == SceneCmdId.SCENE_CMD_ID_ALTERNATE_HEADER_LIST:
                    # TODO
                    assert data1 == 0
                    address = data2_I
                    f.write(f"0x{address:08X}")
                if cmd_id == SceneCmdId.SCENE_CMD_ID_MISC_SETTINGS:
                    sceneCamType = data1
                    worldMapLocation = data2_I
                    sceneCamType_name = oot64_data.get_scene_cam_type_name(sceneCamType)
                    f.write(f"{sceneCamType_name}, {worldMapLocation}")

                f.write("),\n")
            f.write("}\n")

    def get_c_reference(self, resource_offset: int):
        if resource_offset == 0:
            return self.symbol_name
        else:
            raise ValueError


# TODO move resources other than scenecmd to their own file "scene_resources"


def fmt_hex_s(v: int, nibbles: int = 0):
    """Format v to 0x-prefixed uppercase hexadecimal, using (at least) the specified amount of nibbles.

    Meant for signed values (_s suffix),
    adds a space in place of where the - sign would be for positive values.

    Note compared to this,
    - f"{v:#X}" would produce an uppercase 0X (1 -> 0X1)
    - f"0x{v:X}" doesn't work with negative values (-1 -> 0x-1)
    """
    v_str = f"{v:0{nibbles}X}"
    if v < 0:
        v_str = v_str.removeprefix("-")
        return f"-0x{v_str}"
    else:
        return f" 0x{v_str}"


def fmt_hex_u(v: int, nibbles: int = 0):
    """Format v to 0x-prefixed uppercase hexadecimal, using (at least) the specified amount of nibbles.

    Meant for unsigned values (_u suffix),
    but won't fail for negative values.

    See: fmt_hex_s
    """
    v_str = f"{v:0{nibbles}X}"
    if v < 0:
        # Also handle v being negative just in case,
        # it will only mean the output isn't aligned as expected
        v_str = v_str.removeprefix("-")
        return f"-0x{v_str}"
    else:
        return f"0x{v_str}"


class ActorEntryListResource(CDataArrayNamedLengthResource):
    def write_elem(resource, v, f: io.TextIOBase, line_prefix: str):
        assert isinstance(v, dict)
        f.write(line_prefix)
        f.write("{\n")

        f.write(line_prefix + INDENT)
        f.write(oot64_data.get_actor_id_name(v["id"]))
        f.write(",\n")

        f.write(line_prefix + INDENT)
        f.write("{ ")
        f.write(", ".join(f"{p:6}" for p in (v["pos"][axis] for axis in "xyz")))
        f.write(" }, // pos\n")

        f.write(line_prefix + INDENT)
        f.write("{ ")
        f.write(", ".join(fmt_hex_s(r, 4) for r in (v["rot"][axis] for axis in "xyz")))
        f.write(" }, // rot\n")

        f.write(line_prefix + INDENT)
        params = v["params"]
        f.write(fmt_hex_s(params, 4))
        if params < 0:
            params_u16 = params + 0x1_0000
            f.write(f" /* 0x{params_u16:04X} */")
        f.write(", // params\n")

        f.write(line_prefix)
        f.write("}")

        return True

    elem_cdata_ext = CDataExt_Struct(
        (
            ("id", CDataExt_Value.s16),
            ("pos", cdata_ext_Vec3s),
            ("rot", cdata_ext_Vec3s),
            ("params", CDataExt_Value.s16),
        )
    ).set_write(write_elem)

    def get_c_declaration_base(self):
        return f"ActorEntry {self.symbol_name}[{self.length_name}]"


class ObjectListResource(CDataArrayNamedLengthResource):
    elem_cdata_ext = CDataExt_Value("h").set_write_str_v(
        lambda v: oot64_data.get_object_id_name(v)
    )

    def get_c_declaration_base(self):
        return f"s16 {self.symbol_name}[{self.length_name}]"


def write_RomFile(resource, v, f: io.TextIOBase, line_prefix: str):
    assert isinstance(v, dict)
    vromStart = v["vromStart"]
    vromEnd = v["vromEnd"]
    rom_file_name = oot64_data.get_dmadata_table_rom_file_name_from_vrom(
        vromStart, vromEnd
    )
    f.write(line_prefix)
    f.write(f"ROM_FILE({rom_file_name})")
    return True


cdata_ext_RomFile = CDataExt_Struct(
    (
        ("vromStart", CDataExt_Value.u32),
        ("vromEnd", CDataExt_Value.u32),
    )
).set_write(write_RomFile)


class RoomListResource(CDataArrayNamedLengthResource):
    elem_cdata_ext = cdata_ext_RomFile

    def get_c_declaration_base(self):
        return f"RomFile {self.symbol_name}[{self.length_name}]"


class SpawnListResource(CDataArrayResource):
    elem_cdata_ext = CDataExt_Struct(
        (
            ("playerEntryIndex", CDataExt_Value.u8),
            ("room", CDataExt_Value.u8),
        )
    )

    # (eventually) set by SceneCommandsResource
    player_entry_list_length = None
    room_list_length = None

    def try_parse_data(self):
        if self.player_entry_list_length is None or self.room_list_length is None:
            return

        # File.name comes from the Name attribute on a <File> element,
        # which is also used to make the path to the baserom file to read from.
        # So File.name is the name of the baserom file.
        # This may change in the future though ¯\_(ツ)_/¯
        rom_file_name = self.file.name
        # This way we can get the scene ID of the file
        scene_id = oot64_data.get_scene_id_from_rom_file_name(rom_file_name)
        scene_id_name = oot64_data.get_scene_id_name(scene_id)
        # Get all the spawns used by all entrances using the scene
        entrance_ids = oot64_data.get_entrance_ids_from_scene_id_name(scene_id_name)
        all_used_spawns = set()
        for entrance_id in entrance_ids:
            entrance_spawn = oot64_data.get_entrance_spawn(entrance_id)
            all_used_spawns.add(entrance_spawn)
        num_spawns = max(all_used_spawns) + 1

        # Handle the cases where the entrance table references spawn outside the spawn list,
        # by checking if the indices in the last spawn in the list make sense.
        # This is required for a few scenes in practice, otherwise the spawn list and exit list overlap.
        while True:
            last_spawn_unpacked = self.elem_cdata_ext.unpack_from(
                self.file.data,
                self.range_start + (num_spawns - 1) * self.elem_cdata_ext.size,
            )
            if (
                last_spawn_unpacked["playerEntryIndex"] < self.player_entry_list_length
                and last_spawn_unpacked["room"] < self.room_list_length
            ):
                break
            print(
                self,
                "Removing one spawn because the last spawn of the list has bad indices",
                last_spawn_unpacked,
                num_spawns,
                "->",
                num_spawns - 1,
            )
            num_spawns -= 1
            assert num_spawns > 0

        # Handle the case where there may be an unused spawn, in the place of
        # what would otherwise be padding.
        if self.file.memory_context.I_D_OMEGALUL:
            assert self.elem_cdata_ext.size == 2
            if num_spawns % 2 == 1:
                data_to_next_4align = self.file.data[
                    self.range_start + num_spawns * 2 :
                ][:2]
                if data_to_next_4align != b"\x00\x00":
                    print(
                        self,
                        "Adding one spawn because the next supposedly-padding"
                        " two bytes are not padding (not zero)",
                        bytes(data_to_next_4align),
                        num_spawns,
                        "->",
                        num_spawns + 1,
                    )
                    num_spawns += 1

        # Trim the list to avoid overlaps
        # TODO this may be linked to headers for cutscene layers not having the spawns the entrance table expects
        # for example spot00 hyrule field seems to always have a single 0,0 spawn for cutscene layers?
        # (so the above approach using the entrance table does not generalize to cutscene layers)
        # so it may be relevant to have the layer type when parsing the spawn list
        # Alternatively, somehow trim the variable-length resources when overlapping
        while True:
            range_end = self.range_start + num_spawns * self.elem_cdata_ext.size
            result, resource = self.file.get_resource_at(range_end - 1)
            if resource is self:
                break
            print(
                self,
                "Removing one spawn because the last spawn of the list overlaps with another resource",
                resource,
                num_spawns,
                "->",
                num_spawns - 1,
            )
            num_spawns -= 1
            assert num_spawns > 0

        self.set_length(num_spawns)
        super().try_parse_data()

    def get_c_declaration_base(self):
        return f"Spawn {self.symbol_name}[]"


class ExitListResource(CDataArrayResource):
    elem_cdata_ext = CDataExt_Value("h").set_write_str_v(
        lambda v: oot64_data.get_entrance_id_name(v)
    )

    # length set by SceneCommandsResource.try_parse_data

    def get_c_declaration_base(self):
        return f"s16 {self.symbol_name}[]"


class EnvLightSettingsListResource(CDataArrayNamedLengthResource):
    # TODO formatting
    elem_cdata_ext = CDataExt_Struct(
        (
            ("ambientColor", CDataExt_Array(CDataExt_Value.u8, 3)),
            ("light1Dir", CDataExt_Array(CDataExt_Value.s8, 3)),
            ("light1Color", CDataExt_Array(CDataExt_Value.u8, 3)),
            ("light2Dir", CDataExt_Array(CDataExt_Value.s8, 3)),
            ("light2Color", CDataExt_Array(CDataExt_Value.u8, 3)),
            ("fogColor", CDataExt_Array(CDataExt_Value.u8, 3)),
            ("blendRateAndFogNear", CDataExt_Value.s16),
            ("zFar", CDataExt_Value.s16),
        )
    )

    def get_c_declaration_base(self):
        return f"EnvLightSettings {self.symbol_name}[{self.length_name}]"


class TransitionActorEntryListResource(CDataArrayNamedLengthResource):
    def write_elem(resource, v, f: io.TextIOBase, line_prefix: str):
        assert isinstance(v, dict)
        f.write(line_prefix)
        f.write("{\n")

        f.write(line_prefix + INDENT)
        f.write("{\n")
        f.write(line_prefix + 2 * INDENT)
        f.write("// { room, bgCamIndex }\n")
        for side_i in range(2):
            side = v["sides"][side_i]
            room = side["room"]
            bgCamIndex = side["bgCamIndex"]
            f.write(line_prefix + 2 * INDENT)
            f.write("{ ")
            f.write(f"{room}, {bgCamIndex}")
            f.write(" },\n")
        f.write(line_prefix + INDENT)
        f.write("}, // sides\n")

        f.write(line_prefix + INDENT)
        f.write(oot64_data.get_actor_id_name(v["id"]))
        f.write(",\n")

        f.write(line_prefix + INDENT)
        f.write("{ ")
        f.write(", ".join(f"{p:6}" for p in (v["pos"][axis] for axis in "xyz")))
        f.write(" }, // pos\n")

        f.write(line_prefix + INDENT)
        f.write(fmt_hex_s(v["rotY"], 4))
        f.write(", // rotY\n")

        f.write(line_prefix + INDENT)
        params = v["params"]
        f.write(fmt_hex_s(params, 4))
        if params < 0:
            params_u16 = params + 0x1_0000
            f.write(f" /* 0x{params_u16:04X} */")
        f.write(", // params\n")

        f.write(line_prefix)
        f.write("}")

        return True

    elem_cdata_ext = CDataExt_Struct(
        (
            (
                "sides",
                CDataExt_Array(
                    CDataExt_Struct(
                        (
                            ("room", CDataExt_Value.s8),
                            ("bgCamIndex", CDataExt_Value.s8),
                        )
                    ),
                    2,
                ),
            ),
            ("id", CDataExt_Value.s16),
            ("pos", cdata_ext_Vec3s),
            ("rotY", CDataExt_Value.s16),
            ("params", CDataExt_Value.s16),
        )
    ).set_write(write_elem)

    def get_c_declaration_base(self):
        return f"TransitionActorEntry {self.symbol_name}[{self.length_name}]"


class PathListResource(CDataArrayResource):
    def report_elem(resource, v):
        assert isinstance(v, dict)
        count = v["count"]
        assert isinstance(count, int)
        points = v["points"]
        assert isinstance(points, int)
        resource.file.memory_context.report_resource_at_segmented(
            points,
            lambda file, offset: Vec3sArrayResource(
                file, offset, f"{resource.name}_{points:08X}_Points", count
            ),
        )

    def write_elem(resource, v, f: io.TextIOBase, line_prefix: str):
        assert isinstance(v, dict)
        count = v["count"]
        assert isinstance(count, int)
        points = v["points"]
        assert isinstance(points, int)
        f.write(line_prefix)
        f.write("{ ")
        f.write(
            resource.file.memory_context.get_c_expression_length_at_segmented(points)
        )
        f.write(", ")
        f.write(resource.file.memory_context.get_c_reference_at_segmented(points))
        f.write(" }")
        return True

    elem_cdata_ext = (
        CDataExt_Struct(
            (
                ("count", CDataExt_Value.u8),
                ("pad1", CDataExt_Value.pad8),
                ("pad2", CDataExt_Value.pad16),
                ("points", CDataExt_Value("I")),  # Vec3s*
            )
        )
        .set_report(report_elem)
        .set_write(write_elem)
    )

    def try_parse_data(self):
        if self._length is None:
            # TODO guess
            self.set_length(1)
        super().try_parse_data()

    def get_c_declaration_base(self):
        return f"Path {self.symbol_name}[]"


class AltHeadersResource(CDataArrayResource):
    def report_elem(resource, v):
        assert isinstance(v, int)
        address = v
        if address != 0:
            resource.file.memory_context.report_resource_at_segmented(
                address,
                lambda file, offset: SceneCommandsResource(
                    file, offset, f"{resource.name}_{address:08X}_Cmds"
                ),
            )

    def write_elem(resource, v, f: io.TextIOBase, line_prefix: str):
        assert isinstance(v, int)
        address = v
        f.write(line_prefix)
        if address == 0:
            f.write("NULL")
        else:
            f.write(resource.file.memory_context.get_c_reference_at_segmented(address))
        return True

    elem_cdata_ext = (
        CDataExt_Value("I").set_report(report_elem).set_write(write_elem)
    )  # SceneCmd*

    def try_parse_data(self):
        length = 0
        for i, (v,) in enumerate(
            struct.iter_unpack(">I", self.file.data[self.range_start :])
        ):
            if v == 0:
                if i < 3:
                    length = i + 1
                    continue
                else:
                    break

            try:
                (
                    resolution,
                    resolution_info,
                ) = self.file.memory_context.resolve_segmented(v)
            except:
                break
            if resolution != SegmentedAddressResolution.FILE:
                break
            file, offset = resolution_info
            data_may_be_scenecmds = False
            for j in range(offset, len(file.data), 8):
                cmd_id_int = file.data[j]
                try:
                    cmd_id = SceneCmdId(cmd_id_int)
                except ValueError:
                    break
                if cmd_id == SceneCmdId.SCENE_CMD_ID_END:
                    data_may_be_scenecmds = True
                    break
            if not data_may_be_scenecmds:
                break
            length = i + 1
        assert length > 0
        self.set_length(length)
        super().try_parse_data()

    def get_c_declaration_base(self):
        return f"SceneCmd* {self.symbol_name}[]"
