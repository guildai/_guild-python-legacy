import guild.opdir
import guild.util

def op_status(opdir):
    pid = op_pid(opdir)
    if pid is None:
        return "stopped"
    elif guild.util.pid_exists(pid):
        return "running"
    else:
        return "crashed"

def extended_op_status(opdir):
    """Uses exit_status to extend the status to include error or success."""
    base_status = op_status(opdir)
    if base_status == "running":
        return "running"
    elif base_status == "crashed":
        return "terminated"
    elif base_status == "stopped":
        exit_status = guild.opdir.read_meta(opdir, "exit_status")
        if exit_status == "0":
            return "completed"
        else:
            return "error"

def op_pid(opdir):
    lock = guild.opdir.guild_file(opdir, "LOCK")
    try:
        return int(_read_file(lock))
    except (IOError, ValueError):
        return None

def _read_file(path):
    with open(path, "r") as f:
        return f.read()
