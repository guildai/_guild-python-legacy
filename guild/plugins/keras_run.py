import os
import sys
import types

import keras

def main():
    script = _script_from_argv()
    _shift_argv()
    _patch_keras()
    _exec_script(script)

def _script_from_argv():
    return sys.argv[1]

def _shift_argv():
    sys.argv = sys.argv[1:]

def _patch_keras():
    _patch_all_keras_modules(keras, log=set())

def _patch_all_keras_modules(mod, log):
    if mod not in log:
        log.add(mod)
        for name in dir(mod):
            attr = getattr(mod, name)
            if _is_keras_module(attr):
                _patch_all_keras_modules(attr, log)
            elif _is_keras_model(attr):
                _patch_keras_model(attr, log)

def _is_keras_module(x):
    return (isinstance(x, types.ModuleType)
            and x.__name__.startswith("keras."))

def _is_keras_model(x):
    return (isinstance(x, (type, types.ClassType))
            and issubclass(x, keras.engine.training.Model))

def _patch_keras_model(cls, log):
    if cls not in log:
        log.add(cls)
        cls.fit = _fit_wrapper(cls.fit)

def _fit_wrapper(fit0):
    def fit(self, *args, **kw):
        _ensure_tensorboard_cb(kw)
        return fit0(self, *args, **kw)
    return fit

def _ensure_tensorboard_cb(kw):
    callbacks = kw.setdefault("callbacks", [])
    log_dir = "/tmp/keras-run" # TODO provide RUNDIR as arg to script
    tensorboard_cb = _find_tensorboard_cb(callbacks)
    if tensorboard_cb is not None:
        tensorboard_cb.log_dir = log_dir
    else:
        tensorboard_cb = keras.callbacks.TensorBoard(
            log_dir,
            write_graph=True)
        callbacks.append(tensorboard_cb)

def _find_tensorboard_cb(l):
    for cb in l:
        if isinstance(cb, keras.callbacks.TensorBoard):
            return cb
    return None

def _exec_script(script):
    exec(open(script, "r").read())

if __name__ == "__main__":
    main()
