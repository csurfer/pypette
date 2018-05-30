Release History
---------------

v0.0.9 (2018-05-30)
-------------------

**Improvement**

* Extending Pipe to handle and capture exceptions gracefully.
* Extending Pipe to have modes:
    * FAIL_FAST : Where an exception stops the execution of further stages.
    * EXECUTE_ALL : Where an exception doesn't stop the execution of further
      stages.
* Adding ability to specify dependency on other pipelines.
* Adding ability of reporting.

v0.0.8 (2017-11-9)
------------------

**Improvement**

* Making `Job` accept all python callables.
* Increasing the test coverage by adding basic tests for run().

v0.0.7 (2017-10-31)
-------------------

**Bugfixes**

* BashJob doesn't wait till thread is run. Fix with lambda.

v0.0.6 (2017-10-31)
-------------------

**Improvement**

* Support for bash commands using BashJob.

v0.0.5 (2017-10-30)
-------------------

**Bugfixes**

* Continuous build deprecated test fixes.

v0.0.4 (2017-10-30)
-------------------

**Improvement**

* Test coverage.
* Continuous build integration with Travis.
* Continuous coverage integration with Coveralls.

v0.0.3 (2017-10-30)
-------------------
* Inclusion of ``logging``.

v0.0.2 (2017-10-28)
-------------------

**Bugfixes**

* Fixes to setup.py for easier version bump.
* Fixes to README.rst to get rid of ``raw`` tag errors.

v0.0.1 (2107-10-28)
-------------------
* Problem -> Solution.
