#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Unit tests threadwrapper.py classes and methods.

Usage from git root:

    >>> python setup.py test
"""

from pypette import Job, ThreadState, ThreadWrapper


def test_safe_run() -> None:
    """Tests run() thread method can be called safely."""

    def dummy():
        pass

    def corrupt():
        raise Exception('Corrupt')

    tw = ThreadWrapper(Job(function=dummy))
    assert tw.state == ThreadState.INIT
    tw.run()
    assert tw.state == ThreadState.SUCCESS

    tw = ThreadWrapper(Job(function=corrupt))
    assert tw.state == ThreadState.INIT
    tw.run()
    assert tw.state == ThreadState.FAILED


def test_safe_start():
    """Tests start() thread method can be called safely."""

    def dummy():
        pass

    def corrupt():
        raise Exception('Corrupt')

    tw = ThreadWrapper(Job(function=dummy))
    assert tw.state == ThreadState.INIT
    tw.start()
    assert tw.state == ThreadState.SUCCESS

    tw = ThreadWrapper(Job(function=corrupt))
    assert tw.state == ThreadState.INIT
    tw.start()
    assert tw.state == ThreadState.FAILED
