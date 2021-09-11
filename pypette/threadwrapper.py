# -*- coding: utf-8 -*-

"""
threadwrapper.api
~~~~~~~~~~~~~~~~~
Class definitions to create wrapper threads for jobs.
"""

import subprocess
from enum import Enum
from threading import Thread
from typing import Any, Optional

from .jobs import BashJob, Job


class ThreadState(Enum):
    """State in which a thread can be in."""

    FAILED = 1
    INIT = 2
    RUNNING = 3
    SUCCESS = 4


class JobTypes(Enum):
    """Different types of jobs to process"""

    BASHJOB = 1
    JOB = 2
    PIPE = 3


class ThreadWrapper(Thread):
    """Wrapper around a thread to allow for exception handling and safe
    job execution."""

    def __init__(self, job: Any) -> None:
        """Constructor.

        :param job: Job to run.
        """
        self._job: Any = job
        if isinstance(job, Job):
            self._jobtype = JobTypes.JOB
            super(ThreadWrapper, self).__init__(target=job.function, args=job.args, kwargs=job.kwargs)

        elif isinstance(job, BashJob):
            # Note that without lambda, subprocess.Popen runs immediately.
            self._jobtype = JobTypes.BASHJOB
            super(ThreadWrapper, self).__init__(target=lambda: subprocess.Popen(job.cmd).wait())

        else:
            self._jobtype = JobTypes.PIPE
            super(ThreadWrapper, self).__init__(target=job.run)

        self._state = ThreadState.INIT
        self._exception: Optional[Exception] = None

    def run(self) -> None:
        """Runs the thread in an exception free way."""
        try:
            self._state = ThreadState.RUNNING
            super(ThreadWrapper, self).run()
            if self._jobtype == JobTypes.PIPE:
                self._state = self._job.state
            else:
                self._state = ThreadState.SUCCESS
        except Exception as e:
            self._state = ThreadState.FAILED
            self._exception = e

    @property
    def job(self) -> Any:
        """Job being run by the thread."""
        return self._job

    @property
    def state(self) -> ThreadState:
        """Thread's current state."""
        return self._state

    @property
    def exception(self) -> Optional[Exception]:
        """Exception thrown by thread if any."""
        return self._exception
