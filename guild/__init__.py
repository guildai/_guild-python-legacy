import guild.app
import guild.check_cmd
import guild.cli
import guild.cmd_support
import guild.db
import guild.devmode
import guild.evaluate_cmd
import guild.log
import guild.op
import guild.op_support
import guild.op_util
import guild.opdir
import guild.prepare_cmd
import guild.project
import guild.project_util
import guild.runs_cmd
import guild.system
import guild.task_support
import guild.tasks
import guild.tensorflow_support
import guild.train_cmd
import guild.util
import guild.view_cmd
import guild.view_http

VERSION = None
GIT_COMMIT = None

def version():
    if VERSION:
        return VERSION
    elif GIT_COMMIT:
        return "GIT (%s)" % GIT_COMMIT
    else:
        return "UNKNOWN"
