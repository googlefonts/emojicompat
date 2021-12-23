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
import pytest
from testdata_helper import *

from androidx.text.emoji.flatbuffer.MetadataList import MetadataList


def test_parse_sample_dat():
    buf = bytearray((testdata_dir() / "noto_emji_2_028.dat").read_bytes())
    metadata_list = MetadataList.GetRootAsMetadataList(buf, 0)
    assert metadata_list.ListLength() > 0  # verification of exact contents elsewhere
