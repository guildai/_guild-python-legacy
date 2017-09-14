import os
import re

import guild.cli
import guild.cmd_support
# Avoid expensive imports here

class PkgIndex(object):

    def __init__(self):
        self._term_pkgs = {}
        self._pkgs = {}

    def pkg_term(self, term, key, pkg):
        pkgs = self._term_pkgs.setdefault(term, [])
        pkgs.append(key)
        self._pkgs[key] = pkg

    def matches_all(self, terms):
        return self._match(terms, set.intersection)

    def matches_any(self, terms):
        return self._match(terms, set.union)

    def _match(self, terms, set_join):
        matching_keys = [
            set(self._term_pkgs.get(term, []))
            for term in terms
        ]
        intersection_keys = set_join(*matching_keys)
        return [(key, self._pkgs[key]) for key in intersection_keys]


def add_parser(subparsers):
    p = guild.cmd_support.add_parser(
        subparsers,
        "search", "search repositories for packages",
        """Searches repositories for terms.

        By default packages matching any term are displayed. To match
        packages matching all terms, use the --all option.
        """)
    p.add_argument(
        "terms",
        help="a term to search for",
        metavar="TERM",
        nargs="+")
    p.add_argument(
        "--any",
        help="find packages matching any term (default)",
        action="store_true")
    p.add_argument(
        "--all",
        help="find packages matching all terms",
        action="store_true")
    p.set_defaults(func=main)

def main(args):
    import guild.user
    index = _init_index()
    for key, pkg in _match(args, index):
        _print_pkg(key, pkg)

def _init_index():
    index = PkgIndex()
    repos_home = guild.user.user_dir("repos")
    for parent, dirs, files in os.walk(repos_home, topdown=True):
        try:
            dirs.remove(".git")
        except ValueError:
            pass
        pkg_path = os.path.join(parent, "pkg.yml")
        if os.path.isfile(pkg_path):
            _index_pkg(pkg_path, index)
    return index

def _index_pkg(pkg_path, index):
    pkg = _load_pkg(pkg_path)
    repo_name = _repo_name_from_pkg_path(pkg_path)
    for term in _pkg_search_terms(repo_name, pkg):
        _update_index_term(term, repo_name, pkg, index)

def _load_pkg(pkg_path):
    import yaml
    return yaml.load(open(pkg_path, "r"))

# TODO: fill in
DROP_TERMS = set([
    "and", "the", "a", "an", "in", "of"
])

def _pkg_search_terms(repo_name, pkg):
    yield repo_name
    yield pkg.get("name")
    for tag in pkg.get("tags", []):
        yield tag
    for term in _split_desc(pkg.get("description")):
        if term not in DROP_TERMS:
            yield term

def _split_desc(desc):
    return re.split("[^(a-z)]+", desc.lower())

def _repo_name_from_pkg_path(pkg_path):
    return pkg_path.split(os.sep)[-3]

def _update_index_term(term, repo_name, pkg, index):
    index.pkg_term(term, _pkg_key(repo_name, pkg), pkg)

def _pkg_key(repo_name, pkg):
    return (repo_name, pkg.get("name"))

def _match(args, index):
    if args.all:
        return index.matches_all(args.terms)
    else:
        return index.matches_any(args.terms)

def _print_pkg(key, pkg):
    repo_name, pkg_name = key
    print("%s:%s\t%s" % (repo_name, pkg_name, pkg.get("description", "")))
