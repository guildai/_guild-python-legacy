import binascii
import os
import re
import sqlite3
import struct
import sys

import guild.opdir
import guild.util

DEFAULT_SERIES_ENCODING = 1
NULL_ENC = b"\xff\xff\xff\xff\xff\xff\xff\xff"

class Pool(object):

    def __init__(self):
        self._dbs = {}

    def for_run(self, run):
        db = self._dbs.get(run.id)
        if db is None:
            db = init_for_opdir(run.opdir)
            self._dbs[run.id] = db
        return db

    def close(self):
        for db in self._dbs.values():
            db.close()
        self._dbs.clear()

class DB(object):

    def __init__(self, path):
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._try_init_schema()

    def log_attrs(self, attrs):
        if attrs:
            arg_placeholders = _sql_arg_placeholders(attrs)
            SQL = "insert or replace into attr values %s" % arg_placeholders
            params = _sql_arg_vals(attrs, (str, str))
            self._exec(SQL, params)

    def attrs(self):
        SQL = "select * from attr"
        return self._select(SQL)

    def log_flags(self, flags):
        if flags:
            arg_placeholders = _sql_arg_placeholders(flags)
            SQL = "insert or replace into flag values %s" % arg_placeholders
            params = _sql_arg_vals(flags, (str, str))
            self._exec(SQL, params)

    def flags(self):
        SQL = "select * from flag"
        return self._select(SQL)

    def log_series_values(self, vals):
        if vals:
            self._update_series_key_hashes(vals)
            self._insert_series_values(vals)

    def _update_series_key_hashes(self, series_vals):
        vals = [(key, _key_hash(key)) for key, _ in series_vals]
        arg_placeholders = _sql_arg_placeholders(vals)
        SQL = "insert or ignore into series_key values %s" % arg_placeholders
        params = _sql_arg_vals(vals, (str, int))
        self._exec(SQL, params)

    def _insert_series_values(self, raw_vals):
        encoded_vals = _encode_series_values(raw_vals)
        if encoded_vals:
            arg_placeholders = _sql_arg_placeholders(encoded_vals)
            SQL = "insert or ignore into series values %s" % arg_placeholders
            params = _sql_arg_vals(encoded_vals, (int, int, int,
                                                  _buffer_type()))
            self._exec(SQL, params)

    def series_keys(self):
        SQL = "select key from series_key order by key"
        return [key for key, in self._select(SQL)]

    def series_values(self, pattern):
        key_hashes = self._key_hashes_for_pattern(pattern)
        encoded_series = self._encoded_series_for_hashes(key_hashes)
        return _decode_series_values(encoded_series, _key_lookup(key_hashes))

    def _encoded_series_for_hashes(self, hashes):
        SQL = """
        select key_hash, time, encoding, data from series
            where key_hash in (%s) order by key_hash, time
        """ % _hash_list(hashes)
        return self._select(SQL)

    def _key_hashes_for_pattern(self, pattern):
        all_hashes = self._select("select key, hash from series_key")
        return _filter_hashes(all_hashes, pattern)

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
        create table if not exists series (
            key_hash integer,
            time integer,
            encoding integer,
            data,
            primary key (key_hash, time));
        create table if not exists series_key (
            key text primary key,
            hash integer);
        create table if not exists output (
            time integer,
            stream integer,
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

def _key_hash(key):
    return binascii.crc32(key.encode("UTF-8")) & 0xffffffff

def _encode_series_values(raw_values):
    encoded = []
    for key, series in raw_values:
        if series:
            t0 = series[0][0]
            encoded.append(
                (_key_hash(key),
                 t0,
                 DEFAULT_SERIES_ENCODING,
                 _default_series_encode(series)))
    return encoded

def _default_series_encode(vals):
    parts = []
    for time, step, val in vals:
        parts.append(_encode_time_step_val(time, step, val))
    return b"".join(parts)

def _encode_time_step_val(time, step, val):
    time_step_enc = struct.pack(">QQ", time, step)
    if val is None:
        val_enc = NULL_ENC
    else:
        val_enc = struct.pack(">d", val)
    return time_step_enc + val_enc

def _filter_hashes(hashes, pattern):
    cre = re.compile(r"^%s$" % pattern)
    return [(key, hash) for key, hash in hashes if cre.match(key) is not None]

def _hash_list(hashes):
    return ",".join([str(hash) for _key, hash in hashes])

def _key_lookup(hashes):
    return dict([(hash, key) for key, hash in hashes])

def _decode_series_values(encoded, key_lookup):
    vals = []
    cur_hash = None
    key_vals_acc = []
    for key_hash, _t0, encoding, data in encoded:
        if cur_hash is not None and key_hash != cur_hash:
            vals.append((key_lookup[cur_hash], key_vals_acc))
            key_vals_acc = []
        cur_hash = key_hash
        for val in _series_decode(encoding, data):
            key_vals_acc.append(val)
    if key_vals_acc:
        vals.append((key_lookup[cur_hash], key_vals_acc))
    return vals

def _series_decode(encoding, data):
    if encoding == DEFAULT_SERIES_ENCODING:
        return _default_series_decode(data)
    else:
        raise AssertionError(encoding)

def _default_series_decode(data):
    vals = []
    offset = 0
    while offset < len(data):
        next_offset, tsv = _default_decode_time_step_val_from(data, offset)
        vals.append(tsv)
        offset = next_offset
    return vals

def _default_decode_time_step_val_from(data, offset):
    time_step_enc = data[offset:offset+16]
    time, step = struct.unpack(">QQ", time_step_enc)
    val_enc = data[offset+16:offset+24]
    if val_enc == NULL_ENC:
        val = None
    else:
        val, = struct.unpack(">d", val_enc)
    return offset + 24, (time, step, val)

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

def _buffer_type():
    # Handles buffer type for Python3
    if sys.version_info > (3,):
        return memoryview
    else:
        return buffer # pylint: disable=undefined-variable
