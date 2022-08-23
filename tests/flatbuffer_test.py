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
from fontTools import ttLib
import pytest
import tempfile
from typing import NamedTuple, Tuple

from emojicompat.compat_metadata import *
from emojicompat.flatbuffer import *
from testdata_helper import *


def test_parse_sample_dat():
    flat_list = read_2_028_sample()
    assert flat_list.ListLength() > 1000  # verification of exact contents elsewhere


def test_roundtrip():
    before = FlatbufferList.fromflat(read_2_028_sample())
    after = FlatbufferList.fromflatbytes(before.toflatbytes())
    assert before == after


def test_fromfont():
    sample = FlatbufferList.fromflat(read_2_028_sample())

    font = ttLib.TTFont(testdata_dir() / "Smiley.ttf")
    from_font = FlatbufferList.fromfont(font)

    assert sample == from_font


def test_from_compat_entries():
    # The entries up to what is in the 2.028 sample should be identical

    sample = FlatbufferList.fromflat(read_2_028_sample())
    # sample = sample._replace(items=sample.items[:128])  # TEMPORARY
    compat_entries = emoji_compat_metadata()[: len(sample.items)]
    from_compat = FlatbufferList.from_compat_entries(compat_entries, sample.source_sha)

    assert sample._replace(items=()) == from_compat._replace(items=())

    # Try to get a nicer diff
    errors = []
    for idx, (e1, e2) in enumerate(zip(sample.items, from_compat.items)):
        if e1 == e2:
            continue
        errors.append((e1, e2))
    assert [e[0] for e in errors] == [e[1] for e in errors]

    # Match the whole darn thing just to be sure
    assert sample == from_compat


# NOTE: originally wanted to confirm binary identical recreation of 2.028
# but despite getting binaries with equivalent json the bytes differ; in
# retrospect this is fine.
