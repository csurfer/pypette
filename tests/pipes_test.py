#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Unit tests pipes.py classes and methods.

Usage from git root:

    >>> python setup.py test
"""

import logging
import unittest
from threading import Thread

from pypette import BashJob, Job, Pipe

logging.basicConfig(level=logging.CRITICAL)


class PipeTest(unittest.TestCase):

    def test_validation(self):
        """Tests the validation of job list submitted to Pipe object."""

        def dummy():
            pass

        job = Job(dummy)
        bashjob = BashJob(["ls"])
        pipe = Pipe("dummy")

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
            Pipe._validate(["test_string"])

    def test_basic_flow(self):
        """Validates the flow created due to submission of jobs to pipeline."""

        def dummy():
            pass

        j1 = Job(dummy)
        b1 = BashJob(["ls"])
        p = Pipe("test")

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

        expected = [[j1], [b1], [b1], [j1], [j1, b1], [b1, j1]]

        for (a, b) in zip(p.job_map.values(), expected):
            self.assertEqual(
                a, b, "Jobset in the current stage of pipeline is different"
            )

    def test_create_thread_for(self):
        """Tests creation of threads for various jobs."""

        # Validate thread creation for python callable.

        def dummy(msg):
            pass

        t = Pipe._create_thread_for(Job(dummy, args=("a",)))
        self.assertEqual(
            type(t), Thread, "Thread for Job created successfully"
        )

        # Validate thread creation for Pipe object.
        p = Pipe("test")
        t = Pipe._create_thread_for(p)
        self.assertEqual(
            type(t), Thread, "Thread for Pipe created successfully"
        )

        # Validate thread creation for bash job.
        t = Pipe._create_thread_for(BashJob(["ls"]))
        self.assertEqual(
            type(t), Thread, "Thread for BashJob created successfully"
        )

    def test_representative_name(self):
        """Validates the name for pipeline."""
        p = Pipe("test")
        self.assertEqual(
            "Pipe(test)", p.__repr__(), "Pipe name not as expected"
        )
        self.assertEqual(
            "Pipe(test)", p.__str__(), "Pipe name not as expected"
        )

    def test_graph(self):
        """Validates graph call on pipelines."""
        p = Pipe("test")

        # Validate graph call on empty pipe.
        try:
            p.graph()
        except Exception:
            self.fail("graph() on empty pipe should not throw any exception")

        # Validate graph on a pipe with jobs.

        def dummy():
            pass

        def dummy1():
            pass

        p1 = Pipe("test1")
        p1.add_jobs([Job(dummy)])
        p1.add_jobs([Job(dummy), Job(dummy1)], run_in_parallel=True)
        p.add_jobs([p1])
        p.add_jobs([Job(dummy), Job(dummy1)], run_in_parallel=True)
        p.add_jobs([BashJob(["ls"])])

        try:
            p.graph()
        except Exception:
            self.fail("graph() should not throw any exception")

    def test_run(self):
        """Validates run call on pipelines."""
        p = Pipe("test")

        # Validate run call on empty pipe.
        try:
            p.run()
        except Exception:
            self.fail("run() on empty pipe should not throw any exception")

        def dummy():
            pass

        p.add_jobs([Job(dummy), BashJob(["pwd"])])

        try:
            p.run()
        except Exception:
            self.fail("run() should not throw any exception")


if __name__ == "__main__":
    unittest.main()
