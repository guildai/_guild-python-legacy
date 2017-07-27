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

Log flags as follows:

>>> db.log_flags([("foo", "FOO"), ("bar", 123)])
>>> pprint(db.flags())
[(u'foo', u'FOO'), (u'bar', u'123')]

Helper functions
----------------

>>> vals = [(1,2), (3,4)]
>>> guild.db._sql_arg_placeholders(vals)
'(?,?),(?,?)'
>>> guild.db._sql_arg_vals(vals, (int, int))
[1, 2, 3, 4]
>>> guild.db._sql_arg_vals(vals, (int, str))
[1, '2', 3, '4']
