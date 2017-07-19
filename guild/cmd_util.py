import argparse
import re
import textwrap

__CONSOLE_WIDTH = None

def add_parser(subparsers, cmd, help, description):
    return subparsers.add_parser(
        cmd,
        help=help,
        formatter_class=argparse.RawTextHelpFormatter,
        description=format_description(description))

def format_description(desc):
    pars = desc.split("\n\n")
    return "\n\n".join([format_par(par) for par in pars])

def format_par(par):
    normalized = strip_repeating_ws(par).strip()
    wrapper = textwrap.TextWrapper(
        width=console_width() - 10)
    lines = wrapper.wrap(normalized)
    return "\n".join(lines)

def strip_repeating_ws(s):
    return re.sub("\s+", " ", s)

def console_width():
    global __CONSOLE_WIDTH
    if __CONSOLE_WIDTH is None:
        import os
        _, cols = os.popen('stty size', 'r').read().split()
        __CONSOLE_WIDTH = int(cols)
    return __CONSOLE_WIDTH
