#!/usr/bin/env python3
import ast

from six_checkers.six_checker import SixChecker
from flake8_errors_info import SIXErrorInfo


class AsyncNotAllowedChecker(SixChecker):
    """
    Six Checker that checks that no async functions are used.
    Example: async def foo():.

    This can be detected via the apperance of ast.AsyncFunctionDef.
    """

    error_message = "async functions are not allowed! They are not supported in python2"

    @classmethod
    def check(cls, node: ast.AsyncFunctionDef, errors: list[SIXErrorInfo]) -> None:
        """
        Check that the given node is valid.
        If it is not valid, create the relevant error info and update errors.

        Args:
            node (ast.AsyncFunctionDef): The ast statement to check
            errors (list[SIXErrorInfo]): The error to be updated with found errors.
        """
        errors.append(cls._create_six_error(node))


class AwaitNotAllowedChecker(SixChecker):
    """
    Six Checker that checks that no await statements are used.
    Example: await other_func().

    This can be detected via the apperance of ast.Await.
    """

    error_message = (
        "await statements are not allowed! They are not supported in python2"
    )

    @classmethod
    def check(cls, node: ast.Await, errors: list[SIXErrorInfo]) -> None:
        """
        Check that the given node is valid.
        If it is not valid, create the relevant error info and update errors.

        Args:
            node (ast.Await): The ast statement to check
            errors (list[SIXErrorInfo]): The error to be updated with found errors.
        """
        errors.append(cls._create_six_error(node))
