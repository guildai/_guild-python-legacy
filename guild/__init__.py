import guild.app
import guild.check_cmd
import guild.cli
import guild.cmd_support
import guild.devmode
import guild.evaluate_cmd
import guild.log
import guild.op
import guild.op_support
import guild.opdir
import guild.prepare_cmd
import guild.project
import guild.project_util
import guild.system
import guild.train_cmd
import guild.util

VERSION = None
GIT_COMMIT = None

def version():
    if VERSION:
        return VERSION
    elif GIT_COMMIT:
        return "GIT (%s)" % GIT_COMMIT
    else:
        return "UNKNOWN"
