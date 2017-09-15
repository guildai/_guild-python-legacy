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
    for parent, dirs, _files in _walk(repos_home):
        try:
            dirs.remove(".git")
        except ValueError:
            pass
        pkg_path = os.path.join(parent, "pkg.yml")
        if os.path.isfile(pkg_path):
            yield Pkg(pkg_path)

def _walk(path):
    return os.walk(path, topdown=True, followlinks=True)

def compare_versions(v1, v2):
    try:
        sv1 = semantic_version.Version(v1)
        sv2 = semantic_version.Version(v2)
    except Exception:
        return cmp(v1, v2)
    else:
        return cmp(sv1, sv2)

class NoSuchPackageError(Exception):

    def __init__(self, spec):
        super(NoSuchPackageError, self).__init__(self)
        self.spec = spec

class MultiplePackagesError(Exception):

    def __init__(self, spec, pkgs):
        super(MultiplePackagesError, self).__init__(spec, pkgs)
        self.spec = spec
        self.pkgs = pkgs

def find_one_package(spec):
    all_matches = _find_packages(spec)
    pkgs = _remove_outdated_packages(all_matches)
    if len(pkgs) == 0:
        raise NoSuchPackageError(spec)
    elif len(pkgs) > 1:
        raise MultiplePackagesError(spec, pkgs)
    else:
        return pkgs[0]

def _find_packages(spec):
    parts = spec.split(":", 1)
    if len(parts) == 2:
        return _packages_for_repo_and_name(*parts)
    else:
        return _packages_for_name(*parts)

def _packages_for_repo_and_name(repo, name):
    return [
        pkg for pkg in all_packages()
        if pkg.repo == repo and pkg.name == name
    ]

def _packages_for_name(name):
    return [pkg for pkg in all_packages() if pkg.name == name]
    
def _remove_outdated_packages(pkgs):
    current = {}
    for pkg in pkgs:
        key = "%s:%s" % (pkg.repo, pkg.name)
        try:
            pkg0 = current[key]
        except KeyError:
            current[key] = pkg
        else:
            current[key] = _latest_package(pkg0, pkg)
    return current.values()

def _latest_package(p1, p2):
    return p1 if compare_versions(p1.version, p2.version) > 0 else p2
