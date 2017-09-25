import guild.source_cmd_support

def main(args):
    pkg = guild.source_cmd_support.resolve_one_package(args.package)
    _print_pkg_info(pkg)

def _print_pkg_info(pkg):
    print("Package: %s:%s" % (pkg.repo, pkg.name))
    print("Version: %s" % pkg.version)
    print("Description: %s" % pkg.description)
    print("Tags: %s" % ", ".join(pkg.tags))
