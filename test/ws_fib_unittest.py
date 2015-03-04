#!/usr/bin/python
#
# author: Bo Yang
#

"""
main entry for unit test
"""

import fib_test
import unittest

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromModule(fib_test))
    unittest.TextTestRunner(verbosity=2).run(suite)
