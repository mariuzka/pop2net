.. currentmodule:: pop2net
.. highlight:: shell

===================
Notes to Developers
===================

Versioning
==========

We use a semantic versioning approach of MAJOR.MINOR.PATCH.

- MAJOR versions are not guaranteed to be backwards compatible,
- MINOR versions indicate the addition of new functionality, and
- PATCH versions only fix bugs and do not otherwise influence the functionality of the package.

.. note::
  It is important to note, that all releases will be published on GitHub, but only stable releases (i.e., not prereleases -> there is no letter in the version number) will be released on pypi.
  That ensures that users of the package can rely on PyPi to always have a up-to-date stable version, whereas developers can easily get pre-releases to test new functionality.


How to Contribute
=================

Thank you for your interest in contributing! 🎉
We welcome bug reports, feature requests, documentation improvements, and code contributions.

1. Reporting Issues
-------------------

Use the `GitHub issues`_ to report bugs or suggest features.

.. _GitHub issues: https://github.com/mariuzka/pop2net/issues

When reporting a bug, include:

- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, package version)

2. Development setup
--------------------

To install pop2net for development, it is strongly advised to use `poetry <https://python-poetry.org/>`_.
This has to be installed outside the virtual environment.
The recommended way to have poetry installed, generally is via `pipx <https://pipx.pypa.io/stable/installation/>`_.
Once poetry is installed, just run ``poetry install`` from within the repository to install the package, all dependencies as well as all test and development dependencies.

3. Testing
----------

Every code contribution should include tests to help maintain quality and reliability.
We use pytest for testing and ship pytest as a dev dependency.
That after installation, the tests can be run with ``poetry run pytest``

4. Submitting a Pull Request
----------------------------

- Push your branch to your fork.
- Open a Pull Request (PR) against the ``dev`` branch.
- Clearly describe what your PR does and reference any related issues.
- A maintainer will review your PR and may request changes.

For core developers
===================

Branches
--------

The ``main`` branch is locked and can only be modified via PRs.
The general idea for a development workflow is:

1. Create a new feature branch based on ``dev``.
2. Create a PR from your feature branch to ``dev``.
3. Once we release a new version, we set it up in ``dev`` and create a release PR from ``dev`` to ``main``.

If your are not a member of the core development team, PRs are generally always welcome.
Please fork the repository, create a new branch and create your PRs from there to ``pop2net/dev``.

How to Release
--------------

The release process is triggered manually as a GitHub Action that is called "Release New Version".
In a dropdown menu, you can select how much you want to increment the version.
The parameters that are selectable are directly passed to a ``poetry version`` command, so to see how the version changes, best check poetry's documentation directly `here <https://python-poetry.org/docs/cli#version>`_.
