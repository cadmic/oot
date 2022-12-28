import abc
import io
from typing import Callable, Any, Sequence

from . import Resource, File

from .repr_c_struct import CData, CData_Value, CData_Struct, CData_Array


class CDataExt(CData, abc.ABC):

    report_f = None
    write_f = None

    # TODO not sure what to name this, it doesn't have to be used for pointer reporting,
    # more generic "callback" may be better idk yet
    def set_report(self, report_f: Callable[["CDataResource", Any], None]):
        self.report_f = report_f
        return self

    def set_write(
        self, write_f: Callable[["CDataResource", Any, io.TextIOBase, str], bool]
    ):
        self.write_f = write_f
        return self

    def freeze(self):
        self.set_report = None
        self.set_write = None
        return self

    @abc.abstractmethod
    def write_default(
        self, resource: "CDataResource", v: Any, f: io.TextIOBase, line_prefix
    ) -> bool:
        ...

    def report(self, resource: "CDataResource", v: Any):
        if self.report_f:
            try:
                self.report_f(resource, v)
            except:
                print("Error reporting data", self, self.report_f, resource, v)
                raise

    def write(
        self, resource: "CDataResource", v: Any, f: io.TextIOBase, line_prefix
    ) -> bool:
        """
        Returns True if something has been written
        (typically, False will be returned if this data is struct padding)
        """
        if self.write_f:
            ret = self.write_f(resource, v, f, line_prefix)
            # This assert is meant to ensure the function returns a value at all,
            # since it's easy to forget to return a value (typically True)
            assert isinstance(ret, bool), ("must return a bool", self.write_f)
        else:
            ret = self.write_default(resource, v, f, line_prefix)
            assert isinstance(ret, bool), self
        return ret


class CDataExt_Value(CData_Value, CDataExt):
    is_padding = False

    def padding(self):
        self.is_padding = True
        return self

    def freeze(self):
        self.padding = None
        return super().freeze()

    def report(self, resource: "CDataResource", v: Any):
        super().report(resource, v)
        if self.is_padding:
            if v != 0:
                raise Exception("non-0 padding")

    def write_default(
        self, resource: "CDataResource", v: Any, f: io.TextIOBase, line_prefix
    ):
        if not self.is_padding:
            f.write(line_prefix)
            f.write(str(v))
            return True
        else:
            return False


CDataExt_Value.s8 = CDataExt_Value("b").freeze()
CDataExt_Value.u8 = CDataExt_Value("B").freeze()
CDataExt_Value.s16 = CDataExt_Value("h").freeze()
CDataExt_Value.u16 = CDataExt_Value("H").freeze()
CDataExt_Value.s32 = CDataExt_Value("i").freeze()
CDataExt_Value.u32 = CDataExt_Value("I").freeze()
CDataExt_Value.f32 = CDataExt_Value("f").freeze()
CDataExt_Value.f64 = CDataExt_Value("d").freeze()
CDataExt_Value.pointer = CDataExt_Value("I").freeze()

CDataExt_Value.pad8 = CDataExt_Value("b").padding().freeze()
CDataExt_Value.pad16 = CDataExt_Value("h").padding().freeze()
CDataExt_Value.pad32 = CDataExt_Value("i").padding().freeze()


INDENT = " " * 4


class CDataExt_Array(CData_Array, CDataExt):
    def __init__(self, element_cdata_ext: CDataExt, length: int):
        super().__init__(element_cdata_ext, length)
        self.element_cdata_ext = element_cdata_ext

    def report(self, resource: "CDataResource", v: Any):
        assert isinstance(v, list)
        super().report(resource, v)
        for elem in v:
            self.element_cdata_ext.report(resource, elem)

    def write_default(
        self, resource: "CDataResource", v: Any, f: io.TextIOBase, line_prefix
    ):
        assert isinstance(v, list)
        f.write(line_prefix)
        f.write("{\n")
        for i, elem in enumerate(v):
            ret = self.element_cdata_ext.write(resource, elem, f, line_prefix + INDENT)
            assert ret
            f.write(f", // {i}\n")
        f.write(line_prefix)
        f.write("}")
        return True


class CDataExt_Struct(CData_Struct, CDataExt):
    def __init__(self, members: Sequence[tuple[str, CDataExt]]):
        super().__init__(members)
        self.members_ext = members

    def report(self, resource: "CDataResource", v: Any):
        assert isinstance(v, dict)
        super().report(resource, v)
        for member_name, member_cdata_ext in self.members_ext:
            member_cdata_ext.report(resource, v[member_name])

    def write_default(
        self, resource: "CDataResource", v: Any, f: io.TextIOBase, line_prefix
    ):
        assert isinstance(v, dict)
        f.write(line_prefix)
        f.write("{\n")
        for member_name, member_cdata_ext in self.members_ext:
            if member_cdata_ext.write(
                resource, v[member_name], f, line_prefix + INDENT
            ):
                f.write(f", // {member_name}\n")
        f.write(line_prefix)
        f.write("}")
        return True


class CDataResource(Resource):

    # Set by child classes
    cdata_ext: CDataExt

    # Resource implementation

    def __init__(self, file: File, range_start: int, name: str):
        if not self.can_size_be_unknown:
            assert hasattr(self, "cdata_ext")
            assert self.cdata_ext is not None
            range_end = range_start + self.cdata_ext.size
        else:
            if hasattr(self, "cdata_ext") and self.cdata_ext is not None:
                range_end = range_start + self.cdata_ext.size
            else:
                range_end = None
        super().__init__(file, range_start, range_end, name)
        self.is_cdata_processed = False

    def try_parse_data(self):
        if self.can_size_be_unknown:
            assert hasattr(self, "cdata_ext") and self.cdata_ext is not None, (
                "Subclasses with can_size_be_unknown=True should redefine try_parse_data"
                " and call the superclass definition (CDataResource.try_parse_data)"
                " only once cdata_ext has been set",
                self.__class__,
            )
            assert (
                self.range_end is not None
            ), "Subclasses with can_size_be_unknown=True should also set range_end once the size is known"
        assert hasattr(self, "cdata_ext")
        assert self.cdata_ext is not None

        # Use own bool is_cdata_processed to remember if data has been unpacked and
        # reported already, to let subclasses use is_data_parsed if they want to
        if not self.is_cdata_processed:
            self.cdata_unpacked = self.cdata_ext.unpack_from(
                self.file.data, self.range_start
            )

            self.cdata_ext.report(self, self.cdata_unpacked)

            self.is_cdata_processed = True

        self.is_data_parsed = True

    def write_extracted(self):
        with self.extract_to_path.open("w") as f:
            self.cdata_ext.write(self, self.cdata_unpacked, f, "")
            f.write("\n")


class Vec3sArrayResource(CDataResource):

    elem_cdata_ext = CDataExt_Struct(
        (
            ("x", CDataExt_Value.s16),
            ("y", CDataExt_Value.s16),
            ("z", CDataExt_Value.s16),
        )
    )

    def __init__(self, file: File, range_start: int, name: str, length: int):
        assert length > 0
        self.cdata_ext = CDataExt_Array(self.elem_cdata_ext, length)
        super().__init__(file, range_start, name)

    def get_c_declaration_base(self):
        return f"Vec3s {self.symbol_name}[]"

    def get_c_reference(self, resource_offset: int):
        raise NotImplementedError()
