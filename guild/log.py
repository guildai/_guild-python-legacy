import sys

def error(err):
    sys.stderr.write("ERROR: ")
    sys.stderr.write(str(err))
    sys.stderr.write("\n")

def warn(msg):
    sys.stderr.write("WARNING: ")
    sys.stderr.write(str(msg))
    sys.stderr.write("\n")

def info(msg):
    sys.stderr.write("INFO: ")
    sys.stderr.write(str(msg))
    sys.stderr.write("\n")
