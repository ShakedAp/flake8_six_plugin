#!/usr/bin/env python3
import ast

from six_checkers.six_checker import SixChecker
from flake8_errors_info import SIXErrorInfo


class UnspecifiedStringPrefix(SixChecker):
    """
    Six Checker that checks that all the strings are explicitly unicode or bytes.
    """

    error_message = (
        "all strings must be prefixed with b or u (bytes or unicode respectively)"
    )

    @classmethod
    def check(cls, node: ast.Constant, errors: list[SIXErrorInfo]) -> None:
        """
        Check that the given node is valid.
        If it is not valid, create the relevant error info and update errors.

        Args:
            node (ast.Constant): The ast statement to check
            errors (list[SIXErrorInfo]): The error to be updated with found errors.
        """
        if isinstance(node.value, str) and node.kind is None:
            errors.append(cls._create_six_error(node))


class FStringsNotAllowedChecker(SixChecker):
    """
    Six Checker that checks that no f-strings are used.
    Example: f''.

    This can be detected via the apperance of ast.JoinedStr.
    """

    error_message = "f-strings are not allowed! They are not supported in python2"

    @classmethod
    def check(cls, node: ast.JoinedStr, errors: list[SIXErrorInfo]) -> None:
        """
        Check that the given node is valid.
        If it is not valid, create the relevant error info and update errors.

        Args:
            node (ast.JoinedStr): The ast statement to check
            errors (list[SIXErrorInfo]): The error to be updated with found errors.
        """
        errors.append(cls._create_six_error(node))
