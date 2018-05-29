#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Unit tests pipes.py classes and methods.

Usage from git root:

    >>> python setup.py test
"""

import logging
import unittest

from pypette import BashJob, Job, Pipe, ThreadState

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

    def test_add_jobs(self):
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

    def test_add_stages(self):
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
        p.add_stage()
        self.assertEqual([], list(p.job_map.values()))

        # Validate the structure of the jobs submittted.
        p.add_stage(j1)
        p.add_stage(b1)
        p.add_stage(b1)
        p.add_stage(j1)
        # Builder pattern
        p.add_stage(j1, b1).add_stage(b1, j1)

        expected = [[j1], [b1], [b1], [j1], [j1, b1], [b1, j1]]

        for (a, b) in zip(p.job_map.values(), expected):
            self.assertEqual(
                a, b, "Jobset in the current stage of pipeline is different"
            )

    def test_add_dependency(self):
        """Validates adding of dependencies to pipeline."""

        p = Pipe("test")

        p1 = Pipe("dependency1")
        p.add_dependency(p1)
        self.assertEqual([p1], p.dependent_on, "Dependency not as expected")

        p2 = Pipe("dependency2")
        p.add_dependency(p2)
        self.assertEqual(
            [p1, p2], p.dependent_on, "Dependency not as expected"
        )

        p3 = Pipe("dependency3")
        p4 = Pipe("dependency4")
        p.add_dependency(p3, p4)
        self.assertEqual(
            [p1, p2, p3, p4], p.dependent_on, "Dependency not as expected"
        )

    def test_dependency_check(self):
        """Validates dependency check of pipeline."""

        p = Pipe("test")

        p1 = Pipe("dependency1")
        p1.state = ThreadState.SUCCESS
        p2 = Pipe("dependency2")
        p2.state = ThreadState.SUCCESS
        p3 = Pipe("dependency3")
        p3.state = ThreadState.SUCCESS
        p4 = Pipe("dependency4")
        p4.state = ThreadState.SUCCESS

        p.add_dependency(p1, p2, p3, p4)
        self.assertTrue(
            p.dependency(), "Dependency check expected to be successful"
        )

        p3.state = ThreadState.FAILED
        self.assertFalse(
            p.dependency(), "Dependency check expected to be a failure"
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

    def test_report(self):
        """Validates report call on pipelines."""
        p = Pipe("test")

        # Validate run call on empty pipe.
        try:
            p.report()
        except Exception:
            self.fail("report() on empty pipe should not throw any exception")

        def dummy():
            pass

        p.add_jobs([Job(dummy), BashJob(["pwd"])])

        try:
            p.run()
            p.report()
        except Exception:
            self.fail("report() should not throw any exception")


if __name__ == "__main__":
    unittest.main()
