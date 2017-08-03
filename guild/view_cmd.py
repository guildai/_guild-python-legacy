import guild

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
        type=int,
        default=DEFAULT_REFRESH_INTERVAL)
    p.add_argument(
        "-l", "--logging",
        help="enable logging",
        action="store_true")
    guild.cmd_support.add_project_arguments(p)
    p.set_defaults(func=main)

def main(args):
    print("TODO: view", args)
