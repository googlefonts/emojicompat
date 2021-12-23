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

import pytest

from androidx.text.emoji.flatbuffer.MetadataList import MetadataList
from emojicompat import compat_metadata
from testdata_helper import *


def test_emoji_metadata_superset_2_028_emoji():
    buf = bytearray((testdata_dir() / "noto_emji_2_028.dat").read_bytes())
    flat_list = MetadataList.GetRootAsMetadataList(buf, 0)
    flat_entries = tuple(flat_list.List(i) for i in range(flat_list.ListLength()))
    flat_entries = [
        compat_metadata.CompatEntry(
            e.Id(),
            e.SdkAdded(),
            e.CompatAdded(),
            tuple(e.Codepoints(i) for i in range(e.CodepointsLength())),
        )
        for e in flat_entries
    ]
    compat_entries = compat_metadata.metadata()

    assert len(flat_entries) <= len(
        compat_entries
    ), "compat entries should be a superset of 2.028 sample"

    for i in range(len(flat_entries)):
        assert flat_entries[i] == compat_entries[i], f"Mismatch at [{i}]"
