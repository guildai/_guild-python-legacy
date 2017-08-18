Guild utils
===========

The module `guild.util` is a set of general utility functions.

>>> import guild.util

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

Reducing lists
--------------

When users view large datasets, we often want to reduce the number of
values viewed. This can dramatically improve performance for larger
datasets.

Use `reduce_to` to reduce a list to a maximum number of items.

>>> red = guild.util.reduce_to

Reducing to one item:

>>> red([], 1)
[]
>>> red([1], 1)
[1]
>>> red([1, 2], 1)
[2]
>>> red([1, 2, 3], 1)
[3]

Reducing to two items:

>>> red([], 2)
[]
>>> red([1], 2)
[1]
>>> red([1, 2], 2)
[1, 2]
>>> red([1, 2, 3], 2)
[1, 3]

Reducing a list of ten items to various lengths:

>>> l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> red(l, 1)
[10]
>>> red(l, 2)
[4, 10]
>>> red(l, 3)
[2, 6, 10]
>>> red(l, 4)
[1, 4, 7, 10]
>>> red(l, 5)
[1, 4, 7, 10]
>>> red(l, 6)
[2, 4, 6, 8, 10]
>>> red(l, 7)
[2, 4, 6, 8, 10]
>>> red(l, 8)
[2, 4, 6, 8, 10]
>>> red(l, 9)
[2, 4, 6, 8, 10]
>>> red(l, 10)
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> red(l, 11)
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
