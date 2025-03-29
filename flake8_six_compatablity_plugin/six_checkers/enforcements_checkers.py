#!/usr/bin/env python3
import ast

from flake8_six_compatablity_plugin.six_checkers.six_checker import SixChecker
from flake8_six_compatablity_plugin.flake8_errors_info import SIXErrorInfo


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


class ClassInheritanceChecker(SixChecker):
    """
    Six Checker that checks that all of the defined classes inherit from at least one thing.
    This is to ensure the parent is the object class.
    """

    error_message = "all classes must inherit from at least one base (use object for default)"

    @classmethod
    def check(cls, node: ast.ClassDef, errors: list[SIXErrorInfo]) -> None:
        """
        Check that the given node is valid.
        If it is not valid, create the relevant error info and update errors.

        Args:
            node (ast.ClassDef): The ast statement to check
            errors (list[SIXErrorInfo]): The error to be updated with found errors.
        """
        if not node.bases:
            errors.append(cls._create_six_error(node))
