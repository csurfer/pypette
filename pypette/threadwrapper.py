# -*- coding: utf-8 -*-

"""
threadwrapper.api
~~~~~~~~~~~~~~~~~
Class definitions to create wrapper threads for jobs.
"""

import subprocess
from threading import Thread

from enum import Enum

from .jobs import BashJob, Job


class ThreadState(Enum):
    """State in which a thread can be in."""

    INIT = 1
    RUNNING = 2
    SUCCESS = 3
    FAILED = 4


class ThreadWrapper(Thread):
    """Wrapper around a thread to allow for exception handling."""

    def __init__(self, job):
        """Constructor.

        :param job: Job to run.
        :type: JobInterface or Pipe.
        """
        if isinstance(job, Job):
            super(ThreadWrapper, self).__init__(
                target=job.function, args=job.args, kwargs=job.kwargs
            )

        elif isinstance(job, BashJob):
            # Note that without lambda, subprocess.Popen runs immediately.
            super(ThreadWrapper, self).__init__(
                target=lambda: subprocess.Popen(job.cmd).wait()
            )

        else:
            super(ThreadWrapper, self).__init__(target=job.run)

        self._state = ThreadState.INIT
        self._exception = None

    def run(self):
        """Runs the thread in an exception free way."""
        try:
            self._state = ThreadState.RUNNING
            super(ThreadWrapper, self).run()
            self._state = ThreadState.SUCCESS
        except Exception as e:
            self._state = ThreadState.FAILED
            self._exception = e

    @property
    def state(self):
        """Thread's current state."""
        return self._state

    @property
    def exception(self):
        """Exception thrown by thread if any."""
        return self._exception
