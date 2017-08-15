from __future__ import absolute_import

from . import app
from . import check_cmd
from . import cli
from . import cmd_support
from . import db
from . import devmode
from . import evaluate_cmd
from . import log
from . import op
from . import op_support
from . import op_util
from . import opdir
from . import prepare_cmd
from . import project
from . import project_cmd
from . import project_util
from . import run
from . import runs_cmd
from . import series_cmd
from . import system
from . import task_support
from . import tasks
from . import tensorflow_support
from . import test
from . import train_cmd
from . import util
from . import view
from . import view_cmd
from . import view_http

VERSION = None
GIT_COMMIT = None

def version():
    if VERSION:
        return VERSION
    elif GIT_COMMIT:
        return "GIT (%s)" % GIT_COMMIT
    else:
        return "UNKNOWN"
