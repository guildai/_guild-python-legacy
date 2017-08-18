__version__ = None
__git_commit__ = None

def version():
    if __version__:
        return __version__
    elif __git_commit__:
        return "GIT (%s)" % __git_commit__
    else:
        return "UNKNOWN"
