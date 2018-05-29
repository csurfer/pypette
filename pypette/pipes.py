# -*- coding: utf-8 -*-

"""
pipes.api
~~~~~~~~~
Class definitions to create, validate and run jobs as pipelines.

Description:

`Job` is the basic unit of pipeline which does some work.
`Pipe` is a structure which helps run the above jobs one after the other or in
parallel. A pipe can be used to run jobs or other pipes.

Hence overtly complicated pipelines can be boiled down to the above two basic
blocks.
"""

import logging
from collections import OrderedDict
from functools import partial
from itertools import chain
from uuid import uuid4

import crayons
from enum import Enum

from .jobs import JobInterface
from .threadwrapper import ThreadState, ThreadWrapper


class Gate(Enum):
    """Different kinds of gating allowed for pipes."""

    def __fail_fast():
        return False

    # Fails at the first error or exception thrown from a job. (Default)
    FAIL_FAST = partial(__fail_fast)

    def __execute_all():
        return True

    # Silently captures the error or exception to execute all the jobs.
    EXECUTE_ALL = partial(__execute_all)


class Pipe(object):
    """Class to define the pipeline structure."""

    def __init__(self, name, gate=Gate.FAIL_FAST):
        """Constructor.

        :param name: Name given to the pipe object for identification.
        :type name: str
        """
        self.name = "Pipe({})".format(name)
        self.job_map = OrderedDict()
        self.thread_map = OrderedDict()
        self.gate = gate.value
        self.dependent_on = []

    def add_jobs(self, jobs, run_in_parallel=False):
        """Method to add jobs to pipeline.

        :param jobs: List of jobs/pipes to run.
        :type jobs: list
        :param run_in_parallel: This flag when set to False(default) runs the
                                list of jobs given one after another. This flag
                                if set to True runs the jobs/pipes submitted in
                                parallel threads.
        :type run_in_parallel: boolean
        """

        # Return if nothing to do.
        if not jobs:
            return

        # Validate the set of jobs given.
        Pipe._validate(jobs)

        # Add jobs to pipeline.
        if run_in_parallel:
            self._add_in_parallel(jobs)
        else:
            self._add_in_series(jobs)

        return self

    def add_stage(self, *args):
        """Method to add stages of pipeline. Jobs are to be given comma
        separated and all the jobs given form a single stage. Another way to
        add jobs to a pipeline in builder pattern.

        :param args: Jobs to be added. Adds comma separated list in parallel or
                     a single job as a stage.
        """

        # Return if nothing to do.
        if not args:
            return

        # Validate the set of jobs given.
        Pipe._validate(args)

        # Add jobs to pipeline.
        if len(args) > 1:
            self._add_in_parallel(list(args))
        else:
            self._add_in_series(args)

        return self

    def add_dependency(self, *args):
        """Method to add dependency of one pipe on another.

        :param args: Pipes to be added as dependency for this pipeline.
        """
        for job in args:
            if not isinstance(job, Pipe):
                logging.error("Dependecies should be of type Pipe")
                raise AssertionError(
                    "Invalid type {} submitted".format(type(job))
                )
        self.dependent_on.extend(args)

    def dependency(self):
        """Method to check for success of pipelines listed as dependency."""
        allowed = True
        for item in self.dependent_on:
            allowed = allowed and (item.state == ThreadState.SUCCESS)
        return allowed

    def run(self):
        """Method to run the pipeline."""
        logging.debug("run() method called on {}".format(self.name))

        logging.debug(
            "Dependency for {} is {}".format(self, self.dependent_on)
        )
        if not self.dependency():
            return

        broken = False
        prev = True
        for key, jobset in self.job_map.items():
            if not prev:
                break
            job_threads = []
            # Create job threads
            for job in jobset:
                job_threads.append(ThreadWrapper(job))
            # Start job threads
            for job in job_threads:
                job.start()
            # Job main thread to create flow
            for job in job_threads:
                job.join()
            self.thread_map[key] = tuple(job_threads)
            # Stage finished successfully.
            for job in job_threads:
                prev = prev and (job.state == ThreadState.SUCCESS)
                if not prev:
                    broken = True
                prev = prev or self.gate()

        if prev and not broken:
            self.state = ThreadState.SUCCESS
        else:
            self.state = ThreadState.FAILED

    def graph(self):
        """Method to print the structure of the pipeline."""
        logging.debug("graph() method called on {}".format(self.name))
        self._pretty_print()
        print("")

    @staticmethod
    def _cstate(tw):
        """Returns state in colour for pretty printing reports."""
        if isinstance(tw, ThreadWrapper):
            if tw.state == ThreadState.SUCCESS:
                return str(crayons.green(tw.state.name))
            elif tw.state == ThreadState.FAILED:
                return str(crayons.red(tw.state.name))
            else:
                return str(crayons.yellow(tw.state.name))
        else:
            if ThreadState.SUCCESS.name in tw:
                return str(crayons.green(tw))
            elif ThreadState.FAILED.name in tw:
                return str(crayons.red(tw))
            else:
                return str(crayons.yellow(tw))

    def report(self):
        """Method to pretty print the report."""
        print("")
        print(crayons.green(self.name, bold=True))

        if not self.thread_map:
            print(crayons.red("No jobs run in pipeline yet !"))
            return

        joblen = len(self.thread_map)
        for i, jobs in enumerate(self.thread_map.values()):
            print(crayons.blue(u"| "))
            if len(jobs) == 1:
                print(crayons.blue(u"\u21E8  ") + Pipe._cstate(jobs[0]))
            else:
                if i == joblen - 1:
                    pre = u"  "
                else:
                    pre = u"| "
                l1 = [u"-" * 10 for j in jobs]
                l1 = u"".join(l1)
                l1 = l1[:-1]
                print(crayons.blue(u"\u21E8 ") + crayons.blue(l1))
                fmt = u"{0:^{wid}}"
                l2 = [fmt.format(u"\u21E9", wid=12) for j in jobs]
                print(crayons.blue(pre) + crayons.blue(u"".join(l2)))
                l3 = [
                    Pipe._cstate(fmt.format(j.state.name, wid=12))
                    for j in jobs
                ]
                print(crayons.blue(pre) + u"".join(l3))

        pipes = filter(
            lambda x: isinstance(x.job, Pipe), chain(*self.thread_map.values())
        )

        for item in pipes:
            item.job.report()

    @staticmethod
    def _validate(jobs):
        """Method to validate the jobs submitted to pipeline.

        :param jobs: List of jobs submitted.
        :type jobs: list
        """
        for job in jobs:
            valid = isinstance(job, JobInterface) or isinstance(job, Pipe)
            if not valid:
                logging.error(
                    "Pipeline jobs should be of type Job, BashJob or Pipe"
                )
                raise AssertionError(
                    "Invalid type {} submitted".format(type(job))
                )

    def _add_in_parallel(self, jobs):
        """Method to add jobs to pipeline so that they run in parallel.

        :param jobs: List of jobs submitted.
        :type jobs: list
        """
        self.job_map[uuid4()] = jobs
        logging.debug("{} submitted to be run in parallel".format(jobs))

    def _add_in_series(self, jobs):
        """Method to add jobs to pipeline so that they run one after another,
        only after the previous job completes.

        :param jobs: List of jobs submitted.
        :type jobs: list
        """
        for job in jobs:
            self.job_map[uuid4()] = [job]
            logging.debug("{} submitted to be run in series".format(job))

    def _pretty_print(self):
        """Method to pretty print the pipeline."""
        print("")
        print(crayons.green(self.name, bold=True))

        if not self.job_map:
            print(crayons.red("No jobs added to the pipeline yet !"))
            return

        joblen = len(self.job_map)
        for i, jobs in enumerate(self.job_map.values()):
            print(crayons.blue(u"| "))
            if len(jobs) == 1:
                print(crayons.blue(u"\u21E8  ") + crayons.white(jobs[0].name))
            else:
                if i == joblen - 1:
                    pre = u"  "
                else:
                    pre = u"| "
                l1 = [u"-" * (len(j.name) + 2) for j in jobs]
                l1 = u"".join(l1)
                l1 = l1[: -len(jobs[-1].name) // 2 + 1]
                print(crayons.blue(u"\u21E8 ") + crayons.blue(l1))
                fmt = u"{0:^{wid}}"
                l2 = [fmt.format(u"\u21E9", wid=len(j.name) + 2) for j in jobs]
                print(crayons.blue(pre) + crayons.blue(u"".join(l2)))
                l3 = [fmt.format(j.name, wid=len(j.name) + 2) for j in jobs]
                print(crayons.blue(pre) + crayons.white(u"".join(l3)))

        pipes = filter(
            lambda x: isinstance(x, Pipe), chain(*self.job_map.values())
        )

        for item in pipes:
            item._pretty_print()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()
