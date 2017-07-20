Command utils
=============

The `cmd_util` module provides a number of functions to support
commands.

>>> import guild

Project support
---------------

Numerous commands require a valid Guild project. The command line
options for specifying a project may be defined for a parser using
`add_project_arguments`:

>>> import argparse
>>> parser = argparse.ArgumentParser()
>>> guild.cmd_util.add_project_arguments(parser)

We can use these to parse command line arguments:

>>> args = parser.parse_args(["-P", sample("mnist")])
>>> args.project_dir
'tests/samples/mnist'

We can use `project_for_args` to load a valid project:

>>> project = guild.cmd_util.project_for_args(args)
>>> project.attr("name")
'MNIST'

If we specify an invalid project directory we get an Exit error:

>>> args = parser.parse_args(["-P", "does_not_exist"])
>>> guild.cmd_util.project_for_args(args)
Traceback (most recent call last):
Exit: (1) Directory 'does_not_exist' does not exist
