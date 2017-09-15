import guild.cmd_support
# Avoid expensive imports here

def add_parser(subparsers):
    p = guild.cmd_support.add_parser(
        subparsers,
        "install", "install one or more packages",
        """Installs one or more packages.
        """)
    p.add_argument(
        "packages",
        help="package to install",
        nargs="+",
        metavar="PACKAGE")
    p.set_defaults(func=main)

def main(args):
    import guild.source_cmd_support
    pkgs = guild.source_cmd_support.resolve_all_packages(args.packages)
    _resolve_pkg_sources(pkgs)
    _install_pkgs(pkgs)

def _resolve_pkg_sources(pkgs):
    for pkg in pkgs:
        for source in pkg.sources:
            _resolve_pkg_source(source)

def _resolve_pkg_source(source):
    print("TODO: resolve source: %s" % source)

def _install_pkgs(pkgs):
    for pkg in pkgs:
        _install_pkg(pkg)

def _install_pkg(pkg):
    print("TODO: install pkg")
