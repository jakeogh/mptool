#!/usr/bin/env python3

import pprint
import sys
from collections.abc import Iterator
from typing import Any
from typing import BinaryIO

import msgpack
from eprint import eprint
from globalverbose import gvd


# assumes unmp(single_type=True)
def mpd_enumerate(
    iterator,
    *,
    verbose: bool = False,
) -> Iterator[tuple[int, object, int]]:
    key_count = 0
    for index, _mpobj in enumerate(iterator):
        if verbose:
            eprint(index, _mpobj)
        if index == 0:
            if isinstance(_mpobj, dict):
                key_count = len(_mpobj)
            else:
                key_count = 0
        yield index, _mpobj, key_count


def _output(
    *,
    arg: Any,
    tty: bool,
    flush: bool,
    file_handle: BinaryIO,
    file_handle_encoding: None | str,
    verbose: bool = False,
) -> None:
    if gvd:
        try:
            length = len(arg)
        except TypeError:
            length = None
        try:
            repr_length = len(repr(arg))
        except TypeError:
            repr_length = None
        eprint(
            f"{tty=}",
            f"{type(arg)=}",
            f"{length=}",
            f"{repr_length=}",
            f"{arg=}",
            f"{file_handle=}",
            f"{flush=}",
        )

    assert file_handle_encoding in {None, "utf8"}
    if tty:
        if isinstance(arg, str):
            repr_arg = arg
        else:
            repr_arg = repr(arg)

        result_arg = repr_arg + "\n"
        if not file_handle_encoding:
            result_arg = result_arg.encode("utf8")

        file_handle.write(result_arg)
        if flush:
            file_handle.flush()
        return

    message = msgpack.packb(arg)

    if gvd:
        eprint(f"{repr(message)=}")

    file_handle.write(message)
    if flush:
        file_handle.flush()


def output(
    arg,
    *,
    reason: Any,  # if dict_output, becomes the dict key
    dict_output: bool = False,
    stderr: bool = False,
    flush: bool = True,
    file_handle: BinaryIO = sys.stdout.buffer,
    file_handle_encoding: None | str = None,
    pretty_print: bool = False,
    tty: None | bool = None,
    verbose: bool = False,
) -> None:
    if tty is None:
        tty = sys.stdout.isatty()

    if pretty_print and tty:
        arg = pprint.PrettyPrinter(indent=4).pformat(arg)

    if dict_output:
        arg = {reason: arg}

    if stderr:
        file_handle = sys.stderr.buffer

    _output(
        arg=arg,
        tty=tty,
        flush=flush,
        verbose=verbose,
        file_handle=file_handle,
        file_handle_encoding=file_handle_encoding,
    )
