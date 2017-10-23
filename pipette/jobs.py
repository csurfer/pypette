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

from types import FunctionType


class Job(object):
    """Class to format python methods as pipeline jobs."""

    def __init__(self, function, args=(), kwargs={}):
        """Constructor.

        :param function: Python method to run.
        :param args: Argument list to run the method with.
        :param kwargs: Keyword arguments to run the method with.
        """

        # Validate the structure of the job submitted.
        assert isinstance(function, FunctionType), 'Python function expected'
        assert isinstance(args, tuple)
        assert isinstance(kwargs, dict)

        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.name = function.__name__
