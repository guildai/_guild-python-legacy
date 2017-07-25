import sys

def error(err):
    sys.stderr.write("ERROR: ")
    sys.stderr.write(str(err))
    sys.stderr.write("\n")
