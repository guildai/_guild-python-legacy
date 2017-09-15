import os

import semantic_version
import yaml

import guild.user

class Pkg(object):

    def __init__(self, pkg_path):
        self.path = pkg_path
        self.data = _load_pkg_data(pkg_path)
        self.repo = _repo_name_for_path(pkg_path)

    @property
    def name(self):
        return self.data.get("name")

    @property
    def tags(self):
        return self.data.get("tags", [])

    @property
    def description(self):
        return self.data.get("description", "")

    @property
    def version(self):
        v = self.data.get("version")
        return str(v) if v is not None else None

def _load_pkg_data(pkg_path):
    return yaml.load(open(pkg_path, "r"))

def _repo_name_for_path(path):
    return path.split(os.sep)[-3]

def all_packages():
    repos_home = guild.user.user_dir("packages")
    for parent, dirs, _files in os.walk(repos_home, topdown=True):
        try:
            dirs.remove(".git")
        except ValueError:
            pass
        pkg_path = os.path.join(parent, "pkg.yml")
        if os.path.isfile(pkg_path):
            yield Pkg(pkg_path)

def compare_versions(v1, v2):
    try:
        sv1 = semantic_version.Version(v1)
        sv2 = semantic_version.Version(v2)
    except Exception:
        return cmp(v1, v2)
    else:
        return cmp(sv1, sv2)

