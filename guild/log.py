import logging

DEFAULT_SOURCE = "guild"

def error(msg, source=DEFAULT_SOURCE, *args):
    _log(logging.error, msg, args, source)

def warning(msg, source=DEFAULT_SOURCE, *args):
    _log(logging.warning, msg, args, source)

def info(msg, source=DEFAULT_SOURCE, *args):
    _log(logging.info, msg, args, source)

def debug(msg, source=DEFAULT_SOURCE, *args):
    _log(logging.debug, msg, args, source)

def exception(msg, source=DEFAULT_SOURCE, *args):
    _log(logging.debug, msg, args, source)

def _log(log_fun, msg, args, source):
    msg_with_source = ("[%s]" % source) + msg
    log_fun(msg_with_source, *args)
