|Logo|

|pypiv| |pyv| |Build| |Licence|

--------------

pypette (to be read as pipette) is a module which makes building pipelines
ridiculously simple, allowing users to control the flow with minimal
instructions.

Features
--------

* Ridiculously simple interface.
* Ability to view pipeline structure within the comfort of a terminal.
* Run pipeline in exception resilient way if needed.
* Create dependencies on pipelines easily.
* Generate a easy to view/understand report within the comfort of a terminal.

Setup
-----

Using pip
~~~~~~~~~

.. code:: bash

    pip install pypette

Directly from the repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    git clone https://github.com/csurfer/pypette.git
    python pypette/setup.py install

Documentation
--------------

Detailed documentation can be found at https://csurfer.github.io/pypette

Structures
----------

Job
~~~

The basic unit of execution, say a python method or a callable.

.. code:: python

    from pypette import Job

    def print_hello():
        print("Hello!")

    def print_hello_msg(msg):
        print("Hello " + msg + "!")

    # Job without arguments
    j1 = Job(print_hello)

    # Job with arguments specified as argument list
    j2 = Job(print_hello_msg, args=("pypette is simple",))

    # Job with arguments specified as key word arguments
    j3 = Job(print_hello_msg, kwargs={"msg":"pypette is simple"})

BashJob
~~~~~~~

The basic unit of execution, which runs a bash command.

.. code:: python

    from pypette import BashJob

    # Job with bash commands
    b1 = BashJob(['ls', '-l'])
    b2 = BashJob(['pwd'])

Pipe
~~~~

Structure to specify the flow in which the jobs need to be executed. The whole
interface consists of only 4 methods.

.. code:: python

    from pypette import Pipe

    # 1. Create a new Pipe
    p = Pipe('TestPipe')

    # 2. Add jobs to execute. (Assuming job_list is a list of python/bash jobs)

    # To run the jobs in job_list in order one after the other where each job
    # waits for the job before it to finish.
    p.add_jobs(job_list)

    # To run the jobs in job_list parallelly and run the next step only after
    # all jobs in job list finish.
    p.add_jobs(job_list, run_in_parallel=True)

    # Add jobs in a builder format.
    p.add_stage(job1).add_stage(job2) # To add jobs in series.
    p.add_stage(job1, job2) # To add jobs in parallel.

Building complex pipelines
~~~~~~~~~~~~~~~~~~~~~~~~~~

Jobs submitted to pipeline should be callables i.e. structures which can be
run. This means python methods, lambdas etc qualify.

What about Pipe itself?

Of course, it is a callable and you can submit a pipe object to be run along
with regular jobs. This way you can build small pipelines which achieve a
specific task and then combine them to create more complex pipelines.

.. code:: python

    from pypette import BashJob, Job, Pipe

    def welcome():
        print("Welcome user!")

    def havefun():
        print("Have fun!")

    def goodbye():
        print("Goodbye!")

    # Build a simple pipeline
    p1 = Pipe('Fun')
    p1.add_jobs([
        Job(havefun),
    ])

    # Include simple pipeline into a complicated pipeline
    p2 = Pipe('Overall')
    p2.add_jobs([
        Job(welcome),
        p1,
        Job(goodbye),
        BashJob(['ls', '-l']),
        BashJob(['pwd'])
    ])

    p2.run() # This first runs welcome, then runs p1 pipeline then runs goodbye.

Example pipeline
~~~~~~~~~~~~~~~~

An example pipeline and its code are included in `examples`_ folder.

Visualizing the pipeline using graph()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pipeline objects have a method called ``graph()`` which helps visualize the
pipeline within the comfort of your terminal. The graph is recursive in nature
and it visualizes everything that will be run if we call ``run()`` on the pipe
object.

Visualizing the top-level pipeline in `examples/basic.py`_ led to the
following visualization.

|Viz|

Running the entire pipeline.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The only thing you need to do at this point to run the entire pipeline is to
call ``run()`` on your pipeline object.

Reporting the entire pipeline.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The only thing you need to do at this point to get the report of entire
pipeline is to call `report()` on your pipeline object.

Contributing
------------

Bug Reports and Feature Requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please use `issue tracker`_ for reporting bugs or feature requests.

Development
~~~~~~~~~~~

Pull requests are most welcome. Kindly follow the steps suggested below:

1. Checkout the repository.
2. Make your changes and add/update relavent tests.
3. Install **`poetry`** using **`pip install poetry`**.
4. Run **`poetry install`** to create project's virtual environment.
5. Run tests using **`poetry run tox`** (Any python versions which you don't have checked out will fail this). Fix failing tests and repeat.
6. Make documentation changes that are relavant.
7. Install **`pre-commit`** using **`pip install pre-commit`** and run **`pre-commit run --all-files`** to do lint checks.
8. Generate documentation using **`poetry run sphinx-build -b html docs/ docs/_build/html`**.
9. Generate **`requirements.txt`** for automated testing using **`poetry export --dev --without-hashes -f requirements.txt > requirements.txt`**.
10. Commit the changes and raise a pull request.


Buy the developer a cup of coffee!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you found the utility helpful you can buy me a cup of coffee using

|Donate|

.. |Logo| image:: https://i.imgur.com/MBu5x0h.png
   :width: 60%
   :target: https://pypi.python.org/pypi/pypette

.. |Donate| image:: https://www.paypalobjects.com/webstatic/en_US/i/btn/png/silver-pill-paypal-44px.png
   :target: https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=3BSBW7D45C4YN&lc=US&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donate_SM%2egif%3aNonHosted

.. _issue tracker: https://github.com/csurfer/pypette/issues
.. _examples/basic.py: https://github.com/csurfer/pypette/tree/master/examples/basic.py
.. _examples: https://github.com/csurfer/pypette/tree/master/examples

.. |Viz| image:: https://i.imgur.com/1PaPlD3.png
   :width: 200px

.. |Licence| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/csurfer/pypette/master/LICENSE

.. |Build| image:: https://github.com/csurfer/pypette/actions/workflows/pytest.yml/badge.svg?branch=master
   :target: https://github.com/csurfer/pypette/actions/workflows/pytest.yml/badge.svg?branch=master

.. |pypiv| image:: https://img.shields.io/pypi/v/pypette.svg
   :target: https://pypi.python.org/pypi/pypette

.. |pyv| image:: https://img.shields.io/pypi/pyversions/pypette.svg
   :target: https://pypi.python.org/pypi/pypette
