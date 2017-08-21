import doctest
import os
import pprint
import re
import sys
import tempfile

class Py23DocChecker(doctest.OutputChecker):
    """Output checker that works around Python 2/3 unicode representations.

    https://dirkjan.ochtman.nl/writing/2014/07/06/single-source-python-23-doctests.html
    """

    def check_output(self, want, got, optionflags):
        if sys.version_info[0] > 2:
            want = re.sub("u'(.*?)'", "'\\1'", want)
            want = re.sub('u"(.*?)"', '"\\1"', want)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)

def testfile(path):
    return testfile_(
        path,
        globs=test_globals(),
        optionflags=(
            doctest.REPORT_ONLY_FIRST_FAILURE |
            doctest.ELLIPSIS |
            doctest.IGNORE_EXCEPTION_DETAIL |
            doctest.NORMALIZE_WHITESPACE))

def testfile_(filename, globs, optionflags):
    """Modified from doctest.py to use custom checker."""

    text, filename = _load_testfile(filename)
    name = os.path.basename(filename)

    if globs is None:
        globs = {}
    else:
        globs = globs.copy()
    if '__name__' not in globs:
        globs['__name__'] = '__main__'

    checker = Py23DocChecker()
    runner = doctest.DocTestRunner(
        checker=checker,
        verbose=None,
        optionflags=optionflags)

    parser = doctest.DocTestParser()
    test = parser.get_doctest(text, globs, name, filename, 0)
    runner.run(test)

    runner.summarize()

    if doctest.master is None:
        doctest.master = runner
    else:
        doctest.master.merge(runner)

    return doctest.TestResults(runner.failures, runner.tries)

def _load_testfile(filename):
    # Wrapper to handle Python 2/3 differences
    # pylint: disable=protected-access
    try:
        # pylint: disable=no-value-for-parameter
        return doctest._load_testfile(filename, None, True)
    except TypeError:
        # pylint: disable=too-many-function-args
        return doctest._load_testfile(filename, None, True, "utf-8")

def test_globals():
    return {
        "cat": cat,
        "find": find,
        "mkdtemp": mkdtemp,
        "pprint": pprint.pprint,
        "sample": sample,
        "samples_dir": samples_dir
    }

def sample(name):
    return os.path.join(samples_dir(), name)

def samples_dir():
    return os.path.join("tests", "samples")

def mkdtemp():
    return tempfile.mkdtemp(prefix="guildtest-")

def find(root):
    all = []
    for path, _, files in os.walk(root):
        for name in files:
            full_path = os.path.join(path, name)
            rel_path = os.path.relpath(full_path, root)
            all.append(rel_path)
    all.sort()
    return all

def cat(file_path):
    with open(file_path, "r") as f:
        return f.read()
