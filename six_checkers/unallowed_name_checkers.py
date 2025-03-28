#!/usr/bin/env python3
import ast
import abc

from flake8_errors_info import SIXErrorInfo
from six_checkers.six_checker import SixChecker


class CallFuncionNameNotAllowedChecker(abc.ABC, SixChecker):
    unallowed_name = ""

    @classmethod
    def check(cls, node: ast.Call, errors: list[SIXErrorInfo]) -> None:
        if isinstance(node.func, ast.Name) and node.func.id == cls.unallowed_name:
            errors.append(cls._create_six_error(node.func))


class FuncionDefNameNotAllowedChecker(abc.ABC, SixChecker):
    unallowed_name = ""

    @classmethod
    def check(cls, node: ast.FunctionDef, errors: list[SIXErrorInfo]) -> None:
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
