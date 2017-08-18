Op Dir Meta
===========

>>> import guild.opdir

Meta attributes are stored under an op directory. These are used to
quickly read op attributes directly from the file system.

Attributes are stored as follows::

    guild.d/meta/KEY-1
    guild.d/meta/KEY-2
    ...

Values are stored as arbitrary file content, though are generally
string values not ending with a line feed.

>>> opdir = mkdtemp()
>>> guild.opdir.write_all_meta(opdir, {
...    "foo": 123,
...    "bar": "hello bar",
...    "baz": 1.1234})
>>> find(opdir)
['guild.d/meta/bar', 'guild.d/meta/baz', 'guild.d/meta/foo']

We can read the attributes back:

>>> pprint(guild.opdir.read_all_meta(opdir))
{'bar': 'hello bar', 'baz': '1.1234', 'foo': '123'}
