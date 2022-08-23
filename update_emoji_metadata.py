"""Helper to update emoji_metadata.txt"""

from absl import app
from absl import flags
from emojicompat.compat_metadata import emoji_compat_metadata, emoji_metadata_file
import itertools
from nototools import unicode_data
from typing import Tuple


FLAGS = flags.FLAGS


flags.DEFINE_integer("sdk_added", None, "The SDK that will have the new sequences")


_IGNORED = {
    (0x20e3,),  # Keycap is an odd duck
    (0xfe82b,), # Shows up in unicode_data; not an emoji sequence per https://unicode.org/Public/emoji/15.0/emoji-test.txt
}


def _unqualify(seq: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(c for c in seq if c != 0xfe0f)


def main(_):
    current_metadata = emoji_compat_metadata()
    max_pua = max(c.identifier for c in current_metadata)
    max_sdk_added = max(c.sdk_added for c in current_metadata)
    max_compat_added = max(c.compat_added for c in current_metadata)
    current_emoji = set(c.codepoints for c in current_metadata)

    if FLAGS.sdk_added <= max_sdk_added:
        raise ValueError(f"New sdk added must exceed previous max, --sdk_added {FLAGS.sdk_added} < {max_sdk_added}")

    new_emoji = set(_unqualify(s) for s in unicode_data.get_emoji_sequences()) - current_emoji - _IGNORED
    print(f"{len(new_emoji)} new sequences, first few")
    for s in sorted(new_emoji)[:64]:
        print(" ".join(f"{c:04x}" for c in s))

    if new_emoji:
        pua_gen = itertools.chain(range(0xE000, 0xF8FF + 1), range(0xF0000, 0xFFFFD + 1), range(0x100000, 0x10FFFD + 1))
        while next(pua_gen) <= max_pua:
            continue

        with open(emoji_metadata_file(), "a") as f:
            for seq in sorted(new_emoji):
                pua = next(pua_gen)
                assert pua > max_pua

                seq = " ".join(f"{c:04X}" for c in seq)
                f.write(f"{pua:04X} {FLAGS.sdk_added} {max_compat_added + 1} {seq}\n")



if __name__ == "__main__":
    flags.mark_flag_as_required("sdk_added")
    app.run(main)
