Op support
==========

Operations may use the `op_support` module for operation related help.

>>> import guild

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
 'intro',
 '--prepare',
 'epochs',
 '100',
 'datadir',
 './data',
 'rundir',
 '$RUNDIR',
 'batch_size',
 '100']
