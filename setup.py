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

from setuptools import setup, find_packages

setup_args = dict(
    name="emojicompat",
    use_scm_version={"write_to": "src/emojicompat/_version.py"},
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    entry_points={
        'console_scripts': [
            'emojicompat=emojicompat.emojicompat:main',
        ],
    },
    setup_requires=["setuptools_scm"],
    include_package_data=True,
    install_requires=[
        "absl-py>=2.0",
        "fonttools>=4.43.1",
        "flatbuffers>=2.0",
        "notofonttools>=0.2.19",  # unicode 15.1
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-clarity",
            "black==24.10.0",
            "pytype==2024.10.11",
        ],
    },
    # this is so we can use the built-in dataclasses module
    python_requires=">=3.9.5",

    # this is for type checker to use our inline type hints:
    # https://www.python.org/dev/peps/pep-0561/#id18
    package_data={
      "emojicompat": [
        "py.typed",
      ],
    },

    # metadata to display on PyPI
    author="Rod S",
    author_email="rsheeter@google.com",
    description=("Utility to insert emojicompat metadata into an emoji font"),
)


if __name__ == "__main__":
    setup(**setup_args)
