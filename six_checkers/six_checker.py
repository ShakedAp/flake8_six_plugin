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
