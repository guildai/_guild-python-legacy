from __future__ import division

import time

class Stop(Exception):
    pass

def series_timestamp():
    return int(time.time() * 1000)

def loop(cb, interval, stop):
    cb_fun, cb_args = cb
    start = time.time()
    while True:
        sleep = _sleep_interval(interval, start)
        try:
            stop_signal = stop.poll(sleep)
        except KeyboardInterrupt:
            break
        if stop_signal:
            stop.send("ack")
            break
        try:
            cb_fun(*cb_args)
        except Stop:
            break

def _sleep_interval(interval, start):
    now_ms = int(time.time() * 1000)
    interval_ms = int(interval * 1000)
    start_ms = int(start * 1000)
    sleep_ms = (
        ((now_ms - start_ms) // interval_ms + 1)
        * interval_ms + start_ms - now_ms)
    return sleep_ms / 1000

def log_kv_as_series(kvs, db):
    vals = []
    timestamp = series_timestamp()
    for key, val in kvs.items():
        vals.append((key, [[timestamp, 0, val]]))
    db.log_series_values(vals)
