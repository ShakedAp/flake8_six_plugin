#!/usr/bin/env python3
import ast

from six_checkers.six_compatibility_node_visitor import SixCompatibilityNodeVisitor


class SixCompatibilityPlugin:
    name = "six_compatibility_plugin"
    version = "1.0.0"

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self):
        visitor = SixCompatibilityNodeVisitor()
        visitor.visit(self._tree)

        yield from visitor.errors
