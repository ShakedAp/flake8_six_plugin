#!/usr/bin/env python3
import ast
from typing import Iterable

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

    error_message = (
        "all classes must inherit from at least one base (use object for default)"
    )

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


def _find_functiondefs_with_name(body: Iterable[ast.stmt], name: str):
    methods = []
    for method in body:
        if isinstance(method, ast.FunctionDef) and method.name == name:
            methods.append(method)
    return methods


class DivisionSpecialMethodsChecker(SixChecker):
    """
    Six Checker that checks that when implementing division special methods, all off them are implemented.
    For example, make sure that when __div__ is defined, __floordiv__ and __truediv__ are defined as well.
    """

    error_message = "when implementing division special method, all three should be implemented (__div__, __floordiv__, __truediv__)"

    @classmethod
    def check(cls, node: ast.ClassDef, errors: list[SIXErrorInfo]) -> None:
        """
        Check that the given node is valid.
        If it is not valid, create the relevant error info and update errors.

        Args:
            node (ast.ClassDef): The ast statement to check
            errors (list[SIXErrorInfo]): The error to be updated with found errors.
        """
        div_defs = _find_functiondefs_with_name(node.body, "__div__")
        floordiv_defs = _find_functiondefs_with_name(node.body, "__floordiv__")
        truediv_defs = _find_functiondefs_with_name(node.body, "__truediv__")

        if not div_defs or not floordiv_defs or not truediv_defs:
            for function_def in div_defs:
                errors.append(cls._create_six_error(function_def))
            for function_def in floordiv_defs:
                errors.append(cls._create_six_error(function_def))
            for function_def in truediv_defs:
                errors.append(cls._create_six_error(function_def))
