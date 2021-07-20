#!/usr/bin/env python3.9

from PyStrong.Accepts import accepts
from PyStrong.Exceptions import InvalidTypeError, MismatchedTypeError, LambdaFunctionFailureError

import unittest


class TypingAcceptsTest(unittest.TestCase):

    def test_clean_types(self):
        """
        Types inside the decorator match with the
        function parameters
        """

        @accepts(int, int)
        def func(a: int, b: int):
            return a + b
        _resultant = func(1, 1)

    def test_dirty_types(self):
        """
        Same as test above, however the function
        instaniation is incorrect
        """

        with self.assertRaises(InvalidTypeError):
            @accepts(int, str)
            def func(a: int, b: str):
                return None
            func(1, 1)

    def test_mismatched_decorator(self):
        """
        Types inside the decorator do not match the
        function parameters
        """

        with self.assertRaises(MismatchedTypeError):
            @accepts(int, int)
            def func(a: int, b: bool):
                return None

    def test_union_types(self):
        """
        Intended usage of the unionization of types
        `int` belongs to the first parameter union, therefore it can be used
        """

        @accepts((int, float))
        def func(a: int):
            return a + 1

    def test_type_not_in_union(self):
        """
        Incorrect usage of the unionization of types
        `str` does not belong to the first parameter union, therefore it cannot be used
        """
        with self.assertRaises(MismatchedTypeError):
            @accepts((int, float))
            def func(a: str):
                return f'{a} {a}'

    def test_homogenous_type(self):
        """
        Ensure all the elements inside the container belong to
        indicated type.
        """
        @accepts(list[str])
        def func(a: list[str]):
            return None

        func(["jared", "dyreson"])

    def test_non_homogenous_type(self):
        """
        Ensure all the elements inside the container belong to
        indicated type. Failure to do so will result in MismatchedTypeError
        """

        with self.assertRaises(MismatchedTypeError):
            @accepts(list[str])
            def func(a: list[str]):
                return None

            func(["jared", 1])

    def test_lambda_checks(self):
        """
        If parameter needs a specialized function to be
        asserted, one can include it using the following format:


        @accepts(int, ensure_big_int=(0, lambda x: x > 100))
        def func(value: int):
            return value + 100
        """

        @accepts(int, ensure_big_int=(0, lambda x: x > 100))
        def func(value: int):
            return value + 100

        func(199)

    def test_failed_lambda_check(self):
        with self.assertRaises(LambdaFunctionFailureError):
            @accepts(int, ensure_big_int=(0, lambda x: x > 100))
            def func(value: int):
                return value + 100

            func(99)
