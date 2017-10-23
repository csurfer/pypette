# Example script to create basic pipeline.
#
# Pipe(p1)
# |
# ---> ppr('parent')
# |
# ---> Pipe(p)
#      |
#      ---> ppr('s1')
#      |
#      ---> ppo('s', '2')
#      |
#      ---> ppr('p1'), ppo('p, '2')

import threading
from time import sleep

from pipette import Job, Pipe


def ppr(x):
    print(threading.currentThread().getName(), 'Starting')
    sleep(1)
    print('From within ppr : ' + str(x))
    print(threading.currentThread().getName(), 'Ending')


def ppo(a, b):
    print(threading.currentThread().getName(), 'Starting')
    sleep(1)
    print('From within ppo : ' + str(a + b))
    print(threading.currentThread().getName(), 'Ending')


# Create pipeline p
p = Pipe('p')
p.add_jobs([
    Job(ppr, ('s1',)),
    Job(ppo, ('s', '2',))
])
p.add_jobs([
    Job(ppr, ('p1',)),
    Job(ppo, ('p', '2',))
], run_in_parallel=True)

# Create pipeline p1
p1 = Pipe('p1')
p1.add_jobs([
    Job(ppr, ('parent',)),
    p
])

# Display the structure of the pipeline to be run.
p1.graph()

# Run the pipeline.
p1.run()
