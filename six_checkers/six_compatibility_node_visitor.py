import ast

from flake8_errors_info import SIXErrorInfo
from six_checkers.unallowed_name_checkers import (
    InternNotAllowedChecker,
    ReloadNotAllowedChecker,
    CoerceNotAllowedChecker,
    CoerceMethodNotAllowedChecker,
)


class SixCompatibilityNodeVisitor(ast.NodeVisitor):
    """
    An ast node visitor that keeps track of any errors found by checkers.
    """

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
