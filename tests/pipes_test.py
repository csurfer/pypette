#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Unit tests pipes.py classes and methods.

Usage from git root:

    >>> python setup.py test
"""

import unittest

from pypette import Job, Pipe


class PipeTest(unittest.TestCase):
    def test_validation(self):
        """Tests the validation of job list submitted to Pipe object."""
        def dummy():
            pass

        job = Job(dummy)
        pipe = Pipe('dummy')

        try:
            # Validate job object list is valid list to submit.
            Pipe._validate([job])
            # Validate pipe object list is valid list to submit.
            Pipe._validate([pipe])
            # Validate lists including both are valid list to submit.
            Pipe._validate([job, pipe])
        except AssertionError:
            self.fail("Submit validation raised AssertionError unexpectedly!")

        # Validate wrong types of input raise AssertionError.
        with self.assertRaises(AssertionError):
            Pipe._validate([1])
        with self.assertRaises(AssertionError):
            Pipe._validate(['test_string'])

    def test_basic_flow(self):
        """Validates the flow created due to submission of jobs to pipeline."""
        def dummy1():
            pass

        def dummy2():
            pass

        j1 = Job(dummy1)
        j2 = Job(dummy2)
        p = Pipe('test')

        # Validate a new pipe contains no jobs by default.
        self.assertEquals([], p.job_map.values())

        # Validate empty job list does nothing but doesn't throw an error
        # either.
        p.add_jobs([])
        self.assertEquals([], p.job_map.values())

        # Validate the structure of the jobs submittted.
        p.add_jobs([j1, j2])
        p.add_jobs([j2, j1])
        p.add_jobs([j1, j2], True)
        p.add_jobs([j2, j1], True)

        expected = [
            [j1],
            [j2],
            [j2],
            [j1],
            [j1, j2],
            [j2, j1]
        ]

        for (a, b) in zip(p.job_map.values(), expected):
            self.assertEqual(
                a,
                b,
                'Jobset in the current stage of pipeline is different')


if __name__ == '__main__':
    unittest.main()
