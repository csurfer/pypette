# -*- coding: utf-8 -*-

"""
Example script to create basic pipeline of the form.

  Pipe(p)
  |
  ⇨  print_job
  |
  ⇨  Pipe(p1)
  |   |
  |   ⇨  print_job
  |   |
  |   ⇨ ------------------
  |          ⇩         ⇩
  |      print_job  Pipe(p2)
  |                 |
  |                 ⇨  print_corrupt
  |                 |
  |                 ⇨  print_job
  |                 |
  |                 ⇨ ------------------
  |                 |      ⇩          ⇩
  |                 |  print_job  print_job
  |                 |
  |                 ⇨  print_job
  |
  ⇨  ls -l
  |
  ⇨  pwd
  |
  ⇨  Pipe(p3) <- Dependent on Pipe(p1)
      |
      ⇨  ls
"""

__author__ = 'Vishwas B Sharma'
__author_email__ = 'sharma.vishwas88@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 Vishwas B Sharma'

import threading
from time import sleep

from pypette import BashJob, Job, Pipe


def print_job(message: str) -> None:
    """Sample method which takes a message to print."""
    print(threading.currentThread().getName(), 'Starting')
    sleep(1)
    print('From within print_job : ' + str(message))
    print(threading.currentThread().getName(), 'Ending')


def print_corrupt(message: str) -> None:
    print(threading.currentThread().getName(), 'Starting')
    sleep(1)
    print('From within print_corrupt : ' + str(message))
    print(threading.currentThread().getName(), 'Ending')
    raise Exception('lal')


# Create pipeline p2
p2 = Pipe('p2')
p2.add_jobs([Job(print_corrupt, ('p2 1',)), Job(print_job, ('p2 2',))])
p2.add_jobs(
    [Job(print_job, ('p2 3.1',)), Job(print_job, ('p2 3.2',))],
    run_in_parallel=True,
)
p2.add_jobs([Job(print_job, ('p2 4',))])

# Create pipeline p1
p1 = Pipe('p1')
p1.add_jobs([Job(print_job, ('p1 1',))])
p1.add_jobs([Job(print_job, ('p1 2.1',)), p2], run_in_parallel=True)

# Create pipeline p
# When created as Pipe("p") or Pipe("p", Gate.FAIL_FAST) the pipeline exits the
# execution in the first stage where it encounters exception.
#
# When created as Pipe("p", Gate.EXECUTE_ALL) the pipeline is forgiving of
# exceptions and continues to execute all jobs even if an exception is thrwon
# in a stage.
#
# Note that when an external dependency is added to the Pipeline, as showin in
# line 93, the pipeline is not executed unless all of the pipelines are
# mentioned as dependencies are successfully executed.

# Create pipeline p3
p3 = Pipe('p3')
p3.add_jobs([BashJob(['ls'])])
p3.add_dependency(p1, p2)

p = Pipe('p')
p.add_jobs([Job(print_job, ('p 1',)), p1, BashJob(['ls', '-l']), BashJob(['pwd']), p3])

# Display the structure of the pipeline to be run.
p.graph()

# Run the pipeline.
p.run()

# Report of pipeline.
p.report()
