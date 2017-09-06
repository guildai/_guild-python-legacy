import argparse
import logging
import socket
import sys

import guild.cli
import guild.cmd_support
# Avoid expensive imports here

DEFAULT_PORT = 6333
DEFAULT_REFRESH_INTERVAL = 5

def add_parser(subparsers):
    p = guild.cmd_support.add_parser(
        subparsers,
        "view", "start Guild View",
        """Start a web based app to view and interact with a project.

        When the server is running, open your browser on the specified
        port (default is %i) - e.g. http://localhost:%i.

        To log server requests, use --logging.

        To modify the refresh interval (default is %i seconds), use
        --interval. This is useful for longer running operations that
        don't need to be refreshed often.
        """ % (DEFAULT_PORT, DEFAULT_PORT, DEFAULT_REFRESH_INTERVAL))
    guild.cmd_support.add_project_arguments(p)
    p.add_argument(
        "-H", "--host",
        help="HTTP server host (default is to listen on all interfaces)",
        default="")
    p.add_argument(
        "-p", "--port",
        help="HTTP server port (default is %i)" % DEFAULT_PORT,
        metavar="PORT",
        type=int,
        default=DEFAULT_PORT)
    p.add_argument(
        "-n", "--interval",
        help=("refresh interval in seconds (default is %i)"
              % DEFAULT_REFRESH_INTERVAL),
        metavar="SECONDS",
        dest="refresh_interval",
        type=int,
        default=DEFAULT_REFRESH_INTERVAL)
    p.add_argument(
        "--logging",
        help="enable HTTP request logging",
        action="store_true")
    p.add_argument(
        "--tensorboard",
        default="tensorboard",
        metavar="PATH",
        help="path to the TensorBoard executable used by Guild View")
    p.add_argument(
        "--tf-demo",
        help=argparse.SUPPRESS,
        action="store_true")
    p.set_defaults(func=main)

def main(args):
    import guild.view
    import guild.view_http

    project = guild.cmd_support.project_for_args(args, use_plugins=True)
    settings = _view_settings_for_args(args)
    tb_proxy = _try_start_tensorboard_proxy(project, args)
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

def _try_start_tensorboard_proxy(project, args):
    import guild.tensorboard_proxy

    logdir = guild.project_util.runs_dir_for_project(project)
    port = guild.util.free_port()
    proxy = guild.tensorboard_proxy.TensorBoardProxy(
        args.tensorboard, logdir, port)
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
