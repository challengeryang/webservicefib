#!/usr/bin/python
#
# author: Bo Yang
#

"""
Unit test cases for fib.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), "../"))
import unittest
import fib

class FibTest(unittest.TestCase):
    """ Class to do unittest for functions in fib """

    def test_fib(self):
        """ to test function fib """
        expected_vals = [0, 1, 1, 2, 3, 5, 8]
        for idx, val in enumerate(fib.fib()):
            self.assertEqual(val, expected_vals[idx])
            if idx == len(expected_vals)-1:
                break

    def test__fib_sequence(self):
        """ to test function _fib_sequence """
        self.assertEqual(fib._fib_sequence(0), ' ')
        self.assertEqual(fib._fib_sequence(1), '0')
        self.assertEqual(fib._fib_sequence(2), '0 1')
        self.assertEqual(fib._fib_sequence(3), '0 1 1')
        self.assertEqual(fib._fib_sequence(4), '0 1 1 2')
        self.assertEqual(fib._fib_sequence(5), '0 1 1 2 3')
        # can add more

    def test_fib_sequence_wapper(self):
        """ to test function fib_sequence_wapper """
        self.assertEqual(fib.fib_sequence_wapper(-1), fib.HELP_MESSAGE)
        self.assertEqual(fib.fib_sequence_wapper(0), ' ')
        self.assertEqual(fib.fib_sequence_wapper(1), '0')
        self.assertEqual(fib.fib_sequence_wapper('1'), '0')
        self.assertEqual(fib.fib_sequence_wapper(2), '0 1')
        self.assertEqual(fib.fib_sequence_wapper(3), '0 1 1')
        self.assertEqual(fib.fib_sequence_wapper(1.1), fib.HELP_MESSAGE)
        self.assertEqual(fib.fib_sequence_wapper('a'), fib.HELP_MESSAGE)
        self.assertEqual(fib.fib_sequence_wapper([1, 2]), fib.HELP_MESSAGE)
        self.assertEqual(fib.fib_sequence_wapper({1:'a'}), fib.HELP_MESSAGE)
        self.assertEqual(fib.fib_sequence_wapper(''), fib.HELP_MESSAGE)
        self.assertEqual(fib.fib_sequence_wapper(None), fib.HELP_MESSAGE)
        # can add more
