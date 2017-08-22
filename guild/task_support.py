from __future__ import division

import time

class Stop(Exception):
    pass

def series_timestamp():
    return int(time.time() * 1000)

def loop(cb, interval, stop, first=None, on_stop=True):
    try:
        _loop(cb, interval, stop, first, on_stop)
    except Stop:
        pass
    except KeyboardInterrupt:
        pass

def _loop(cb, interval, stop, first, on_stop):
    loop_interval = first if first is not None else interval
    start = time.time()
    while True:
        sleep = _sleep_interval(loop_interval, start)
        loop_interval = interval
        stop_signal = stop.poll(sleep)
        if stop_signal:
            if on_stop:
                _loop_cb(cb)
            stop.send("ack")
            break
        else:
            _loop_cb(cb)

def _loop_cb(cb):
    cb_fun, cb_args = cb
    cb_fun(*cb_args)

def _sleep_interval(interval, start):
    if interval <= 0:
        return 0
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
