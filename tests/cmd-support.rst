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
>>> op = guild.op.Op(
...          cmd_args=args,
...          cmd_env=env,
...          cmd_cwd=".",
...          opdir_pattern=None,
...          meta={},
...          tasks=[])

And use `preview_op` to preview it:

>>> guild.cmd_support.preview_op(op)
This command will use the settings below.
<BLANKLINE>
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
<BLANKLINE>
