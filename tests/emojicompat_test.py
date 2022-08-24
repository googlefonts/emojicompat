# Copyright 2022 Google LLC
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

from emojicompat.emojicompat import _setup_pua, PuaCheckResult
from emojicompat.flatbuffer import FlatbufferItem, FlatbufferList
from fontTools import ttLib
from testdata_helper import *
from typing import Tuple
import pytest


_SMILEY_SEQ = (0x263A,)
_SMILEY_PUA = 0xF8F0

_HANDSHAKE_LIGHT_SEQ = (0x1F91D, 0x1F3FB)
_HANDSHAKE_LIGHT_PUA = 0xF8F1

_HANDSHAKE_MEDIUM_SEQ = (0x1F91D, 0x1F3FC)
_HANDSHAKE_MEDIUM_PUA = 0xF8F2


def test_detect_and_correct_missing_pua():
    font = ttLib.TTFont(testdata_dir() / "Smiley.ttf")
    compat_metadata = FlatbufferList(
        version=42,
        items=(_compat_item(_SMILEY_PUA, _SMILEY_SEQ),),
        source_sha="do_not_care",
    )
    assert _setup_pua(font, compat_metadata) == PuaCheckResult(added=1)

    # once fixed should report as much
    assert _setup_pua(font, compat_metadata) == PuaCheckResult(correct=1)


def test_detect_missing_pua():
    font = ttLib.TTFont(testdata_dir() / "Smiley.ttf")
    compat_metadata = FlatbufferList(
        version=42,
        items=(_compat_item(_HANDSHAKE_LIGHT_PUA, _HANDSHAKE_LIGHT_SEQ),),
        source_sha="do_not_care",
    )
    assert _setup_pua(font, compat_metadata) == PuaCheckResult(missing=1)


def test_fix_pua():
    font = ttLib.TTFont(testdata_dir() / "Handshake.ttf")
    compat_metadata = FlatbufferList(
        version=42,
        items=(
            _compat_item(_HANDSHAKE_LIGHT_PUA, _HANDSHAKE_LIGHT_SEQ),
            _compat_item(_HANDSHAKE_MEDIUM_PUA, _HANDSHAKE_MEDIUM_SEQ),
        ),
        source_sha="do_not_care",
    )
    assert _setup_pua(font, compat_metadata) == PuaCheckResult(added=2)
    assert _setup_pua(font, compat_metadata) == PuaCheckResult(correct=2)

    # Light initially has the wrong target
    for cmap_table in font["cmap"].tables:
        if _HANDSHAKE_LIGHT_PUA in cmap_table.cmap:
            cmap_table.cmap[_HANDSHAKE_LIGHT_PUA] = cmap_table.cmap[
                _HANDSHAKE_MEDIUM_PUA
            ]

    # Correct the PUA for light
    assert _setup_pua(font, compat_metadata) == PuaCheckResult(fixed=1, correct=1)
    assert _setup_pua(font, compat_metadata) == PuaCheckResult(correct=2)


def _compat_item(pua: int, codepoints: Tuple[int, ...]) -> FlatbufferItem:
    return FlatbufferItem(
        identifier=pua,
        emoji_style=True,
        sdk_added=42,
        compat_added=11,
        width=42,
        height=42,
        codepoints=codepoints,
    )


# TODO test addition of meta *and* PUA
# TODO test multiple addition of meta and PUA
