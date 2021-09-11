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
from typing import Any, Callable, Dict, List, Tuple, Union


class JobInterface:
    """Pipeline job interface."""

    def __init__(self, name: str) -> None:
        """Constructor.

        :param name: Name of the job.
        """
        self.name: str = name

    def __eq__(self, other: Any) -> bool:
        raise Exception

    def __repr__(self) -> str:
        raise Exception

    def __str__(self) -> str:
        return self.__repr__()


class Job(JobInterface):
    """Class to format python methods as pipeline jobs."""

    def __init__(
        self,
        function: Callable[..., Any],
        args: Union[Tuple, Tuple[Any]] = (),
        kwargs: Union[Dict, Dict[Any, Any]] = {},
    ) -> None:
        """Constructor.

        :param function: Python method to run.
        :param args: Argument list to run the method with.
        :param kwargs: Keyword arguments to run the method with.
        """
        assert isroutine(function), 'Python callable expected'
        assert isinstance(args, tuple)
        assert isinstance(kwargs, dict)

        super(Job, self).__init__(function.__name__)
        self.function: Callable[..., Any] = function
        self.args: Union[Tuple, Tuple[Any]] = args
        self.kwargs: Union[Dict, Dict[Any, Any]] = kwargs

    def __eq__(self, other: Any) -> bool:
        # Note that same method run with two different sets of parameters is
        # considered to be two different jobs and not one job.
        return (
            type(self) == type(other)
            and self.function == other.function
            and self.args == other.args
            and self.kwargs == other.kwargs
        )

    def __repr__(self) -> str:
        return 'Job(function={}, args={}, kwargs={})'.format(self.name, self.args, self.kwargs)


class BashJob(JobInterface):
    """Class to format bash commands as pipeline jobs."""

    def __init__(self, cmd: List[str]):
        """Constructor.

        :param cmd: Bash command to run.
        """
        assert isinstance(cmd, list), 'Bash command as list of strings needed'

        super(BashJob, self).__init__(' '.join(cmd))
        self.cmd: List[str] = cmd

    def __eq__(self, other: Any) -> bool:
        return type(self) == type(other) and self.cmd == other.cmd

    def __repr__(self) -> str:
        return 'BashJob(cmd={})'.format(self.name)
