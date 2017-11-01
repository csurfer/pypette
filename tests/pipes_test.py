#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Unit tests pipes.py classes and methods.

Usage from git root:

    >>> python setup.py test
"""

import logging
import unittest

from pypette import BashJob, Job, Pipe

logging.basicConfig(level=logging.CRITICAL)


class PipeTest(unittest.TestCase):
    def test_validation(self):
        """Tests the validation of job list submitted to Pipe object."""
        def dummy():
            pass

        job = Job(dummy)
        bashjob = BashJob(['ls'])
        pipe = Pipe('dummy')

        try:
            # Validate job object list is valid list to submit.
            Pipe._validate([job])
            # Validate bash job object list is valid list to submit.
            Pipe._validate([bashjob])
            # Validate pipe object list is valid list to submit.
            Pipe._validate([pipe])
            # Validate lists including both are valid list to submit.
            Pipe._validate([job, bashjob, pipe])
        except AssertionError:
            self.fail("Submit validation raised AssertionError unexpectedly!")

        # Validate wrong types of input raise AssertionError.
        with self.assertRaises(AssertionError):
            Pipe._validate([1])
        with self.assertRaises(AssertionError):
            Pipe._validate(['test_string'])

    def test_basic_flow(self):
        """Validates the flow created due to submission of jobs to pipeline."""
        def dummy():
            pass

        j1 = Job(dummy)
        b1 = BashJob(['ls'])
        p = Pipe('test')

        # Validate a new pipe contains no jobs by default.
        self.assertEqual([], list(p.job_map.values()))

        # Validate empty job list does nothing but doesn't throw an error
        # either.
        p.add_jobs([])
        self.assertEqual([], list(p.job_map.values()))

        # Validate the structure of the jobs submittted.
        p.add_jobs([j1, b1])
        p.add_jobs([b1, j1])
        p.add_jobs([j1, b1], True)
        p.add_jobs([b1, j1], True)

        expected = [
            [j1],
            [b1],
            [b1],
            [j1],
            [j1, b1],
            [b1, j1]
        ]

        for (a, b) in zip(p.job_map.values(), expected):
            self.assertEqual(
                a,
                b,
                'Jobset in the current stage of pipeline is different')


if __name__ == '__main__':
    unittest.main()
