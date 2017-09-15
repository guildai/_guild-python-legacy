import os
import shutil
import sys

import guild.cli
import guild.cmd_support
# Avoid expensive imports here

def add_parser(subparsers):
    p = guild.cmd_support.add_parser(
        subparsers,
        "sync", "synchronize with package sources",
        """Synchronizes with configured package sources.

        When searching or installing packages, Guild uses locally
        cached source data. Use sync to ensure package data is
        up-to-date before running search or install.
        """)
    p.set_defaults(func=main)

def main(_args):
    import guild.git
    import guild.user

    current_sources = guild.user.read_config("package-sources", [])
    for source in current_sources:
        _sync_source(source)
    for path in _deleted_sources(current_sources):
        _delete_source(path)

def _sync_source(source):
    name, url = _source_attrs(source)
    sys.stdout.write("Synchronizing %s source\n" % name)
    source_path = os.path.join(_packages_home(), name)
    resolved_url = _resolve_url(url)
    if os.path.exists(source_path):
        if os.path.islink(source_path):
            sys.stdout.write("%s is a link, skipping\n" % source_path)
        else:
            guild.git.pull(source_path, resolved_url)
    else:
        guild.git.clone(source_path, resolved_url)

def _source_attrs(source):
    try:
        return source["name"], source["url"]
    except KeyError:
        guild.cli.error(
            "error in sources config\n"
            "Try editing %s to resolve this problem."
            % guild.user.user_config_path())

def _resolve_url(url):
    if url.startswith("file://"):
        return "file://" + os.path.expanduser(url[7:])
    else:
        return url

def _deleted_sources(current):
    installed = _cached_sources()
    for path in installed:
        name = os.path.basename(path)
        if not _source_name_exists(name, current):
            yield path

def _cached_sources():
    packages_home = _packages_home()
    all_paths = [
        os.path.join(packages_home, name)
        for name in os.listdir(packages_home)]
    return [path for path in all_paths if os.path.isdir(path)]

def _packages_home():
    return guild.user.user_dir("packages")

def _source_name_exists(name, sources):
    for source in sources:
        if source.get("name") == name:
            return True
    return False

def _delete_source(path):
    sys.stdout.write(
        "Removing deleted %s source\n"
        % os.path.basename(path))
    _assert_cached_source(path)
    shutil.rmtree(path)

def _assert_cached_source(path):
    if not path.startswith(_packages_home()):
        raise AssertionError(path)
