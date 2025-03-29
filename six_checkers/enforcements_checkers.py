#!/usr/bin/env python3
import ast

from six_checkers.six_checker import SixChecker
from flake8_errors_info import SIXErrorInfo


class OpenEncodingChecker(SixChecker):
    """
    Six Checker that checks that all the calls to open specify the encoding.
    example: open('name', encoding='utf-8')
    """

    error_message = "all open calls must specify the encoding"

    @classmethod
    def check(cls, node: ast.Call, errors: list[SIXErrorInfo]) -> None:
        """
        Check that the given node is valid.
        If it is not valid, create the relevant error info and update errors.

        Args:
            node (ast.Call): The ast statement to check
            errors (list[SIXErrorInfo]): The error to be updated with found errors.
        """
        if isinstance(node.func, ast.Name) and node.func.id == "open":
            keyword_names = [keyword.arg for keyword in node.keywords]
            if "encoding" not in keyword_names:
                errors.append(cls._create_six_error(node))
