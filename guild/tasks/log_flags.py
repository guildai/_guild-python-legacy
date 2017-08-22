import guild.log

def start(op, _stop, flags):
    guild.log.debug("flags: %s", flags)
    op.db.log_flags(flags)
