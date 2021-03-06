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

from androidx.text.emoji.flatbuffer.MetadataList import MetadataList


def testdata_dir() -> Path:
    result = Path(__file__).parent / "testdata"
    assert result.is_dir()
    return result


def read_2_028_raw() -> bytes:
    return (testdata_dir() / "noto_emji_2_028.dat").read_bytes()


def read_2_028_sample() -> MetadataList:
    return MetadataList.GetRootAsMetadataList(bytearray(read_2_028_raw()), 0)
