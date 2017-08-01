class NullAttrs(object):

    def __getattr__(self, _name):
        return None

def cpu_percent(*_args):
    return []

def disk_io_counters(*_args):
    return {}

def disk_partitions(*_args):
    return []

def virtual_memory(*_args):
    return NullAttrs()

def swap_memory(*_args):
    return NullAttrs()
