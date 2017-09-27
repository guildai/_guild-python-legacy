import os

import semantic_version
import yaml

import guild.log
import guild.user
import guild.util

class NoSuchPackageError(Exception):

    def __init__(self, spec):
        super(NoSuchPackageError, self).__init__(self)
        self.spec = spec

class MultiplePackagesError(Exception):

    def __init__(self, spec, pkgs):
        super(MultiplePackagesError, self).__init__(spec, pkgs)
        self.spec = spec
        self.pkgs = pkgs

class ValidationError(Exception):

    def __init__(self, msg):
        super(ValidationError, self).__init__(msg)

class MissingSourcesError(Exception):

    def __init__(self, pkg):
        super(MissingSourcesError, self).__init__(pkg)

class AlreadyInstalled(Exception):

    def __init__(self, src):
        super(AlreadyInstalled, self).__init__(src)

class Pkg(object):

    def __init__(self, pkg_path):
        self.path = pkg_path
        self.data = _load_pkg_data(pkg_path)
        self.repo = _repo_name_for_path(pkg_path)

    @property
    def name(self):
        return self.data.get("name")

    @property
    def key(self):
        return "%s:%s" % (self.repo, self.name)

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

    @property
    def sources(self):
        return self.data.get("sources", [])

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

def resolve_one_package(spec):
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
        try:
            pkg0 = current[pkg.key]
        except KeyError:
            current[pkg.key] = pkg
        else:
            current[pkg.key] = _latest_package(pkg0, pkg)
    return current.values()

def _latest_package(p1, p2):
    return p1 if compare_versions(p1.version, p2.version) > 0 else p2

def resolve_all_packages(specs):
    return [resolve_one_package(spec) for spec in specs]

def install_pkg(pkg):
    if not pkg.sources:
        raise MissingSourcesError(pkg)
    tmp = guild
    print("TODO: install %s" % pkg.key)

def ensure_pkg_sources(pkg):
    if not pkg.sources:
        raise MissingSourcesError(pkg)
    for src in pkg.sources:
        _ensure_source(src)

def _ensure_source(src):
    local_path = _cache_path_for_source(src)
    already_installed = os.path.exists(local_path)
    if not already_installed:
        _get_source(src, local_path)
    _validate_source(src, local_path)
    if already_installed:
        raise AlreadyInstalled(src)

def _cache_path_for_source(src):
    sha256 = src.get("sha256")
    if not sha256:
        raise ValueError("src missing sha256: %s" % src)
    return os.path.join(guild.user.user_dir("cache"), sha256)

def _get_source(src, dest_dir):
    import guild.wget # expensive, import lazily
    for url in src.get("urls", []):
        dest_basename = guild.util.url_basename(url)
        dest_filename = os.path.join(dest_dir, dest_basename)
        try:
            guild.wget.get_to_file(url, dest_filename)
        except Exception:
            guild.log.exception("wget: %s" % url)
        else:
            break

def _validate_source(src, local_path):
    files = os.listdir(local_path)
    if len(files) != 1:
        raise AssertionError("%s: %s", (local_path, files))
    src_filename = os.path.join(local_path, files[0])
    expected_sha256 = src["sha256"]
    actual_sha256 = guild.util.sha256_sum(src_filename)
    if expected_sha256 != actual_sha256:
        raise ValidationError(
            "bad sha256 for %s - expected %s but got %s"
            % (src_filename, expected_sha256, actual_sha256))
