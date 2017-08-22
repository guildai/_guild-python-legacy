import guild.log
import guild.system
import guild.tensorflow_support

def start(op, _stop):
    attrs = (
        _sys_attrs() +
        _gpu_attrs() +
        _tensorflow_attrs())
    guild.log.debug("system attrs: %s", attrs)
    op.db.log_attrs(attrs)

def _sys_attrs():
    return list(guild.system.sys_attrs().items())

def _gpu_attrs():
    flattened = []
    for index, attrs in enumerate(guild.system.gpu_attrs()):
        flattened.append(("gpu%i_name" % index, attrs["name"]))
        flattened.append(("gpu%i_memory" % index, attrs["memory"]))
    return flattened

def _tensorflow_attrs():
    return list(guild.tensorflow_support.tf_attrs().items())
