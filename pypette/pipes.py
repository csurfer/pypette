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
import subprocess
from collections import OrderedDict
from itertools import chain
from threading import Thread
from uuid import uuid4

import crayons

from .jobs import BashJob, Job, JobInterface


class Pipe(object):
    """Class to define the pipeline structure."""

    def __init__(self, name):
        """Constructor.

        :param name: Name given to the pipe object for identification.
        :type name: str
        """
        self.name = 'Pipe({})'.format(name)
        self.job_map = OrderedDict()

    def add_jobs(self, jobs, run_in_parallel=False):
        """Method to add jobs to pipeline.

        :param jobs: List of jobs/pipes to run.
        :type jobs: list
        :param run_in_parallel: This flag when set to False(default) runs the
        list of jobs given one after another. This flag if set to True runs the
        jobs/pipes submitted in parallel threads.
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

    def run(self):
        """Method to run the pipeline."""
        logging.debug('run() method called on {}'.format(self.name))
        for jobset in self.job_map.values():
            job_threads = []
            # Create job threads
            for job in jobset:
                job_threads.append(Pipe._create_thread_for(job))
            # Start job threads
            for job in job_threads:
                job.start()
            # Job main thread to create flow
            for job in job_threads:
                job.join()

    def graph(self):
        """Method to print the structure of the pipeline."""
        logging.debug('graph() method called on {}'.format(self.name))
        self._pretty_print()
        print('')

    @staticmethod
    def _create_thread_for(job):
        """Method to create thread to run the job in.

        :param job: Pipeline job to run.
        :type job: Job or BashJob or Pipe
        """
        if isinstance(job, Job):
            return Thread(
                target=job.function,
                args=job.args,
                kwargs=job.kwargs)
        elif isinstance(job, BashJob):
            # Note that without lambda, subprocess.Popen runs immediately.
            return Thread(target=lambda: subprocess.Popen(job.cmd).wait())
        else:
            return Thread(target=job.run)

    @staticmethod
    def _validate(jobs):
        """Method to validate the jobs submitted to pipeline.

        :param jobs: List of jobs submitted.
        :type jobs: list
        """
        for job in jobs:
            valid = isinstance(job, JobInterface) or isinstance(job, Pipe)
            if not valid:
                logging.error('Pipeline jobs should be of type Job or' +
                              ' BashJob or Pipe')
                raise AssertionError(
                    'Invalid type {} submitted'.format(type(job)))

    def _add_in_parallel(self, jobs):
        """Method to add jobs to pipeline so that they run in parallel.

        :param jobs: List of jobs submitted.
        :type jobs: list
        """
        self.job_map[uuid4()] = jobs
        logging.debug('{} submitted to be run in parallel'.format(jobs))

    def _add_in_series(self, jobs):
        """Method to add jobs to pipeline so that they run one after another,
        only after the previous job completes.

        :param jobs: List of jobs submitted.
        :type jobs: list
        """
        for job in jobs:
            self.job_map[uuid4()] = [job]
            logging.debug('{} submitted to be run in series'.format(job))

    def _pretty_print(self):
        """Method to pretty print the pipeline."""
        print('')
        print(crayons.green(self.name, bold=True))

        if not self.job_map:
            print(crayons.red('No jobs added to the pipeline yet !'))
            return

        joblen = len(self.job_map)
        for i, jobs in enumerate(self.job_map.values()):
            print(crayons.blue(u'| '))
            if len(jobs) == 1:
                print(crayons.blue(u'\u21E8  ') + crayons.white(jobs[0].name))
            else:
                if i == joblen - 1:
                    pre = u'  '
                else:
                    pre = u'| '
                l1 = [u'-' * (len(j.name) + 2) for j in jobs]
                l1 = u''.join(l1)
                l1 = l1[:-len(jobs[-1].name) // 2 + 1]
                print(crayons.blue(u'\u21E8 ') + crayons.blue(l1))
                fmt = u'{0:^{wid}}'
                l2 = [fmt.format(u'\u21E9', wid=len(j.name) + 2) for j in jobs]
                print(crayons.blue(pre) + crayons.blue(u''.join(l2)))
                l3 = [fmt.format(j.name, wid=len(j.name) + 2) for j in jobs]
                print(crayons.blue(pre) + crayons.white(u''.join(l3)))

        pipes = filter(lambda x: isinstance(x, Pipe),
                       chain(*self.job_map.values()))

        for item in pipes:
            item._pretty_print()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()
