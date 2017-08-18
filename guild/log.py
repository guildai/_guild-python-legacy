import logging

DEFAULT_SOURCE = "guild"

def error(msg, *args, **kw):
    _log(logging.error, msg, args, kw)

def warning(msg, *args, **kw):
    _log(logging.warning, msg, args, kw)

def info(msg, *args, **kw):
    _log(logging.info, msg, args, kw)

def debug(msg, *args, **kw):
    _log(logging.debug, msg, args, kw)

def exception(msg, *args, **kw):
    _log(logging.debug, msg, args, kw)

def _log(log_fun, msg, args, kw):
    source = kw.get("source", DEFAULT_SOURCE)
    msg_with_source = ("[%s] " % source) + msg
    log_fun(msg_with_source, *args)
