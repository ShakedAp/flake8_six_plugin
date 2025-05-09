#!/usr/bin/env python3
import ast
import abc

from flake8_six_compatablity_plugin.flake8_errors_info import SIXErrorInfo
from flake8_six_compatablity_plugin.six_checkers.six_checker import SixChecker


class CallFuncionNameNotAllowedChecker(abc.ABC, SixChecker):
    """
    Six Checker that checks that a given name is not called as a function.

    Any inherting class needs to define the unallowed_name, as well as the error_message.
    """

    unallowed_name = ""

    @classmethod
    def check(cls, node: ast.Call, errors: list[SIXErrorInfo]) -> None:
        """
        Check that the given node is valid.
        If it is not valid, create the relevant error info and update errors.

        Args:
            node (ast.Call): The ast statement to check
            errors (list[SIXErrorInfo]): The error to be updated with found errors.
        """
        if isinstance(node.func, ast.Name) and node.func.id == cls.unallowed_name:
            errors.append(cls._create_six_error(node.func))


class FuncionDefNameNotAllowedChecker(abc.ABC, SixChecker):
    """
    Six Checker that checks that a given name is not defined as a function.

    Any inherting class needs to define the unallowed_name, as well as the error_message.
    """

    unallowed_name = ""

    @classmethod
    def check(cls, node: ast.FunctionDef, errors: list[SIXErrorInfo]) -> None:
        """
        Check that the given node is valid.
        If it is not valid, create the relevant error info and update errors.

        Args:
            node (ast.FunctionDef): The ast statement to check
            errors (list[SIXErrorInfo]): The error to be updated with found errors.
        """
        if node.name == cls.unallowed_name:
            errors.append(cls._create_six_error(node))


class InternNotAllowedChecker(CallFuncionNameNotAllowedChecker):
    unallowed_name = "intern"
    error_message = "intern is not python3 compatible - use six.moves.intern"


class ReloadNotAllowedChecker(CallFuncionNameNotAllowedChecker):
    unallowed_name = "reload"
    error_message = "reload is not python3 compatible - use six.moves.reload_module"


class CoerceNotAllowedChecker(CallFuncionNameNotAllowedChecker):
    unallowed_name = "coerce"
    error_message = "coerce was removed in python3! Do not use it"


class CoerceMethodNotAllowedChecker(FuncionDefNameNotAllowedChecker):
    unallowed_name = "__coerce__"
    error_message = "__coerce__ special method was removed in python3! Do not use it"
