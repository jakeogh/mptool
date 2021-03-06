#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4

from __future__ import annotations

import sys
# from collections.abc import Iterator
from math import inf
from typing import Any
from typing import BinaryIO

import msgpack
from epprint import epprint

# from typing import Type



## verbose can be math.inf
# def unmp(
#    *,
#    verbose: bool | int | float,
#    valid_types: None | list | tuple = None,
#    buffer_size: int = 1024,
#    skip: None | int = None,
#    single_type: bool = True,
#    strict_map_key: bool = False,  # True is the default
#    file_handle: BinaryIO = sys.stdin.buffer,
# ) -> Iterator[object]:
#
#    unpacker = msgpack.Unpacker(strict_map_key=strict_map_key, use_list=False)
#    index = 0
#    if valid_types:
#        for _type in valid_types:
#            if not isinstance(_type, Type):
#                raise ValueError(
#                    f"valid_types was passed with a non-Type member {_type=}"
#                )
#
#    found_type: Type = type(None)
#    for chunk in iter(lambda: file_handle.read(buffer_size), b""):
#        if verbose == inf:
#            epprint(
#                f"{valid_types=}",
#                f"{buffer_size=}",
#                f"{type(chunk)=}," f"{len(chunk)=}",
#                f"{chunk=}",
#            )
#        unpacker.feed(chunk)
#        for value in unpacker:
#            if single_type:
#                if index == 0:
#                    found_type = type(value)
#                else:
#                    if not isinstance(value, found_type):
#                        raise TypeError(f"{value=} does not match {found_type=}")
#            index += 1
#            if verbose == inf:
#                epprint(f"{index=}", f"{value=}")
#            if skip is not None:
#                if index <= skip:
#                    continue
#            if valid_types is not None:
#                if type(value) not in valid_types:
#                    raise TypeError(f"{type(value)} not in valid_types: {valid_types}")
#            yield value


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
    dict_input: bool,
    tty: bool,
    verbose: bool | int | float,
    stderr: bool = False,
    flush: bool = True,
    file_handle: BinaryIO = sys.stdout.buffer,
    file_handle_encoding: None | str = None,
) -> None:

    if dict_input:
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
