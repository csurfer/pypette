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

    def test_create_thread_for(self):
        """Tests creation of threads for various jobs."""
        def dummy(msg):
            pass

        # Validate thread creation for python callable.
        t = Pipe._create_thread_for(Job(dummy, args=('a',)))
        self.assertEqual(
            t._Thread__target,
            dummy,
            'Thread target function is not as expected for Job')
        self.assertEqual(
            t._Thread__args,
            ('a',),
            'Thread arguments not as expected for Job')
        self.assertEqual(
            t._Thread__kwargs,
            {},
            'Thread kwargs not as expected for Job')

        # Validate thread creation for Pipe object.
        p = Pipe('test')
        t = Pipe._create_thread_for(p)
        self.assertEqual(
            t._Thread__target,
            p.run,
            'Thread target function is not as expected for Pipe')

        # Validate thread creation for bash job.
        t = Pipe._create_thread_for(BashJob(['ls']))
        self.assertEqual(
            t._Thread__target.__name__,
            '<lambda>',
            'Thread target function is not as expected for BashJob')


if __name__ == '__main__':
    unittest.main()
