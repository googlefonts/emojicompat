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
import tempfile
from typing import NamedTuple, Tuple

from emojicompat.compat_metadata import *
from emojicompat.flatbuffer import *
from testdata_helper import *


def test_parse_sample_dat():
    flat_list = read_2_028_sample()
    assert flat_list.ListLength() > 0  # verification of exact contents elsewhere


def test_roundtrip():
    before = FlatbufferList.fromflat(read_2_028_sample())
    after = FlatbufferList.fromflatbytes(before.toflatbytes())
    assert before == after


# NOTE: originally wanted to confirm binary identical recreation of 2.028
# but despite getting binaries with equivalent json the bytes differ; in
# retrospect this is fine.
