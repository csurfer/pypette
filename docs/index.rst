.. pypette documentation master file, created by
   sphinx-quickstart on Tue May 29 10:41:36 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

|Logo|

|pypiv| |pyv| |Build| |Coverage| |Licence| |Thanks|

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

Quick Start
-----------

.. code:: python

    from pypette import BashJob, Job, Pipe

    def wish():
        print("Hello World!")

    wish_job = Job(wish)

    build_job = BashJob(["python", "setup.py", "build"])

    test_job = BashJob(["python", "setup.py", "test"])

    clean_job = BashJob(["rm", "*.pyc"])

    def goodbye(msg):
        print("Goodbye {}!".format(msg))

    goodbye_job = Job(goodbye, args=("World",))

    # Pipeline can be created using add_jobs
    p = Pipe("Pipeline")
    p.add_jobs([wish_job])
    p.add_jobs([build_job, test_job], run_in_parallel=True)
    p.add_jobs([clean_job])
    p.add_jobs([goodbye_job])

    # Or using add_stage
    p = Pipe("Pipeline")
    p.add_stage(wish_job)
    p.add_stage(build_job, test_job)
    p.add_stage(clean_job)
    p.add_stage(goodbye_job)

    # Can check how the pipeline looks like
    p.graph()

    # Can run the pipeline using
    p.run()

    # Can check on the success states of different stages of pipeline using
    p.report()

Example pipeline
~~~~~~~~~~~~~~~~

An example pipeline and its code are included in `examples`_ folder.

User Guide
----------

.. toctree::
   :maxdepth: 2

   structures

API Reference
-------------

If you are looking for information on a specific function, class or
method, this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api

Contributing
------------

Bug Reports and Feature Requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please use `issue tracker`_ for reporting bugs or feature requests.

Development
~~~~~~~~~~~

Pull requests are most welcome.


Buy the developer a cup of coffee!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you found the utility helpful you can buy me a cup of coffee using

|Donate|

.. |Logo| image:: https://i.imgur.com/MBu5x0h.png
   :width: 60%
   :target: https://pypi.python.org/pypi/pypette

.. |Donate| image:: https://www.paypalobjects.com/webstatic/en_US/i/btn/png/silver-pill-paypal-44px.png
   :target: https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=3BSBW7D45C4YN&lc=US&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donate_SM%2egif%3aNonHosted

.. |Thanks| image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
   :target: https://saythanks.io/to/csurfer

.. _issue tracker: https://github.com/csurfer/pypette/issues
.. _examples: https://github.com/csurfer/pypette/tree/master/examples

.. |Licence| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/csurfer/pypette/master/LICENSE

.. |Build| image:: https://travis-ci.org/csurfer/pypette.svg?branch=master
   :target: https://travis-ci.org/csurfer/pypette

.. |Coverage| image:: https://coveralls.io/repos/github/csurfer/pypette/badge.svg?branch=master
   :target: https://coveralls.io/github/csurfer/pypette?branch=master

.. |pypiv| image:: https://img.shields.io/pypi/v/pypette.svg
   :target: https://pypi.python.org/pypi/pypette

.. |pyv| image:: https://img.shields.io/pypi/pyversions/pypette.svg
   :target: https://pypi.python.org/pypi/pypette
