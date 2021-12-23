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
from typing import NamedTuple, Tuple

from androidx.text.emoji.flatbuffer.MetadataItem import *
from androidx.text.emoji.flatbuffer.MetadataList import *

from emojicompat.compat_metadata import *
from emojicompat.flatbuffer import *
from testdata_helper import *


def test_emoji_metadata_superset_2_028_emoji():
    flat_list = read_2_028_sample()
    flat_entries = FlatbufferList.fromflat(flat_list).compat_entries()
    compat_entries = emoji_compat_metadata()

    assert len(flat_entries) <= len(
        compat_entries
    ), "compat entries should be a superset of 2.028 sample"

    for i in range(len(flat_entries)):
        assert flat_entries[i] == compat_entries[i], f"Mismatch at [{i}]"
