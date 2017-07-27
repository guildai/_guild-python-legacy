import os
import sqlite3

import guild

class DB(object):

    def __init__(self, path):
        self._conn = sqlite3.connect(path)
        self._try_init_schema()

    def log_attrs(self, attrs):
        arg_placeholders = _sql_arg_placeholders(attrs)
        SQL = "insert or replace into attr values %s" % arg_placeholders
        params = _sql_arg_vals(attrs, (str, str))
        self._exec(SQL, params)

    def attrs(self):
        SQL = "select * from attr"
        return self._select(SQL)

    def log_flags(self, flags):
        arg_placeholders = _sql_arg_placeholders(flags)
        SQL = "insert or replace into flag values %s" % arg_placeholders
        params = _sql_arg_vals(flags, (str, str))
        self._exec(SQL, params)

    def flags(self):
        SQL = "select * from flag"
        return self._select(SQL)

    def close(self):
        self._conn.close()

    def _try_init_schema(self):
        SQL = """
        create table if not exists attr (
            name text primary key,
            val text);
        create table if not exists flag (
            name text primary key,
            val text);
        """
        self._exec_script(SQL)

    def _exec(self, SQL, params=None):
        c = self._conn.cursor()
        c.execute(SQL, [] if params is None else params)
        self._conn.commit()

    def _exec_script(self, SQL):
        c = self._conn.cursor()
        c.executescript(SQL)
        self._conn.commit()

    def _select(self, SQL, params=None):
        c = self._conn.cursor()
        c.execute(SQL, [] if params is None else params)
        return list(c)

def init_for_opdir(opdir):
    db_path = guild.opdir.guild_file(opdir, "db")
    guild.util.ensure_dir(os.path.dirname(db_path))
    return DB(db_path)

def _sql_arg_placeholders(vals):
    return ",".join([_sql_arg_group(val) for val in vals])

def _sql_arg_group(val):
    qs = ["?"] * len(val)
    return "(%s)" % ",".join(qs)

def _sql_arg_vals(vals, types):
    flattened = []
    for val in vals:
        for x, t in zip(val, types):
            flattened.append(t(x))
    return flattened
