#!/usr/bin/env python3.9

from PyStrong.Accepts import accepts
from PyStrong.Exceptions import InvalidTypeError, MismatchedTypeError

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
        Same as test above, however the functinon
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
        @accepts((int, float))
        def func(a: int):
            return a + 1

    @unittest.skip("")
    def test_homogenous_type(self):
        @accepts(list[str])
        def func(a: list[str]):
            return None

        func(["jared", "dyreson"])

    @unittest.skip("")
    def test_non_homogenous_type(self):
        with self.assertRaises(MismatchedTypeError):
            @accepts(list[str])
            def func(a: list[str]):
                return None

            func(["jared", 1])
