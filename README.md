[![CI Build Status](https://github.com/googlefonts/emojicompat/workflows/Continuous%20Test%20+%20Deploy/badge.svg)](https://github.com/googlefonts/emojicompat/actions/workflows/ci.yml?query=workflow%3ATest)
[![PyPI](https://img.shields.io/pypi/v/emojicompat.svg)](https://pypi.org/project/emojicompat/)
[![Dependencies](https://badgen.net/github/dependabot/googlefonts/emojicompat)](https://github.com/googlefonts/emojicompat/network/updates)

# emojicompat

Utility to help create and verify fonts for https://developer.android.com/guide/topics/ui/look-and-feel/emoji-compat.

Requires Python 3.7 or greater.

## Test

Install the dev dependencies specified in [`extras_require`](https://github.com/googlefonts/emojicompat/blob/main/setup.py).

```shell
pip install -e .[dev]
pytest
```

If you use zsh, it will prompt an error(`zsh: no matches found: .[dev]`). Please use the following command:

```shell
pip install -e '.[dev]'
```

You can also use [pytest](https://docs.pytest.org/) to test the specified files individually.

```shell
pytest tests/svg_test.py
```

## Releasing

See https://googlefonts.github.io/python#make-a-release.
