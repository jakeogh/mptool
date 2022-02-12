#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4

# pylint: disable=C0111  # docstrings are always outdated and wrong
# pylint: disable=C0114  # Missing module docstring (missing-module-docstring)
# pylint: disable=W0511  # todo is encouraged
# pylint: disable=C0301  # line too long
# pylint: disable=R0902  # too many instance attributes
# pylint: disable=C0302  # too many lines in module
# pylint: disable=C0103  # single letter var names, func name too descriptive
# pylint: disable=R0911  # too many return statements
# pylint: disable=R0912  # too many branches
# pylint: disable=R0915  # too many statements
# pylint: disable=R0913  # too many arguments
# pylint: disable=R1702  # too many nested blocks
# pylint: disable=R0914  # too many local variables
# pylint: disable=R0903  # too few public methods
# pylint: disable=E1101  # no member for base
# pylint: disable=W0201  # attribute defined outside __init__
# pylint: disable=R0916  # Too many boolean expressions in if statement
# pylint: disable=C0305  # Trailing newlines editor should fix automatically, pointless warning
# pylint: disable=C0413  # TEMP isort issue [wrong-import-position] Import "from pathlib import Path" should be placed at the top of the module [C0413]


import os
import sys
import time
from math import inf
from pathlib import Path
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal
from typing import ByteString
from typing import Generator
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import click
import msgpack
import sh
from asserttool import eprint
from asserttool import ic
from asserttool import tv
from asserttool import validate_slice
from click_auto_help import AHGroup
from clicktool import click_add_options
from clicktool import click_global_options
from enumerate_input import enumerate_input
from printtool import output
from retry_on_exception import retry_on_exception
from timetool import get_timestamp

signal(SIGPIPE, SIG_DFL)


def unmp(*,
         verbose: int,
         valid_types: Optional[Union[list, tuple]] = None,
         buffer_size: int = 1024,
         skip: Optional[int] = None,
         single_type: bool = True,
         ) -> Iterator[object]:

    unpacker = msgpack.Unpacker()
    index = 0
    found_type = None
    for chunk in iter(lambda: sys.stdin.buffer.read(buffer_size), b""):
        if verbose == inf:
            ic(valid_types, buffer_size, type(chunk), len(chunk), chunk)
        unpacker.feed(chunk)
        for value in unpacker:
            if single_type:
                if index == 0:
                    found_type = type(value)
                else:
                    assert isinstance(value, found_type)
            index += 1
            if verbose == inf:
                ic(index, value)
            if skip is not None:
                if index <= skip:
                    continue
            #assert isinstance(value, list)
            if valid_types is not None:
                if type(value) not in valid_types:
                    raise TypeError('{} not in valid_types: {}'.format(type(value), valid_types))
            yield value


#@with_plugins(iter_entry_points('click_command_tree'))
#@click.group(no_args_is_help=True, cls=AHGroup)
#@click_add_options(click_global_options)
#@click.pass_context
#def cli(ctx,
#        verbose: int,
#        verbose_inf: bool,
#        ):
#
#    tty, verbose = tv(ctx=ctx,
#                      verbose=verbose,
#                      verbose_inf=verbose_inf,
#                      )


#@click.command()
#@click.argument("paths", type=str, nargs=-1)
#@click.option('--ipython', is_flag=True)
#@click_add_options(click_global_options)
#@click.pass_context
#def cli(ctx,
#        paths: tuple[str],
#        ipython: bool,
#        verbose: int,
#        verbose_inf: bool,
#        ):
#
#    tty, verbose = tv(ctx=ctx,
#                      verbose=verbose,
#                      verbose_inf=verbose_inf,
#                      )
#
#    if paths:
#        iterator = paths
#    else:
#        iterator = unmp(valid_types=[bytes,], verbose=verbose)
#    del paths
#
