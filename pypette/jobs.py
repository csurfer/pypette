# -*- coding: utf-8 -*-

"""
jobs.api
~~~~~~~~
Class definitions to describe python method calls in a deterministic way.

Description: Method outputs are determined by the inputs provided to it, hence
to describe all aspects of the method call we need to know what method is being
called and what arguments it is called with. Classes in this file help to
describe python methods in a structured way.
"""

from inspect import isroutine


class JobInterface(object):
    """Pipeline job interface."""

    def __init__(self, name):
        """Constructor.

        :param name: Name of job.
        :type name: str
        """
        self.name = name


class Job(JobInterface):
    """Class to format python methods as pipeline jobs."""

    def __init__(self, function, args=(), kwargs={}):
        """Constructor.

        :param function: Python method to run.
        :type function: function
        :param args: Argument list to run the method with.
        :type args: tuple
        :param kwargs: Keyword arguments to run the method with.
        :type kwargs: dict
        """

        # Validate the structure of the job submitted.
        assert isroutine(function), 'Python callable expected'
        assert isinstance(args, tuple)
        assert isinstance(kwargs, dict)

        super(Job, self).__init__(function.__name__)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return 'Job(function={}, args={}, kwargs={})'.format(
            self.name,
            self.args,
            self.kwargs)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        # Note that same method run with two different sets of parameters is
        # considered to be two different jobs and not one job.
        return self.function == other.function and \
            self.args == other.args and \
            self.kwargs == other.kwargs


class BashJob(JobInterface):
    """Class to format bash commands as pipeline jobs."""

    def __init__(self, cmd):
        """Constructor.

        :param cmd: Bash command to run.
        :type cmd: list
        """

        # Validate the structure of the job submitted.
        assert isinstance(cmd, list), 'Bash command as list of strings needed'

        super(BashJob, self).__init__(' '.join(cmd))
        self.cmd = cmd

    def __repr__(self):
        return 'BashJob(cmd={})'.format(self.name)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.cmd == other.cmd
