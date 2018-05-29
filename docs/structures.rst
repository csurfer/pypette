Job
===

The basic unit of execution, say a python method or a callable.

for methods without arguments
------------------------------

.. code:: python

    from pypette import Job

    def method():
        print("Hello!")

    job = Job(method)

for methods with arguments
---------------------------

.. code:: python

    from pypette import Job

    def method(msg):
        print("Hello " + msg + "!")

    # As argument list
    job = Job(method, args=("World",))

    # As key word arguments
    job = Job(method, kwargs={"msg":"World"})

for lambda methods
------------------

.. code:: python

    from pypette import Job

    job = Job(lambda: print("Hello World!"))

BashJob
=======

The basic unit of execution, which runs a bash command.

.. code:: python

    from pypette import BashJob

    job = BashJob(['ls', '-l'])
    job = BashJob(['pwd'])
    job = BashJob(['cat', 'file.txt', '|', 'grep', 'colours'])

Pipe
====

Structure to specify the flow in which the jobs need to be executed.

Creation Modes
--------------

FAIL_FAST (Default)
~~~~~~~~~~~~~~~~~~~

Pipe objects created in this mode do not execute any stages to come after an
exception is thrown

.. code:: python

    from pypette import Pipe, Gate

    p = Pipe('Test')
    p = Pipe('Test', gate=Gate.FAIL_FAST)

EXECUTE_ALL
~~~~~~~~~~~

Pipe objects created in this mode continue to execute all stages to come after
an exception is thrown i,e these pipelines are resilient to exceptions.

.. code:: python

    from pypette import Pipe, Gate

    p = Pipe('Test', gate=Gate.EXECUTE_ALL)

Adding jobs to pipeline
-----------------------

Any object of the type :class:`BashJob <pypette.BashJob>`,
:class:`Job <pypette.Job>` or :class:`Pipe <pypette.Pipe>` can be added as a
job to the pipeline

in series
~~~~~~~~~

.. code:: python

    from pypette import Pipe

    p = Pipe('Test')

    # A list of jobs can be added in series as
    p.add_stage(job1)
    p.add_stage(job2)
    p.add_stage(job3)
    p.add_stage(job4)

    # Or as a job list
    p.add_jobs([job1, job2, job3, job4])

in parallel
~~~~~~~~~~~

.. code:: python

    from pypette import Pipe

    p = Pipe('Test')

    # A list of jobs can be added in series as
    p.add_stage(job1, job2, job3, job4)

    # Or as a job list
    p.add_jobs([job1, job2, job3, job4], run_in_parallel=True)

Adding dependencies to pipelines
--------------------------------

Irrespective of the mode the :class:`Pipe <pypette.Pipe>` object is created in,
we several times come across scenarios where we want to create dependencies i,e
we do not want a pipeline to run unless some other pipeline has succeeded. We
can add one :class:`Pipe <pypette.Pipe>` object as a dependency to another
:class:`Pipe <pypette.Pipe>` object as follows

.. code:: python

    from pypette import Pipe

    build = Pipe('Build')
    test = Pipe('Test')

    # Run test pipeline only if build has run and it was successful.
    test.add_dependency(build)

    cleanup = Pipe('Cleanup')
    # Run cleanup pipeline only if build and test have run and completed
    # successfully
    cleanup.add_dependency(build, test)

Visualizing the pipeline structure
----------------------------------

We can visualize the entire pipeline within the comfort of the terminal itself
using the `graph()` method

.. code:: python

    from pypette import Pipe

    test = Pipe('Test')
    ...
    test.graph()

Running the pipeline
--------------------

We can start executing the stages of the pipeline by using the `run()` method

.. code:: python

    from pypette import Pipe

    test = Pipe('Test')
    ...
    test.run()

Generating report for the pipeline run
--------------------------------------

Once the pipleline has been run, we can generate a report of the run using the
`report()` method

.. code:: python

    from pypette import Pipe

    test = Pipe('Test')
    ...
    test.report()

Building complex pipelines
==========================

Jobs submitted to pipeline should be callables i.e. structures which can be
run. This means python methods, lambdas etc qualify.

What about Pipe itself?

Of course, it is a callable and you can submit a pipe object to be run along
with regular jobs. This way you can build small pipelines which achieve a
specific task and then combine them to create more complex pipelines.

Let us understand building pipelines using these jobs

.. code:: python

    from pypette import Job

    def _good():
        print("I am good.")

    def _bad():
        raise Exception("I am bad.")

    def _ugly(): print("I"
        + "am"
            + "ugly.")

    def _dummy():
        pass

    good = Job(_good)
    bad = Job(_bad)
    ugly = Job(_ugly)
    dummy = Job(_dummy)

Exception scenarios
-------------------

Let us understand how a pipeline behaves in case of exception scenarios

Exception thrown in series
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from pypette import Pipe

    p = Pipe("Test") # Note is similar to Pipe("Test", gate=Gate.FAIL_FAST)

    p.add_stage(good)
    p.add_stage(bad)
    p.add_stage(ugly)

    p.run()

    # Executes good, bad and as bad throws exception, exits pipeline without
    # executing ugly.

Exception thrown in parallel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from pypette import Pipe

    p = Pipe("Test") # Note is similar to Pipe("Test", gate=Gate.FAIL_FAST)

    p.add_stage(good, bad)
    p.add_stage(ugly)

    p.run()

    # Executes both good and bad as they need to be executed in parallel and we
    # have no control over what goes before what. And as bad throws an exception
    # does not execute the next stage which has ugly.

Resilient mode
~~~~~~~~~~~~~~

.. code:: python

    from pypette import Gate, Pipe

    p = Pipe("Test", gate=Gate.EXECUTE_ALL)

    # For a pipe created in the following way, ugly would have been executed for
    # both scenarios of exception in series and parallel listed above. What this
    # means is that bad would have thrown an exception but that wouldn't have
    # stopped pipeline from executing stages after it.

Combining everything
--------------------

Combining all the scenarios listed above we can create a complex pipeline with
jobs and sub pipes etc as follows.

.. code:: python

    from pypette import Gate, Pipe

    jenkins = Pipe("Jenkins", gate=Gate.EXECUTE_ALL)

    build = Pipe("Build", gate=Gate.EXECUTE_ALL)
    build.add_stage(good)

    # Test pipeline will throw an exception.
    test = Pipe("Test", gate=Gate.EXECUTE_ALL)
    test.add_stage(bad)

    # Cleanup pipeline is dependent on both build and test pipeline success.
    cleanup = Pipe("Cleanup", gate=Gate.EXECUTE_ALL)
    cleanup.add_stage(ugly)
    cleanup.add_dependency(build, test)

    jenkins.add_stage(dummy, build)
    jenkins.add_stage(test, dummy)
    jenkins.add_stage(cleanup, dummy, dummy)

    jenkins.graph()

    # Would output a graph on the lines of
    #
    # Pipe(Jenkins)
    # |
    # |----------------------------
    # |            |              |
    # |          dummy        Pipe(Build)
    # |----------------------------
    # |            |              |
    # |          Pipe(Test)     dummy
    # |------------------------------------------
    #             |               |             |
    #           Pipe(Cleanup)   dummy         dummy
    #
    # Pipe(Build)
    # |
    # |----------- good
    #
    # Pipe(Test)
    # |
    # |------------ bad
    #
    # Pipe(Cleanup)
    # |
    # |------------ ugly

    jenkins.run()

    # Take a minute before reading the answer and make a mental note of what
    # all gets executed and why?
    #
    # Answer:
    # dummy job gets executed 4 times as EXECUTE_ALL is exception resilient.
    #
    # build pipeline gets successfully executed (implying all internal jobs get
    # executed successully)
    #
    # test pipeline fails (implying one or more jobs threw an exception. Note
    # that even though other jobs do get executed within this pipeline as it is
    # resilient, it still is marked as overall failure as one ore more jobs
    # threw an exception.)
    #
    # cleanup pipeline wont start executing as it is dependent on build and test
    # being successful and test pipe has failed.
    #
    # jenkins overall gets marked as failed as one or more jobs/sub pipes have
    # failed.

    jenkins.report()

    # Would provide a report on the lines of
    #
    # Pipe(Jenkins)
    # |
    # |----------------------------
    # |            |              |
    # |          SUCCESS        SUCCESS
    # |----------------------------
    # |            |              |
    # |          FAILED         SUCCESS
    # |------------------------------------------
    #             |               |             |
    #            FAILED         SUCCESS       SUCCESS
    #
    # Pipe(Build)
    # |
    # |----------- SUCCESS
    #
    # Pipe(Test)
    # |
    # |------------ FAILED
    #
    # Pipe(Cleanup)
    # |
    # |------------ FAILED
