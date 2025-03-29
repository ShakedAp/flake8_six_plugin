#!/usr/bin/env python3
import ast
import abc

from flake8_six_compatablity_plugin.flake8_errors_info import SIXErrorInfo
from flake8_six_compatablity_plugin.six_checkers.six_checker import SixChecker

STRING_MODULE_NAME = "string"
# found using common values betweem vars(str).keys() and vars(string).keys() in python2
STRING_COMMON_ATTRIBUTES = (
    "upper",
    "lstrip",
    "capitalize",
    "replace",
    "expandtabs",
    "strip",
    "ljust",
    "index",
    "rindex",
    "rsplit",
    "find",
    "split",
    "rstrip",
    "translate",
    "rjust",
    "swapcase",
    "zfill",
    "count",
    "lower",
    "join",
    "center",
    "rfind",
)
SYS_MODULE_NAME = "sys"
SYS_DEPRECATED_ATTRIBUTES = ("exc_type", "exc_value", "exc_traceback")


class UnallowedAttributesModuleImportChecker(abc.ABC, SixChecker):
    """
    Six Checker that checks that a given attributes are not imported from the give module nmae.

    Any inherting class needs to define the module_name, module_attributes, as well as the error_message.
    """

    module_name = ""
    module_attributes = tuple()

    @classmethod
    def check(cls, node: ast.ImportFrom, errors: list[SIXErrorInfo]) -> None:
        """
        Check that the given node is valid.
        If it is not valid, create the relevant error info and update errors.

        Args:
            node (ast.ImportFrom): The ast statement to check
            errors (list[SIXErrorInfo]): The error to be updated with found errors.
        """
        if node.module == cls.module_name and node.level == 0:
            for alias in node.names:
                if alias.name in cls.module_attributes:
                    errors.append(cls._create_six_error(alias))


class UnallowedAttributesModuleAccessChecker(abc.ABC, SixChecker):
    """
    Six Checker that checks that a given attributes are not accessed from the given module name.

    Any inherting class needs to define the module_name, module_attributes, as well as the error_message.
    """

    module_name = ""
    module_attributes = tuple()

    @classmethod
    def check(cls, node: ast.Attribute, errors: list[SIXErrorInfo]) -> None:
        """
        Check that the given node is valid.
        If it is not valid, create the relevant error info and update errors.

        Args:
            node (ast.Attribute): The ast statement to check
            errors (list[SIXErrorInfo]): The error to be updated with found errors.
        """
        if isinstance(node.value, ast.Name):
            if node.value.id == cls.module_name and node.attr in cls.module_attributes:
                errors.append(cls._create_six_error(node.value))


class UnallowedModuleImportRenameChecker(abc.ABC, SixChecker):
    """
    Six Checker that checks that a given module is not imported under a different name.

    Any inherting class needs to define the module_name as well as the error_message.
    """

    module_name = ""

    @classmethod
    def check(cls, node: ast.Import, errors: list[SIXErrorInfo]) -> None:
        """
        Check that the given node is valid.
        If it is not valid, create the relevant error info and update errors.

        Args:
            node (ast.Import): The ast statement to check
            errors (list[SIXErrorInfo]): The error to be updated with found errors.
        """
        for alias in node.names:
            if alias.name == cls.module_name and alias.asname is not None:
                errors.append(cls._create_six_error(alias))


class UnallowedAttributesStringImportChecker(UnallowedAttributesModuleImportChecker):
    module_name = STRING_MODULE_NAME
    module_attributes = STRING_COMMON_ATTRIBUTES
    error_message = f"Deprecated attribute import from the {STRING_MODULE_NAME} module - use str instead"


class UnallowedAttributesStringAccessChecker(UnallowedAttributesModuleAccessChecker):
    module_name = STRING_MODULE_NAME
    module_attributes = STRING_COMMON_ATTRIBUTES
    error_message = f"Deprecated attribute access from the {STRING_MODULE_NAME} module - use str instead"


class UnallowedStringImportRenameChecker(UnallowedModuleImportRenameChecker):
    module_name = STRING_MODULE_NAME
    error_message = f"Import {STRING_MODULE_NAME} under a different name is not allowed"


class UnallowedAttributesSysImportChecker(UnallowedAttributesModuleImportChecker):
    module_name = SYS_MODULE_NAME
    module_attributes = SYS_DEPRECATED_ATTRIBUTES
    error_message = f"Deprecated attribute import from the {SYS_MODULE_NAME} module - use sys.exc_info() instead"


class UnallowedAttributesSysAccessChecker(UnallowedAttributesModuleAccessChecker):
    module_name = SYS_MODULE_NAME
    module_attributes = SYS_DEPRECATED_ATTRIBUTES
    error_message = f"Deprecated attribute access from the {SYS_MODULE_NAME} module - use sys.exc_info() instead"


class UnallowedSysImportRenameChecker(UnallowedModuleImportRenameChecker):
    module_name = SYS_MODULE_NAME
    error_message = f"Import {SYS_MODULE_NAME} under a different name is not allowed"
