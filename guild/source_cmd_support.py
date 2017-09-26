import guild.cli
import guild.source

def resolve_one_package(spec):
    try:
        return guild.source.resolve_one_package(spec)
    except guild.source.MultiplePackagesError as e:
        _multiple_matches_error(e.spec, e.pkgs)
    except guild.source.NoSuchPackageError as e:
        _no_such_package_error(e.spec)

def _no_such_package_error(spec):
    guild.cli.error("no packages match '%s'" % spec)

def _multiple_matches_error(spec, pkgs):
    guild.cli.error(
        "multiple packages match '%s'\n"
        "Specify one of: %s"
        % (spec, _multiple_matches_list(pkgs)))

def _multiple_matches_list(pkgs):
    return ", ".join(["%s:%s" % (pkg.repo, pkg.name) for pkg in pkgs])

def resolve_all_packages(specs):
    try:
        return guild.source.resolve_all_packages(specs)
    except guild.source.MultiplePackagesError as e:
        _multiple_matches_error(e.spec, e.pkgs)
    except guild.source.NoSuchPackageError as e:
        _no_such_package_error(e.spec)
