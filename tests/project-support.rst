Project support
===============

The `cmd_support` module provides a number of functions to support
commands, including a number of functions to help with project related
tasks.

>>> import guild.cmd_support

Loading a project from command line args
----------------------------------------

The tests below require a valid "args" object that contains project
related options. We'll create one here as per
`guild_main.project_options`:

>>> class Args(object):
...   def __init__(self, **kw):
...     for name in kw:
...       setattr(self, name, kw[name])
>>> args = Args(project_dir=sample("mnist"))

We can use `project_for_args` to load a valid project:

>>> project = guild.cmd_support.project_for_args(args)
>>> project.attr("name")
'MNIST'

If we specify an invalid project directory we get an Exit error:

>>> args = Args(project_dir="does_not_exist")
>>> guild.cmd_support.project_for_args(args)
Traceback (most recent call last):
Exit: (1) Directory 'does_not_exist' does not exist

If we specify a directory that does not contain a Guild project file,
we get a different Exit error:

>>> args = Args(project_dir=sample(".."))
>>> guild.cmd_support.project_for_args(args)
Traceback (most recent call last):
Exit: (1) Directory 'tests/samples/..' does not contain a guild.yml file
Try 'guild init tests/samples/..' to initialize a project or specify a different project directory

Project flags from the command line
-----------------------------------

The function `project_for_arg` extends the project with flags
specified on the command line:

>>> args = Args(project_dir=sample("mnist"),
...             flags=("foo=bar", "bar=baz"),
...             profiles=("bam",))
>>> project = guild.cmd_support.project_for_args(args)
>>> project.command_line_flags
[('foo', 'bar'), ('bar', 'baz')]
>>> project.command_line_profiles
['bam']
