#!/usr/bin/env python3
from typing import NamedTuple


class Flake8ASTErrorInfo(NamedTuple):
    """
    Flake8 Error info.

    line_number is the line number that the error was detected on.
    offset is the column that the error was detected on.
    msg is the message of the error - it needs to start with the plugin prefix. Otherwise the error is ignored.
    flake_cls is currently unused, but required. As a good practice pass the class that caused the error.
    """

    line_number: int
    offset: int
    msg: str
    flake_cls: type


class SIXErrorInfo(Flake8ASTErrorInfo):
    """
    six_compatibility_plugin Error Info.
    It adds the SIX prefix, and allows for requires to specify the error_number.
    """

    error_prefix = "SIX"

    def __new__(
        cls,
        line_number: int,
        offset: int,
        error_number: int,
        error_message: str,
        flake_cls: type,
    ):
        msg = f"{cls.error_prefix}{error_number:03} {error_message}"
        return super().__new__(cls, line_number, offset, msg, flake_cls)
