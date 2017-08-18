Op support
==========

Operations may use the `op_support` module for operation related help.

>>> import guild.op_support
>>> import guild.project

Python command for spec
-----------------------

Guild assumes that operation specs define Python commands (this will
likely change in future releases).

Use `python_cmd_for_spec` to resolve a command spec to a full Python
command.

First let's load a project:

>>> project = guild.project.from_dir(sample("mnist"))
>>> section = project.default_section("models")
>>> spec = section.attr("prepare")
>>> cmd = guild.op_support.python_cmd_for_spec(spec, section)
>>> pprint(cmd)
['python',
 '-u',
 '/home/garrett/SCM/guild-python/tests/samples/mnist/intro.py',
 '--prepare',
 '--batch_size',
 '100',
 '--datadir',
 './data',
 '--epochs',
 '100',
 '--rundir',
 '$RUNDIR']

Note that the path to the Python script is absolute. This is because
the project directory is not the current working directory. This
ensures that the python script can be run when the cwd is changed to
the project directory.
