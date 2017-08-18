Project support
===============

The `cmd_support` module provides a number of functions to support
commands, including a number of functions to help with project related
tasks.

>>> import guild.cmd_support

Project related command arguments
---------------------------------

Numerous commands require a valid Guild project. The command line
options for specifying a project may be defined for a parser using
`add_project_arguments`:

>>> import argparse
>>> parser = argparse.ArgumentParser()
>>> guild.cmd_support.add_project_arguments(parser, flag_support=True)

We can use these to parse command line arguments:

>>> args = parser.parse_args(["-P", sample("mnist")])
>>> args.project_dir
'tests/samples/mnist'

Loading a project from command line args
----------------------------------------

We can use `project_for_args` to load a valid project:

>>> project = guild.cmd_support.project_for_args(args)
>>> project.attr("name")
'MNIST'

If we specify an invalid project directory we get an Exit error:

>>> args = parser.parse_args(["-P", "does_not_exist"])
>>> guild.cmd_support.project_for_args(args)
Traceback (most recent call last):
Exit: (1) Directory 'does_not_exist' does not exist

If we specify a directory that does not contain a Guild project file,
we get a different Exit error:

>>> args = parser.parse_args(["-P", sample("..")])
>>> guild.cmd_support.project_for_args(args)
Traceback (most recent call last):
Exit: (1) Directory 'tests/samples/..' does not contain a guild.yml file
Try 'guild init tests/samples/..' to initialize a project or specify a different project directory

Project flags from the command line
-----------------------------------

The function `project_for_arg` extends the project with flags
specified on the command line:

>>> args = parser.parse_args(["-P", sample('mnist'),
...                           "-F", "foo=bar",
...                           "-F", "bar=baz",
...                           "--profile", "bam"])
>>> project = guild.cmd_support.project_for_args(args)
>>> project.command_line_flags
[('foo', 'bar'), ('bar', 'baz')]
>>> project.command_line_profiles
['bam']
