# -*- coding: utf-8 -*-

"""
Example script to create basic pipeline of the form.

    Pipe(p)
    |
    ---> print_job
    |
    ---> Pipe(p1)
         |
         ---> print_job
         |
         ---> Pipe(p2)
              |
              ---> print_job
              |
              ---> print_job
              |
              ---> print_job, print_job
"""

import threading
from time import sleep

from pypette import Job, Pipe


def print_job(message):
    """Sample method which takes a message to print."""
    print(threading.currentThread().getName(), 'Starting')
    sleep(1)
    print('From within print_job : ' + str(message))
    print(threading.currentThread().getName(), 'Ending')


# Create pipeline p2
p2 = Pipe('p2')
p2.add_jobs([
    Job(print_job, ('p2 1 series',)),
    Job(print_job, ('p2 2 series',)),
])
p2.add_jobs([
    Job(print_job, ('p2 3 parallel',)),
    Job(print_job, ('p2 4 parallel',)),
], run_in_parallel=True)

# Create pipeline p1
p1 = Pipe('p1')
p1.add_jobs([
    Job(print_job, ('p1 1 series',)),
    p2
])

# Create pipeline p
p = Pipe('p')
p.add_jobs([
    Job(print_job, ('top most',)),
    p1
])

# Display the structure of the pipeline to be run.
p.graph()

# Run the pipeline.
p.run()
