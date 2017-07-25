Command support
===============

>>> import guild

Op preview
----------

Op preview support is provided by `cmd_support`. Let's illustrate by
defining an op with various command arguments and a typical
environment:

>>> args = [
...     "python",
...     "-u", "intro.py",
...     "--epochs", "100",
...     "--foo", "this is foo",
...     "-F", "this_if_F"]
>>> env = {
...     "RUNDIR": "/tmp"
... }
>>> op = guild.op.Op(args, env, ".", {}, [])

And use `preview_op` to preview it:

>>> guild.cmd_support.preview_op(op)
Command:
<BLANKLINE>
  python \
    -u intro.py \
    --epochs 100 \
    --foo "this is foo" \
    -F this_if_F
<BLANKLINE>
Environment:
<BLANKLINE>
  RUNDIR=/tmp
