#!/usr/bin/env python3
import ast
import abc

from flake8_errors_info import SIXErrorInfo

def _should_update_error_counter(bases):
    if not bases:
        return False
    if abc.ABC in bases: 
        return False
    return True

class SixCheckerMeta(abc.ABCMeta):
    _error_number_counter = 1

    def __new__(cls, name, bases, dct):
        if _should_update_error_counter(bases):
            error_number = cls._error_number_counter
            cls._error_number_counter += 1
        else:
            error_number  = 0
        
        self = type.__new__(cls, name, bases, dct)
        self.error_number = error_number
        return self
    

class SixChecker(metaclass=SixCheckerMeta):
    error_message = ""

    @classmethod
    def _create_six_error(cls, node: ast.stmt) -> SIXErrorInfo:
        return SIXErrorInfo(node.lineno,
                            node.col_offset,
                            cls.error_number,
                            cls.error_message,
                            cls)

class CallFuncionNameNotAllowedChecker(abc.ABC, SixChecker):
    unallowed_name = ''

    @classmethod
    def check(cls, node: ast.Call, errors: list[SIXErrorInfo]) -> None:
        if isinstance(node.func, ast.Name) and node.func.id == cls.unallowed_name:
            errors.append(cls._create_six_error(node.func))

class FuncionDefNameNotAllowedChecker(abc.ABC, SixChecker):
    unallowed_name = ''

    @classmethod
    def check(cls, node: ast.FunctionDef, errors: list[SIXErrorInfo]) -> None:
        if node.name == cls.unallowed_name:
            errors.append(cls._create_six_error(node))

class InternNotAllowedChecker(CallFuncionNameNotAllowedChecker):
    unallowed_name = 'intern'
    error_message = "intern is not python3 compatible - use six.moves.intern"

class ReloadNotAllowedChecker(CallFuncionNameNotAllowedChecker):
    unallowed_name = 'reload'
    error_message = "reload is not python3 compatible - use six.moves.reload_module"

class CoerceNotAllowedChecker(CallFuncionNameNotAllowedChecker):
    unallowed_name = 'coerce'
    error_message = "coerce was removed in python3! Do not use it"

class CoerceMethodNotAllowedChecker(FuncionDefNameNotAllowedChecker):
    unallowed_name = '__coerce__'
    error_message = "__coerce__ special method was removed in python3! Do not use it"



class SixCompatibilityNodeVisitor(ast.NodeVisitor):
    
    def __init__(self):
        self.errors: list[SIXErrorInfo] = []
    
    def visit_Call(self, node: ast.Call) -> None:
        InternNotAllowedChecker.check(node, self.errors)
        ReloadNotAllowedChecker.check(node, self.errors)
        CoerceNotAllowedChecker.check(node, self.errors)

        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        CoerceMethodNotAllowedChecker.check(node, self.errors)

        self.generic_visit(node)


class SixCompatibilityPlugin:
    name='six_compatibility_plugin'
    version='1.0.0'

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self):
        visitor = SixCompatibilityNodeVisitor()
        visitor.visit(self._tree)

        yield from visitor.errors
