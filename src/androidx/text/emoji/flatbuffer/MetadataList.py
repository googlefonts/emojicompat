# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flatbuffer

import flatbuffers
from flatbuffers.compat import import_numpy

np = import_numpy()


class MetadataList(object):
    __slots__ = ["_tab"]

    @classmethod
    def GetRootAsMetadataList(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = MetadataList()
        x.Init(buf, n + offset)
        return x

    # MetadataList
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # MetadataList
    def Version(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # MetadataList
    def List(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from androidx.text.emoji.flatbuffer.MetadataItem import MetadataItem

            obj = MetadataItem()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # MetadataList
    def ListLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # MetadataList
    def ListIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

    # MetadataList
    def SourceSha(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None


def MetadataListStart(builder):
    builder.StartObject(3)


def MetadataListAddVersion(builder, version):
    builder.PrependInt32Slot(0, version, 0)


def MetadataListAddList(builder, list):
    builder.PrependUOffsetTRelativeSlot(
        1, flatbuffers.number_types.UOffsetTFlags.py_type(list), 0
    )


def MetadataListStartListVector(builder, numElems):
    return builder.StartVector(4, numElems, 4)


def MetadataListAddSourceSha(builder, sourceSha):
    builder.PrependUOffsetTRelativeSlot(
        2, flatbuffers.number_types.UOffsetTFlags.py_type(sourceSha), 0
    )


def MetadataListEnd(builder):
    return builder.EndObject()
