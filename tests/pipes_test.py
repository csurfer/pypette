#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Unit tests pipes.py classes and methods.

Usage from git root:

    >>> python setup.py test
"""

import logging

import pytest

from pypette import BashJob, Job, Pipe, ThreadState

logging.basicConfig(level=logging.CRITICAL)


def test_validation() -> None:
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
        pytest.fail('Submit validation raised AssertionError unexpectedly!')

    # Validate wrong types of input raise AssertionError.
    with pytest.raises(AssertionError):
        Pipe._validate([1])
    with pytest.raises(AssertionError):
        Pipe._validate(['test_string'])


def test_add_jobs() -> None:
    """Validates the flow created due to submission of jobs to pipeline."""

    def dummy():
        pass

    j1 = Job(dummy)
    b1 = BashJob(['ls'])
    p = Pipe('test')

    # Validate a new pipe contains no jobs by default.
    assert [] == list(p.job_map.values())

    # Validate empty job list does nothing but doesn't throw an error
    # either.
    p.add_jobs([])
    assert [] == list(p.job_map.values())

    # Validate the structure of the jobs submittted.
    p.add_jobs([j1, b1])
    p.add_jobs([b1, j1])
    p.add_jobs([j1, b1], True)
    p.add_jobs([b1, j1], True)

    expected = [[j1], [b1], [b1], [j1], [j1, b1], [b1, j1]]

    for (a, b) in zip(p.job_map.values(), expected):
        assert a == b


def test_add_stages() -> None:
    """Validates the flow created due to submission of jobs to pipeline."""

    def dummy():
        pass

    j1 = Job(dummy)
    b1 = BashJob(['ls'])
    p = Pipe('test')

    # Validate a new pipe contains no jobs by default.
    assert [] == list(p.job_map.values())

    # Validate empty job list does nothing but doesn't throw an error
    # either.
    p.add_stage()
    assert [] == list(p.job_map.values())

    # Validate the structure of the jobs submittted.
    p.add_stage(j1)
    p.add_stage(b1)
    p.add_stage(b1)
    p.add_stage(j1)
    # Builder pattern
    p.add_stage(j1, b1).add_stage(b1, j1)

    expected = [[j1], [b1], [b1], [j1], [j1, b1], [b1, j1]]

    for (a, b) in zip(p.job_map.values(), expected):
        assert a == b


def test_add_dependency() -> None:
    """Validates adding of dependencies to pipeline."""

    p = Pipe('test')

    p1 = Pipe('dependency1')
    p.add_dependency(p1)
    assert [p1] == p.dependent_on

    p2 = Pipe('dependency2')
    p.add_dependency(p2)
    assert [p1, p2] == p.dependent_on

    p3 = Pipe('dependency3')
    p4 = Pipe('dependency4')
    p.add_dependency(p3, p4)
    assert [p1, p2, p3, p4] == p.dependent_on


def test_dependency_check() -> None:
    """Validates dependency check of pipeline."""

    p = Pipe('test')

    p1 = Pipe('dependency1')
    p1.state = ThreadState.SUCCESS
    p2 = Pipe('dependency2')
    p2.state = ThreadState.SUCCESS
    p3 = Pipe('dependency3')
    p3.state = ThreadState.SUCCESS
    p4 = Pipe('dependency4')
    p4.state = ThreadState.SUCCESS

    p.add_dependency(p1, p2, p3, p4)
    assert p.dependency() is True

    p3.state = ThreadState.FAILED
    assert p.dependency() is False


def test_representative_name() -> None:
    """Validates the name for pipeline."""
    p = Pipe('test')
    assert 'Pipe(test)' == p.__repr__()
    assert 'Pipe(test)' == p.__str__()


def test_graph() -> None:
    """Validates graph call on pipelines."""
    p = Pipe('test')

    # Validate graph call on empty pipe.
    try:
        p.graph()
    except Exception:
        pytest.fail('graph() on empty pipe should not throw any exception')

    # Validate graph on a pipe with jobs.

    def dummy():
        pass

    def dummy1():
        pass

    p1 = Pipe('test1')
    p1.add_jobs([Job(dummy)])
    p1.add_jobs([Job(dummy), Job(dummy1)], run_in_parallel=True)
    p.add_jobs([p1])
    p.add_jobs([Job(dummy), Job(dummy1)], run_in_parallel=True)
    p.add_jobs([BashJob(['ls'])])

    try:
        p.graph()
    except Exception:
        pytest.fail('graph() should not throw any exception')


def test_run() -> None:
    """Validates run call on pipelines."""
    p = Pipe('test')

    # Validate run call on empty pipe.
    try:
        p.run()
    except Exception:
        pytest.fail('run() on empty pipe should not throw any exception')

    def dummy():
        pass

    p.add_jobs([Job(dummy), BashJob(['pwd'])])

    try:
        p.run()
    except Exception:
        pytest.fail('run() should not throw any exception')


def test_report() -> None:
    """Validates report call on pipelines."""
    p = Pipe('test')

    # Validate run call on empty pipe.
    try:
        p.report()
    except Exception:
        pytest.fail('report() on empty pipe should not throw any exception')

    def dummy():
        pass

    p.add_jobs([Job(dummy), BashJob(['pwd'])])

    try:
        p.run()
        p.report()
    except Exception:
        pytest.fail('report() should not throw any exception')
