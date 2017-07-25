import os

def home():
    abs_file = os.path.abspath(__file__)
    return os.path.dirname(os.path.dirname(abs_file))

def script(name):
    return os.path.join(home(), "scripts", name)

def pkg_home():
    return user_dir("pkg")

def user_dir(name):
    return os.path.join(os.getenv("HOME"), ".guild", name)
