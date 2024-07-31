.. currentmodule:: popy
.. highlight:: shell

===================
Notes to Developers
===================


These are notes to developers.

.. note::
    We use a semantic versioning approach of MAJOR.MINOR.PATCH. MAJOR versions are not guaranteed to be backwards compatible, MINOR versions indicate the addition of new functionality, and PATCH versions only fix bugs and do not otherwise influence the functionality of the package.

Branches
========

The ``main`` branch is locked and can only be modified via PRs.
The general idea for a development workflow is:

1. Create a new feature branch based on ``dev``.
2. Create a PR from your feature branch to ``dev``.
3. Once we release a new version, we set it up in ``dev`` and create a relase PR from ``dev`` to ``main``.

If your are not a member of the core development team, PRs are generally always welcome. Please fork the repository, create a new branch and create your from there to ``popy/dev``.


How to Release
==============

For the release process, we use a tag-based approach with GitHub Actions, meaning new tags that are merged to ``main`` will automatically trigger the release of a new package version. For this, it is important to update the version number first.

The general / idealized process would be:

1. locally, switch to the ``dev`` branch
2. in ``dev``, run ``poetry version [major|minor|patch]``
  - for example, ``poetry version minor`` will increase the version number from 1.2.14 to 1.3.0 automatically. The version number is denoted in the pyproject.toml file.
  - This command will tell you what the version has been increased to (let's stick to 1.3.0 for this example).
3. create a new commit that contains the changed pyproject.toml file and set the commit message to something like "bump version"
4. create a tag, that contains the version number preceded by the letter "v", with ``git tag v1.3.0``
5. push your commit with ``git push``
6. push your tag with ``git push --tags``
7. create a new PR from ``dev`` to ``main``.
8. If all tests pass, the PR can be merged to ``main`` and automatically triggers the release of the new version on GitHub and PyPi.
