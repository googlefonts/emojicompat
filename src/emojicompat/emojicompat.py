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

from absl import app
from absl import flags
import dataclasses
from emojicompat.flatbuffer import FlatbufferItem, FlatbufferList
from emojicompat.util import bfs_base_table
from fontTools import ttLib
from fontTools.ttLib.tables import otTables as ot
from pathlib import Path


_LOOKUP_TYPE_LIGATURE = 4


FLAGS = flags.FLAGS


flags.DEFINE_enum("op", "dump", ["dump", "setup_pua", "check"], "What job to do.")
flags.DEFINE_string("font", None, "Font to process")
flags.mark_flag_as_required("font")


@dataclasses.dataclass
class PuaCheckResult:
    added: int = 0
    fixed: int = 0
    missing: int = 0
    correct: int = 0

    def print(self):
        print(f"{self.added} PUA missing")
        print(f"{self.fixed} PUA point at wrong glyph")
        print(f"{self.correct} PUA correct")
        print(f"{self.missing} Emji entries did NOT match a glyph")


def _definitely_not_emoji(cp: int) -> bool:
    return (
        # asci control, space
        # we don't care if these are repeatedly mapped
        (0x0000 <= cp <= 0x0020)
        # PUA
        or (0xE000 <= cp <= 0xF8FF)
        or (0xF0000 <= cp <= 0xFFFFD)
        or (0x100000 <= cp <= 0x10FFFD)
    )


def _dump(flat_list: FlatbufferList):
    item_title = "identifier emoji_style sdk_added compat_added width height codepoints"
    item_format = "{identifier:>10} {emoji_style:11} {sdk_added:9} {compat_added:12} {width:5} {height:6} {codepoints:>10}"
    print("version", flat_list.version)
    print(item_title)
    for item in flat_list.items:
        fields = item._asdict()
        fields["identifier"] = f"U+{fields['identifier']:04x}"
        fields["codepoints"] = ",".join(f"U+{c:04x}" for c in fields["codepoints"])
        print(item_format.format(**fields))
    print("source_sha", flat_list.source_sha)


def _setup_pua(font: ttLib.TTFont, flat_list: FlatbufferList) -> PuaCheckResult:
    # Target Android-style cmap rigging: there should be one format 12 we add to
    cmap_tables = [t for t in font["cmap"].tables if t.format == 12]

    # if we have many format 12 tables they should be identical
    if len(set(tuple(t.cmap.items()) for t in cmap_tables)) != 1:
        raise ValueError("All format 12 cmaps should be identical")
    cmap_table = cmap_tables[0]
    reverse_cmap = {
        k: v for k, v in cmap_table.cmap.items() if not _definitely_not_emoji(k)
    }
    assert len(reverse_cmap) == len(
        set(reverse_cmap.values())
    ), "Can't safely reverse if values are non-unique"
    reverse_cmap = {v: k for k, v in reverse_cmap.items()}

    items_by_codepoints = {e.codepoints: e for e in flat_list.items}

    result = PuaCheckResult()

    def _update_pua_entry(entry: FlatbufferItem, target_glyph: str):
        nonlocal result, items_by_codepoints
        if entry.identifier not in cmap_table.cmap:
            result.added += 1
        elif cmap_table.cmap[entry.identifier] == target_glyph:
            result.correct += 1
        else:
            result.fixed += 1
        cmap_table.cmap[entry.identifier] = target_glyph
        items_by_codepoints.pop(entry.codepoints)

    # Multi-codepoint sequences hide in GSUB as ligatures
    # Go find them and figure out the non-pua activation sequence
    for path in bfs_base_table(font["GSUB"].table, 'font["GSUB"]'):
        liga_subst = path[-1].value
        # if not isinstance(entry, ot.Lookup) or not not entry.LookupType == _LOOKUP_TYPE_LIGATURE:
        #     continue
        if not isinstance(liga_subst, ot.LigatureSubst):
            continue

        # for liga_subst in entry.SubTable:
        for start_glyph, ligatures in liga_subst.ligatures.items():
            for ligature in ligatures:
                activation = tuple(
                    reverse_cmap[glyph_name]
                    for glyph_name in [start_glyph] + ligature.Component
                )
                entry = items_by_codepoints.get(activation, None)
                if entry:
                    _update_pua_entry(entry, ligature.LigGlyph)

    # Single-codepoint lives directly in cmap
    single_cp_items = [
        e for e in items_by_codepoints.values() if len(e.codepoints) == 1
    ]
    for entry in single_cp_items:
        cp = entry.codepoints[0]
        glyph = cmap_table.cmap.get(cp, None)
        if glyph:
            _update_pua_entry(entry, glyph)

    # If there were multiple cmap format 12 tables correct the others
    for cmap_table in cmap_tables[1:]:
        cmap_table.cmap = cmap_tables[0].cmap

    result.missing = len(items_by_codepoints)

    return result


def _run(_):
    font_path = Path(FLAGS.font)
    assert font_path.is_file()

    font = ttLib.TTFont(font_path)
    flat_list = FlatbufferList.fromfont(font)

    if FLAGS.op == "dump":
        _dump(flat_list)
    elif FLAGS.op in {"setup_pua", "check"}:
        result = _setup_pua(font, flat_list)
        result.print()
        if FLAGS.op == "setup_pua":
            print(f"Updating {font_path}")
            font.save(font_path)
        # Else it was a check, do NOT save the changes


def main():
    # We don't seem to be __main__ when run as cli tool installed by setuptools
    app.run(_run)


if __name__ == "__main__":
    app.run(_run)
