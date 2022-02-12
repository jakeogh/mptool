#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4

## pylint: disable=C0111  # docstrings are always outdated and wrong
## pylint: disable=C0114  # Missing module docstring (missing-module-docstring)
## pylint: disable=W0511  # todo is encouraged
## pylint: disable=C0301  # line too long
## pylint: disable=R0902  # too many instance attributes
## pylint: disable=C0302  # too many lines in module
## pylint: disable=C0103  # single letter var names, func name too descriptive
## pylint: disable=R0911  # too many return statements
## pylint: disable=R0912  # too many branches
## pylint: disable=R0915  # too many statements
## pylint: disable=R0913  # too many arguments
## pylint: disable=R1702  # too many nested blocks
## pylint: disable=R0914  # too many local variables
## pylint: disable=R0903  # too few public methods
## pylint: disable=E1101  # no member for base
## pylint: disable=W0201  # attribute defined outside __init__
## pylint: disable=R0916  # Too many boolean expressions in if statement
## pylint: disable=C0305  # Trailing newlines editor should fix automatically, pointless warning
## pylint: disable=C0413  # TEMP isort issue [wrong-import-position] Import "from pathlib import Path" should be placed at the top of the module [C0413]


import sys
from math import inf
from typing import Iterator
from typing import Optional
from typing import Type
from typing import Union

import msgpack
from printtool import output


def unmp(*,
         verbose: Union[bool, int, float],  # verbose can be math.inf
         valid_types: Optional[Union[list, tuple]] = None,
         buffer_size: int = 1024,
         skip: Optional[int] = None,
         single_type: bool = True,
         ) -> Iterator[object]:

    unpacker = msgpack.Unpacker()
    index = 0
    if valid_types:
        for _type in valid_types:
            if not isinstance(_type, Type):
                raise ValueError(f'valid_types was passed with a non-Type member {_type=}')

    found_type: Type = type(None)
    for chunk in iter(lambda: sys.stdin.buffer.read(buffer_size), b""):
        if verbose == inf:
            print(f"{valid_types=}", f"{buffer_size=}", f"{type(chunk)=}," f"{len(chunk)=}", f"{chunk=}", file=sys.stderr)
        unpacker.feed(chunk)
        for value in unpacker:
            if single_type:
                if index == 0:
                    found_type = type(value)
                else:
                    if not isinstance(value, found_type):
                        raise TypeError(f'{value=} does not match {found_type=}')
            index += 1
            if verbose == inf:
                print(f"{index=}", f"{value=}", file=sys.stderr)
            if skip is not None:
                if index <= skip:
                    continue
            if valid_types is not None:
                if type(value) not in valid_types:
                    raise TypeError(f'{type(value)} not in valid_types: {valid_types}')
            yield value

