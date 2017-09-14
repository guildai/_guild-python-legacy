import guild.cmd_support
# Avoid expensive imports here

def add_parser(subparsers):
    p = guild.cmd_support.add_parser(
        subparsers,
        "info", "print information about a package",
        """Prints information about a package.

        PACKAGE must be in the form [REPO:]NAME where REPO is an
        optional package repository and NAME is the package name. If
        REPO is omitted, NAME must be unique for repositories

        """)
    p.add_argument(
        "package",
        help="package to print information for",
        metavar="PACKAGE")
    p.set_defaults(func=main)

def main(args):
    print("TODO: print information for %s" % args.package)
