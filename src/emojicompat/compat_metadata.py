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

from pathlib import Path
from typing import NamedTuple, Tuple


# An entry in emoji_metadata.txt
class CompatEntry(NamedTuple):
    identifier: int
    sdk_added: int
    compat_added: int
    codepoints: Tuple[int, ...]

    @classmethod
    def fromstring(cls, line: str) -> "CompatEntry":
        parts = line.split(" ", 3)
        assert len(parts) == 4, line
        return CompatEntry(
            int(parts[0], 16),
            int(parts[1]),
            int(parts[2]),
            tuple(int(s, 16) for s in parts[3].split(" ")),
        )


def emoji_compat_metadata() -> Tuple[CompatEntry, ...]:
    with open(Path(__file__).parent / "emoji_metadata.txt") as f:
        return tuple(
            CompatEntry.fromstring(l)
            for l in f
            if l.strip() and not l.strip().startswith("#")
        )
