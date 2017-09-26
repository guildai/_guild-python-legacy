import logging
import socket
import sys

import guild.cli
import guild.cmd_support
import guild.tensorboard_proxy
import guild.view
import guild.view_http

def main(args):
    if not args.force:
        guild.cli.error(
            "Guild View is under development and currently disabled\n"
            "Use 'guild view --force' to bypass this check.")

    project = guild.cmd_support.project_for_args(args, use_plugins=True)
    settings = _view_settings_for_args(args)
    tb_proxy = _try_start_tensorboard_proxy(project)
    view = guild.view.ProjectView(project, settings, tb_proxy)

    sys.stdout.write("Guild View running on port %i\n" % args.port)
    try:
        guild.view_http.start(args.host, args.port, view, _log_level(args))
    except socket.error:
        guild.cli.error(
            "port %i is being used by another application\n"
            "Try 'guild view --port PORT' with a different port."
            % args.port)
    else:
        sys.stdout.write("\n")
    finally:
        tb_proxy.stop()
        view.close()
        sys.stdout.write("Guild View stopped\n")

def _try_start_tensorboard_proxy(project):
    logdir = guild.project_util.runs_dir_for_project(project)
    port = guild.util.free_port()
    proxy = guild.tensorboard_proxy.TensorBoardProxy(logdir, port)
    proxy.start()
    return proxy

def _view_settings_for_args(args):
    return {
        "refreshInterval": args.refresh_interval,
        "tensorboard": {
            "demo": args.tf_demo
        }
    }

def _log_level(args):
    return logging.INFO if args.logging else logging.WARNING
