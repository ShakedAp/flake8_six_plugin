#!/usr/bin/env python3
from typing import NamedTuple

class Flake8ASTErrorInfo(NamedTuple):
    line_number: int
    offset: int
    msg: str
    flake_cls: type # Currently unused but required

class SIXErrorInfo(Flake8ASTErrorInfo):
    error_prefix="SIX"

    def __new__(cls,
                line_number: int,
                offset: int,
                error_number: int,
                error_message: str,
                flake_cls: type):
        msg = f"{cls.error_prefix}{error_number:03} {error_message}"
        return super().__new__(cls, line_number, offset, msg, flake_cls)