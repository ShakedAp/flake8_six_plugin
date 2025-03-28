#!/usr/bin/env python3
import ast
import abc
from typing import Iterable

from flake8_errors_info import SIXErrorInfo


def _should_update_error_counter(bases: Iterable[type]) -> bool:
    """
    Args:
        bases (Iterable[type]): the clas ases to check.

    Returns:
        bool: True if error counter should be updated, False otherwise.
    """
    if not bases:
        return False
    if abc.ABC in bases:
        return False
    return True


class SixCheckerMeta(abc.ABCMeta):
    """
    The metclass for SIX Checkers.
    This metaclass gives each checker that inherits it a unique error_number
    The given error_number will shown when an error occured.

    Any class that will be the first to use this metaclass will not get an error_number.
    Any class that inherits abc.ABC will not get an error_number.
    """

    _error_number_counter = 1

    def __new__(cls, name, bases, dct):
        if _should_update_error_counter(bases):
            error_number = cls._error_number_counter
            cls._error_number_counter += 1
        else:
            error_number = 0

        self = type.__new__(cls, name, bases, dct)
        self.error_number = error_number
        return self


class SixChecker(metaclass=SixCheckerMeta):
    """
    The base class for each six checker.

    Make sure to override error_message with the relevant error_message.
    Make sure *not* to override error_number, unless a specific error number is wanted.
    """

    error_message = ""

    @classmethod
    def _create_six_error(cls, node: ast.stmt) -> SIXErrorInfo:
        """create the given error info based on the given node.
        This uses the defined error_message, and the automatically given error_number.
        If this method is not used, make sure to use those class member.

        Args:
            node (ast.stmt): the ast node that caused the error.

        Returns:
            SIXErrorInfo: The created error indo.
        """
        return SIXErrorInfo(
            node.lineno, node.col_offset, cls.error_number, cls.error_message, cls
        )
