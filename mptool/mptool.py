#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4

from __future__ import annotations

import sys
from math import inf
from typing import Any
from typing import BinaryIO

import msgpack
from epprint import epprint


def _output(
    *,
    arg: Any,
    tty: bool,
    verbose: bool | int | float,
    stderr: bool,
    flush: bool,
    file_handle: BinaryIO,
    file_handle_encoding: None | str,
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
        return

    message = msgpack.packb(arg)
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
    reason: Any,
    dict_output: bool,
    tty: bool,
    verbose: bool | int | float,
    stderr: bool = False,
    flush: bool = True,
    file_handle: BinaryIO = sys.stdout.buffer,
    file_handle_encoding: None | str = None,
) -> None:

    if dict_output:
        _arg = {reason: arg}
    else:
        _arg = arg
    del arg

    if stderr:
        file_handle = sys.stderr.buffer

    _output(
        arg=_arg,
        tty=tty,
        flush=flush,
        stderr=stderr,
        verbose=verbose,
        file_handle=file_handle,
        file_handle_encoding=file_handle_encoding,
    )
