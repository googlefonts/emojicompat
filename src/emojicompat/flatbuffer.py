# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import flatbuffers
from pathlib import Path
from typing import NamedTuple, Tuple
from emojicompat.compat_metadata import CompatEntry

from androidx.text.emoji.flatbuffer.MetadataItem import *
from androidx.text.emoji.flatbuffer.MetadataList import *


# All the fields of the flatbuffer item
class FlatbufferItem(NamedTuple):
    identifier: int
    emoji_style: bool
    sdk_added: int
    compat_added: int
    width: int
    height: int
    codepoints: Tuple[int, ...]

    def compat_entry(self) -> CompatEntry:
        return CompatEntry(
            self.identifier,
            self.sdk_added,
            self.compat_added,
            self.codepoints,
        )

    @classmethod
    def fromflat(cls, flat: MetadataItem) -> "FlatbufferItem":
        return cls(
            flat.Id(),
            flat.EmojiStyle(),
            flat.SdkAdded(),
            flat.CompatAdded(),
            flat.Width(),
            flat.Height(),
            tuple(flat.Codepoints(i) for i in range(flat.CodepointsLength())),
        )


# All the fields of the flatbuffer list
class FlatbufferList(NamedTuple):
    version: int
    items: Tuple[FlatbufferItem, ...]
    source_sha: str

    def compat_entries(self) -> Tuple[CompatEntry]:
        return tuple(e.compat_entry() for e in self.items)

    def toflatbytes(self) -> bytearray:
        # See https://google.github.io/flatbuffers/flatbuffers_guide_tutorial.html
        builder = flatbuffers.Builder(65536)

        item_offsets = []
        for item in self.items:
            MetadataItemStartCodepointsVector(builder, len(item.codepoints))
            for codepoint in reversed(item.codepoints):
                builder.PrependInt32(codepoint)
            codepoint_vec = builder.EndVector()

            MetadataItemStart(builder)
            MetadataItemAddId(builder, item.identifier)
            MetadataItemAddEmojiStyle(builder, item.emoji_style)
            MetadataItemAddSdkAdded(builder, item.sdk_added)
            MetadataItemAddCompatAdded(builder, item.compat_added)
            MetadataItemAddWidth(builder, item.width)
            MetadataItemAddHeight(builder, item.height)
            MetadataItemAddCodepoints(builder, codepoint_vec)
            item_offsets.append(MetadataItemEnd(builder))

        MetadataListStartListVector(builder, len(self.items))
        for item_offset in reversed(item_offsets):
            builder.PrependUOffsetTRelative(item_offset)
        item_vec = builder.EndVector()

        source_sha = builder.CreateString(self.source_sha)

        MetadataListStart(builder)
        MetadataListAddVersion(builder, max(e.compat_added for e in self.items))
        MetadataListAddList(builder, item_vec)
        MetadataListAddSourceSha(builder, source_sha)
        list_offset = MetadataListEnd(builder)

        builder.Finish(list_offset)

        return builder.Output()

    @classmethod
    def fromflat(cls, flat: MetadataList) -> "FlatbufferList":
        return cls(
            flat.Version(),
            tuple(
                FlatbufferItem.fromflat(flat.List(i)) for i in range(flat.ListLength())
            ),
            flat.SourceSha(),
        )

    @classmethod
    def fromflatbytes(cls, flat: bytes) -> "FlatbufferList":
        return cls.fromflat(MetadataList.GetRootAsMetadataList(bytearray(flat), 0))
