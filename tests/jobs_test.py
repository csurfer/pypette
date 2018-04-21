#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Unit tests jobs.py classes and methods.

Usage from git root:

    >>> python setup.py test
"""

import unittest

from pypette import BashJob, Job


class JobTest(unittest.TestCase):
    """Unit tests Job class."""

    def test_default_args(self):
        """Validates the default arguments set for jobs."""

        def dummy():
            pass

        j = Job(dummy)

        self.assertEqual((), j.args, "args should be set to `()` by default")
        self.assertEqual(
            {}, j.kwargs, "kwargs should be set to `\{\}` by default"
        )

    def test_function_validation(self):
        """Tests the function validation mechanism."""
        with self.assertRaises(AssertionError):
            Job(1)
        with self.assertRaises(AssertionError):
            Job("test")

    def test_string_representation(self):
        """Tests printable representation of Jobs."""

        def dummy(msg):
            pass

        self.assertEqual(
            "Job(function=dummy, args=('a',), kwargs={'msg': 'a'})",
            Job(dummy, ("a",), {"msg": "a"}).__repr__(),
            "Job representation not as expected",
        )

        self.assertEqual(
            "Job(function=dummy, args=('a',), kwargs={'msg': 'a'})",
            Job(dummy, ("a",), {"msg": "a"}).__str__(),
            "Job representation not as expected",
        )

    def test_equality(self):
        """Validates equality of jobs."""

        def dummy(msg):
            pass

        def dummy1(msg):
            pass

        self.assertEqual(Job(dummy, args=("a",)), Job(dummy, args=("a",)))

        self.assertNotEqual(Job(dummy, args=("a",)), Job(dummy1, args=("a",)))

        self.assertNotEqual(Job(dummy, args=("a",)), Job(dummy, args=("b",)))

        self.assertEqual(
            Job(dummy, kwargs={"msg": "a"}), Job(dummy, kwargs={"msg": "a"})
        )

        self.assertNotEqual(
            Job(dummy, kwargs={"msg": "a"}), Job(dummy1, kwargs={"msg": "a"})
        )

        self.assertNotEqual(
            Job(dummy, kwargs={"msg": "a"}), Job(dummy, kwargs={"msg": "b"})
        )


class BashJobTest(unittest.TestCase):
    """Unit tests BashJob"""

    def test_function_validation(self):
        """Tests the function validation mechanism."""
        with self.assertRaises(AssertionError):
            Job(1)
        with self.assertRaises(AssertionError):
            Job("test")

    def test_string_representation(self):
        """Tests printable representation of BashJobs."""
        self.assertEqual(
            "BashJob(cmd=ls -l)",
            BashJob(["ls", "-l"]).__repr__(),
            "BashJob representation not as expected",
        )

        self.assertEqual(
            "BashJob(cmd=pwd)",
            BashJob(["pwd"]).__repr__(),
            "BashJob representation not as expected",
        )

    def test_equality(self):
        """Validates equality of bash jobs."""
        self.assertEqual(BashJob(["ls"]), BashJob(["ls"]))
        self.assertEqual(BashJob(["ls -l"]), BashJob(["ls -l"]))
        self.assertNotEqual(BashJob(["pwd"]), BashJob(["ls"]))


if __name__ == "__main__":
    unittest.main()
