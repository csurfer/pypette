#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Unit tests threadwrapper.py classes and methods.

Usage from git root:

    >>> python setup.py test
"""

import unittest

from pypette import Job, ThreadState, ThreadWrapper


class ThreadWrapperTest(unittest.TestCase):
    """Unit tests ThreadWrapper class."""

    def test_safe_run(self):
        """Tests run() thread method can be called safely."""

        def dummy():
            pass

        def corrupt():
            raise Exception("Corrupt")

        tw = ThreadWrapper(Job(function=dummy))
        self.assertEqual(tw.state, ThreadState.INIT)
        tw.run()
        self.assertEqual(tw.state, ThreadState.SUCCESS)

        tw = ThreadWrapper(Job(function=corrupt))
        self.assertEqual(tw.state, ThreadState.INIT)
        tw.run()
        self.assertEqual(tw.state, ThreadState.FAILED)

    def test_safe_start(self):
        """Tests start() thread method can be called safely."""

        def dummy():
            pass

        def corrupt():
            raise Exception("Corrupt")

        tw = ThreadWrapper(Job(function=dummy))
        self.assertEqual(tw.state, ThreadState.INIT)
        tw.start()
        self.assertEqual(tw.state, ThreadState.SUCCESS)

        tw = ThreadWrapper(Job(function=corrupt))
        self.assertEqual(tw.state, ThreadState.INIT)
        tw.start()
        self.assertEqual(tw.state, ThreadState.FAILED)
