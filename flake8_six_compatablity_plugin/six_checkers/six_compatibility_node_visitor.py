#!/usr/bin/env python3
import ast
from typing import Dict, Tuple, Iterable

from flake8_six_compatablity_plugin.flake8_errors_info import SIXErrorInfo
from flake8_six_compatablity_plugin.six_checkers.six_checker import SixChecker
from flake8_six_compatablity_plugin.six_checkers.enforcements_checkers import (
    OpenEncodingChecker,
)
from flake8_six_compatablity_plugin.six_checkers.unallowed_name_checkers import (
    InternNotAllowedChecker,
    ReloadNotAllowedChecker,
    CoerceNotAllowedChecker,
    CoerceMethodNotAllowedChecker,
)
from flake8_six_compatablity_plugin.six_checkers.constant_checkers import (
    UnspecifiedStringPrefix,
    FStringsNotAllowedChecker,
)
from flake8_six_compatablity_plugin.six_checkers.deprecated_import_checkers import (
    UnallowedAttributesStringImportChecker,
    UnallowedAttributesStringAccessChecker,
    UnallowedStringImportRenameChecker,
    UnallowedAttributesSysImportChecker,
    UnallowedAttributesSysAccessChecker,
    UnallowedSysImportRenameChecker,
)
from flake8_six_compatablity_plugin.six_checkers.await_async_checkers import (
    AsyncNotAllowedChecker,
    AwaitNotAllowedChecker,
)


NODE_VISITOR_VISIT_METHOD_FORMAT = "visit_{}"


def _create_visit_method(checkers: Iterable[SixChecker]) -> callable:
    """Create the visit method from the given checkers.

    Args:
        checkers (Iterable[SixChecker]): The checkers to run on each relevant node visit.

    Returns:
        callable: A visit method that runs the check function on all the given checkers and calls generic_visit at the end.
    """

    def visit(self: ast.NodeVisitor, node: ast.stmt) -> None:
        for checker in checkers:
            checker.check(node, self.errors)

        self.generic_visit(node)

    return visit


def _add_node_checkers_to_methods(
    node_checkers: Dict[str, Tuple[SixChecker]], dct: dict
) -> None:
    """
    Add ast Node Visitor visit functions from the given node_checkers.

    Args:
        node_checkers (Dict[str, Tuple[SixChecker]]): A dictionary that maps between the visit function name and the checkers to run.
        dct (dict): The attribute dicts to be updated.
    """
    for node_name, checkers in node_checkers.items():
        method_name = NODE_VISITOR_VISIT_METHOD_FORMAT.format(node_name)
        dct[method_name] = _create_visit_method(checkers)


class NodeCheckerAdderMeta(type):
    """
    A metaclass that populates all of the ast Node Visitor visit functions from the defined node_checkers.
    """

    def __new__(cls, name, bases, dct):
        node_checkers = dct.get("node_checkers", {})
        _add_node_checkers_to_methods(node_checkers, dct)

        return super().__new__(cls, name, bases, dct)


class SixCompatibilityNodeVisitor(ast.NodeVisitor, metaclass=NodeCheckerAdderMeta):
    """
    An ast node visitor that keeps track of any errors found by checkers.

    The node visitors are populated using the metaclass, and the node_checkers dict.
    Each key in the dict is being used to created the corresponding visit function, and calls the check method for all
    of the listed checkers.

    For example, adding Call will create visit_Call that will run all it's checkers.
    """

    node_checkers: Dict[str, Tuple[SixChecker]] = {
        "Call": (
            InternNotAllowedChecker,
            ReloadNotAllowedChecker,
            CoerceNotAllowedChecker,
            OpenEncodingChecker,
        ),
        "Import": (UnallowedStringImportRenameChecker, UnallowedSysImportRenameChecker),
        "ImportFrom": (
            UnallowedAttributesStringImportChecker,
            UnallowedAttributesSysImportChecker,
        ),
        "Attribute": (
            UnallowedAttributesStringAccessChecker,
            UnallowedAttributesSysAccessChecker,
        ),
        "FunctionDef": (CoerceMethodNotAllowedChecker,),
        "Constant": (UnspecifiedStringPrefix,),
        "JoinedStr": (FStringsNotAllowedChecker,),
        "Await": (AwaitNotAllowedChecker,),
        "AsyncFunctionDef": (AsyncNotAllowedChecker,),
    }

    def __init__(self):
        self.errors: list[SIXErrorInfo] = []
