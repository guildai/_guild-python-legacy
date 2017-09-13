import os
import shutil
import sys

import guild.cli
import guild.cmd_support
# Avoid expensive imports here

def add_parser(subparsers):
    p = guild.cmd_support.add_parser(
        subparsers,
        "sync", "synchronize with package repositories",
        """Synchronizes with configured package repositories.

        When searching or installing packages, Guild uses locally
        cached repository data. Use sync to ensure repository data is
        up-to-date before running search or install.
        """)
    p.set_defaults(func=main)

def main(args):
    import guild.git
    import guild.user

    current_repos = guild.user.read_config("repos", [])
    for repo in current_repos:
        _sync_repo(repo)
    for path in _deleted_repos(current_repos):
        _delete_repo(path)

def _sync_repo(repo):
    name, url = _repo_attrs(repo)
    sys.stdout.write("Synchronizing %s repo\n" % name)
    repo_path = os.path.join(_repos_home(), name)
    resolved_url = _resolve_url(url)
    if os.path.exists(repo_path):
        guild.git.pull(repo_path, resolved_url)
    else:
        guild.git.clone(repo_path, resolved_url)

def _repo_attrs(repo):
    try:
        return repo["name"], repo["url"]
    except KeyError:
        guild.cli.error(
            "error in repos config\n"
            "Try editing %s to resolve this problem."
            % guild.user.user_config_path())

def _resolve_url(url):
    if url.startswith("file://"):
        return "file://" + os.path.expanduser(url[7:])
    else:
        return url

def _deleted_repos(current):
    installed = _cached_repos()
    for path in installed:
        name = os.path.basename(path)
        if not _repo_name_exists(name, current):
            yield path

def _cached_repos():
    repos_home = _repos_home()
    all_paths = [
        os.path.join(repos_home, name)
        for name in os.listdir(repos_home)]
    return [path for path in all_paths if os.path.isdir(path)]

def _repos_home():
    return os.path.join(guild.user.home(), "repos")

def _repo_name_exists(name, repos):
    for repo in repos:
        if repo.get("name") == name:
            return True
    return False

def _delete_repo(path):
    sys.stdout.write(
        "Removing deleted %s repo\n"
        % os.path.basename(path))
    _assert_cached_repo(path)
    shutil.rmtree(path)

def _assert_cached_repo(path):
    if not path.startswith(_repos_home()):
        raise AssertionError(path)
