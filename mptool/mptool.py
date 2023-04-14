#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4

from __future__ import annotations

import pprint
import sys
from collections.abc import Iterator
from math import inf
from typing import Any
from typing import BinaryIO

import msgpack
from epprint import epprint


# todo: this assumes unmp(single_type=True)
def mpd_enumerate(
    iterator,
    *,
    verbose: bool | int | float = False,
) -> Iterator[tuple[int, object, int]]:
    for index, _mpobj in enumerate(iterator):
        if verbose:
            epprint(index, _mpobj)
        if index == 0:
            first_type = type(_mpobj)
            if first_type == dict:
                key_count = len(list(_mpobj.keys()))
            else:
                key_count = 0
            # multi_key = False
            # if key_count:
            #    if key_count > 1:
            #        multi_key = True

        yield index, _mpobj, key_count
        # yield index, _mpobj, multi_key


def _output(
    *,
    arg: Any,
    tty: bool,
    stderr: bool,
    flush: bool,
    file_handle: BinaryIO,
    file_handle_encoding: None | str,
    verbose: bool | int | float = False,
) -> None:
    if verbose == inf:
        try:
            length = len(arg)
        except TypeError:
            length = None
        epprint(
            f"{tty=}",
            f"{type(arg)=}",
            f"{length=}",
            f"{arg=}",
            f"{file_handle=}",
            f"{flush=}",
            f"{stderr=}",
        )

    assert file_handle_encoding in [None, "utf8"]
    if tty:
        # TODO check if tty encoding is utf8
        if isinstance(arg, str):
            repr_arg = arg
        else:
            repr_arg = repr(arg)

        result_arg = repr_arg + "\n"
        if (
            not file_handle_encoding
        ):  # no encoding, convert to bytes from py native utf8 str
            result_arg = result_arg.encode("utf8")

        file_handle.write(result_arg)
        if flush:
            file_handle.flush()
        return

    message = msgpack.packb(arg)
    # a picle is not a mp type, so it's just bytes, not that useful
    # try:
    #    message = msgpack.packb(arg)
    # except TypeError as e:
    #    if verbose:
    #        epprint(e)
    #    message = msgpack.packb(pickle.dumps(arg))

    if verbose == inf:
        epprint(f"{repr(message)=}")

    file_handle.write(message)
    if flush:
        file_handle.flush()

    # if stderr:
    #    sys.stderr.buffer.write(message)
    #    sys.stderr.buffer.flush()
    # else:
    #    sys.stdout.buffer.write(message)
    #    if flush:
    #        sys.stderr.buffer.flush()


def output(
    arg,
    *,
    reason: Any,  # if this is a dict, use dict protocol
    dict_output: bool,
    first_type=None,
    stderr: bool = False,
    flush: bool = True,
    file_handle: BinaryIO = sys.stdout.buffer,
    file_handle_encoding: None | str = None,
    pretty_print: bool = False,
    tty: bool | None = None,
    verbose: bool | int | float = False,
) -> None:
    if pretty_print:
        if tty:
            pp = pprint.PrettyPrinter(indent=4)
            arg = pp.pformat(arg)

    if dict_output:
        _arg = {reason: arg}
    else:
        _arg = arg
    del arg

    if stderr:
        file_handle = sys.stderr.buffer

    if not tty:
        _tty = sys.stdout.isatty()
    else:
        _tty = tty

    _output(
        arg=_arg,
        tty=_tty,
        flush=flush,
        stderr=stderr,
        verbose=verbose,
        file_handle=file_handle,
        file_handle_encoding=file_handle_encoding,
    )
