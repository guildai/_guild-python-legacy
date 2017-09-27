import re

import guild.cmd_support
import guild.source

class PkgIndex(object):

    def __init__(self):
        self._term_keys = {}
        self._pkgs = {}

    def pkg_term(self, term, pkg):
        term_keys = self._term_keys.setdefault(term, [])
        key = _pkg_key(pkg)
        term_keys.append(key)
        self._pkgs[key] = pkg

    def matches_all(self, terms):
        return self._match(terms, set.intersection)

    def matches_any(self, terms):
        return self._match(terms, set.union)

    def _match(self, terms, set_join):
        matching_keys = [
            set(self._term_keys.get(term, []))
            for term in terms
        ]
        intersection_keys = set_join(*matching_keys)
        return [self._pkgs[key] for key in intersection_keys]

def _pkg_key(pkg):
    return (pkg.repo, pkg.name)

def main(args):
    index = _init_index()
    for pkg in _match(args, index):
        _print_pkg(pkg)

def _init_index():
    index = PkgIndex()
    for pkg in guild.source.all_packages():
        _index_pkg(pkg, index)
    return index

def _index_pkg(pkg, index):
    for term in _pkg_search_terms(pkg):
        _update_index_term(term, pkg, index)

# TODO: fill in
DROP_TERMS = set([
    "and", "the", "a", "an", "in", "of"
])

def _pkg_search_terms(pkg):
    yield pkg.repo
    yield pkg.name
    for tag in pkg.tags:
        yield tag
    for term in _split_desc(pkg.description):
        if term not in DROP_TERMS:
            yield term

def _split_desc(desc):
    return re.split("[^(a-z)]+", desc.lower())

def _update_index_term(term, pkg, index):
    index.pkg_term(term, pkg)

def _match(args, index):
    if args.all:
        return index.matches_all(args.terms)
    else:
        return index.matches_any(args.terms)

def _print_pkg(pkg):
    print("%s\t%s" % (pkg.key, pkg.description))
