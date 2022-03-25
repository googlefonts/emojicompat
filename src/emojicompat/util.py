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

# TODO if/when FontTools provides traversal algorithm delete dfs/bfs base table

from collections import deque
from fontTools.ttLib.tables import otBase
from fontTools.ttLib.tables import otTables
from fontTools.ttLib.tables import otConverters
from typing import Callable, Deque, Iterable, List, Tuple


SubTablePath = Tuple[otBase.BaseTable.SubTableEntry, ...]

# Given f(current frontier, new entries) add new entries to frontier
AddToFrontierFn = Callable[[Deque[SubTablePath], List[SubTablePath]], None]


def dfs_base_table(
    root: otBase.BaseTable, root_accessor: str
) -> Iterable[SubTablePath]:
    yield from _traverse_ot_data(
        root, root_accessor, lambda frontier, new: frontier.extendleft(reversed(new))
    )


def bfs_base_table(
    root: otBase.BaseTable, root_accessor: str
) -> Iterable[SubTablePath]:
    yield from _traverse_ot_data(
        root, root_accessor, lambda frontier, new: frontier.extend(new)
    )


def _traverse_ot_data(
    root: otBase.BaseTable, root_accessor: str, add_to_frontier_fn: AddToFrontierFn
) -> Iterable[SubTablePath]:
    # no visited because general otData is forward-offset only and thus cannot cycle

    frontier: Deque[SubTablePath] = deque()
    frontier.append((otBase.BaseTable.SubTableEntry(root_accessor, root),))
    while frontier:
        # path is (value, attr_name) tuples. attr_name is attr of parent to get value
        path = frontier.popleft()
        current = path[-1].value

        yield path

        new_entries = []
        for subtable_entry in current.iterSubTables():
            new_entries.append(path + (subtable_entry,))

        add_to_frontier_fn(frontier, new_entries)
