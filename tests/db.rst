Guild Db
========

>>> import guild

Initializing
------------

To initialize a Guild DB, simply use the `guild.db.DB` constructor
with a path. However, in most cases, you'll use `init_for_opdir`,
which stores the database as a Guild file named `db`:

>>> tmp = mkdtemp()
>>> db = guild.db.init_for_opdir(tmp)
>>> find(tmp)
['guild.d/db']

Flags
-----

>>> db.log_flags([("foo", "FOO"), ("bar", 123)])
>>> pprint(db.flags())
[(u'foo', u'FOO'), (u'bar', u'123')]

Attrs
-----

>>> db.log_attrs([("foo", 123), ("bar", "BAR")])
>>> pprint(db.attrs())
[(u'foo', u'123'), (u'bar', u'BAR')]

Series
------

Series represent a named sequence of values, each value being a
three-tuple of timestamp, global step, and float value.

>>> vals = [("foo", [[123, 1, 1.0], [124, 2, 1.1], [125, 3, 1.2]]),
...         ("bar", [[123, 1, 2.0], [124, 2, 2.1], [125, 3, 2.2]]),
...         ("baz", [[123, 1, 3.0], [124, 2, 3.1], [125, 3, 3.2]])]
>>> db.log_series_values(vals)

To read back series, we provide a key pattern, which is used to match
against the whole series key:

>>> pprint(db.series_values("foo"))
[(u'foo', [(123, 1, 1.0), (124, 2, 1.1), (125, 3, 1.2)])]

>>> pprint(db.series_values("bar"))
[(u'bar', [(123, 1, 2.0), (124, 2, 2.1), (125, 3, 2.2)])]

>>> pprint(db.series_values("baz"))
[(u'baz', [(123, 1, 3.0), (124, 2, 3.1), (125, 3, 3.2)])]

>>> pprint(db.series_values("foo|bar"))
[(u'bar', [(123, 1, 2.0), (124, 2, 2.1), (125, 3, 2.2)]),
 (u'foo', [(123, 1, 1.0), (124, 2, 1.1), (125, 3, 1.2)])]

>>> pprint(db.series_values("ba."))
[(u'bar', [(123, 1, 2.0), (124, 2, 2.1), (125, 3, 2.2)]),
 (u'baz', [(123, 1, 3.0), (124, 2, 3.1), (125, 3, 3.2)])]

>>> pprint(db.series_values(".+"))
[(u'bar', [(123, 1, 2.0), (124, 2, 2.1), (125, 3, 2.2)]),
 (u'baz', [(123, 1, 3.0), (124, 2, 3.1), (125, 3, 3.2)]),
 (u'foo', [(123, 1, 1.0), (124, 2, 1.1), (125, 3, 1.2)])]

Edge cases:

>>> db.log_series_values([])

>>> db.log_series_values([("bam", [])])
>>> db.series_values("bam")
[]

Helper functions
----------------

>>> vals = [(1,2), (3,4)]
>>> guild.db._sql_arg_placeholders(vals)
'(?,?),(?,?)'
>>> guild.db._sql_arg_vals(vals, (int, int))
[1, 2, 3, 4]
>>> guild.db._sql_arg_vals(vals, (int, str))
[1, '2', 3, '4']
