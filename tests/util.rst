Guild utils
===========

The module `guild.util` is a set of general utility functions.

>>> import guild

Resolving arguments
-------------------

Use `resolve_args` to resolve env references within a list of
arguments.

>>> env = {"RUNDIR": "foo"}
>>> args = ["--rundir", "$RUNDIR", "--train-dir", "$RUNDIR/train"]
>>> guild.util.resolve_args(args, env)
['--rundir', 'foo', '--train-dir', 'foo/train']

Finding executables
-------------------

>>> import os
>>> if os.name == "posix":
...    guild.util.find_executable("ls") == "/bin/ls"
... else:
...    True
True
