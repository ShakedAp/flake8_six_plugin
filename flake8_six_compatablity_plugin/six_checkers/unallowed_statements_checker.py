#!/usr/bin/env python3
import ast
import abc

from flake8_six_compatablity_plugin.flake8_errors_info import SIXErrorInfo
from flake8_six_compatablity_plugin.six_checkers.six_checker import SixChecker


class StatementNotAllowed(abc.ABC, SixChecker):
    """
    Six Checker that checks that a statement is not used at all.
    """

    @classmethod
    def check(cls, node: ast.stmt, errors: list[SIXErrorInfo]) -> None:
        """
        Check that the given node is valid.
        If it is not valid, create the relevant error info and update errors.

        Args:
            node (ast.stmt): The ast statement to check
            errors (list[SIXErrorInfo]): The error to be updated with found errors.
        """
        errors.append(cls._create_six_error(node))


class AnnAssignNotAllowed(StatementNotAllowed):
    error_message = (
        "Annotation Assignment is not allowed - it is not supported in python2"
    )


class AsyncForNotAllowed(StatementNotAllowed):
    error_message = "Async For is not allowed - it is not supported in python2"


class AsyncWithNotAllowed(StatementNotAllowed):
    error_message = "Async With is not allowed - it is not supported in python2"


class MatchNotAllowed(StatementNotAllowed):
    error_message = "Match is not allowed - it is not supported in python2"


class NonlocalNotAllowed(StatementNotAllowed):
    error_message = "Nonlocal is not allowed - it is not supported in python2"


class NamedExprNotAllowed(StatementNotAllowed):
    error_message = "Warlus operator is not allowed - it is not supported in python2"


class YieldFromNotAllowed(StatementNotAllowed):
    error_message = "Yield From is not allowed - it is not supported in python2"


class MatchValueNotAllowed(StatementNotAllowed):
    error_message = "Match Value is not allowed - it is not supported in python2"


class MatchSingletonNotAllowed(StatementNotAllowed):
    error_message = "Match Singleton is not allowed - it is not supported in python2"


class MatchSequenceNotAllowed(StatementNotAllowed):
    error_message = "Match Sequence is not allowed - it is not supported in python2"


class MatchMappingNotAllowed(StatementNotAllowed):
    error_message = "Match Mapping is not allowed - it is not supported in python2"


class MatchClassNotAllowed(StatementNotAllowed):
    error_message = "Match Class is not allowed - it is not supported in python2"


class MatchStarNotAllowed(StatementNotAllowed):
    error_message = "Match Star is not allowed - it is not supported in python2"


class MatchAsNotAllowed(StatementNotAllowed):
    error_message = "Match As is not allowed - it is not supported in python2"


class MatchOrNotAllowed(StatementNotAllowed):
    error_message = "Match Or is not allowed - it is not supported in python2"


class NameConstantNotAllowed(StatementNotAllowed):
    error_message = "Match Constant is not allowed - it is not supported in python2"
