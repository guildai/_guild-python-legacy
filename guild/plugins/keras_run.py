import argparse
import json
import numbers
import os
import types

try:
    import keras
except ImportError:
    keras = None

FLAGS = None

def main():
    _check_keras()
    _init_flags()
    _patch_keras()
    _exec_script()

def _check_keras():
    if keras is None:
        raise AssertionError("keras is not installed")

def _init_flags():
    global FLAGS
    p = argparse.ArgumentParser()
    p.add_argument("script", help="Keras script to execute")
    p.add_argument("opdir", help="Guild opdir")
    p.add_argument("--epochs", type=int, help="training epochs")
    p.add_argument("--batch-size", type=int, help="training batch size")
    FLAGS, rest = p.parse_known_args()
    FLAGS.rest_args = rest

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
        _patch_fit_kw(kw)
        _ensure_tensorboard_cb(kw)
        return fit0(self, *args, **kw)
    return fit

def _patch_fit_kw(kw):
    for name in kw:
        val = getattr(FLAGS, name, None)
        if val is not None:
            kw[name] = val

def _ensure_tensorboard_cb(kw):
    callbacks = kw.setdefault("callbacks", [])
    cb = _find_tensorboard_cb(callbacks)
    if cb is None:
        cb = keras.callbacks.TensorBoard(write_graph=True)
        callbacks.append(cb)
    if not _is_wrapped(cb):
        _wrap_tensorboard_cb(cb)

def _find_tensorboard_cb(l):
    for cb in l:
        if isinstance(cb, keras.callbacks.TensorBoard):
            return cb
    return None

def _is_wrapped(cb):
    return getattr(cb, "__GUILD_WRAPPED__", False)

def _wrap_tensorboard_cb(cb):
    cb.log_dir = FLAGS.opdir
    cb.set_params = types.MethodType(_set_params_wrapper(cb), cb)
    cb.__GUILD_WRAPPED__ = True

def _set_params_wrapper(cb):
    set_params0 = cb.set_params
    def set_params(_self, params):
        _write_run_flags(params)
        return set_params0(params)
    return set_params

def _write_run_flags(params):
    flags_path = os.path.join(FLAGS.opdir, "guild.d", "flags.json")
    json.dump(_flags_for_params(params), open(flags_path, "w"))

def _flags_for_params(params):
    return {
        key: val
        for key, val in params.items()
        if isinstance(val, (basestring, numbers.Number, bool))
    }

def _acc_field():
    return {
        "color": "teal-600",
        "format": "0.00%",
        "icon": "accuracy",
        "label": "Training Accuracy",
        "reduce": "last",
        "source": "series/tf/acc"
    }

def _epochs_field():
    return {
        "color": "blue-700",
        "format": "0,0",
        "icon": "steps",
        "label": "Epochs",
        "reduce": "steps1",
        "source": "series/tf/loss"
    }

def _time_field():
    return {
        "color": "yellow-700",
        "format": "0:00:00",
        "icon": "time",
        "label": "Time",
        "reduce": "duration",
        "source": "series/tf/loss"
    }

def _exec_script():
    # pylint: disable=exec-used
    exec(open(FLAGS.script, "r").read())

if __name__ == "__main__":
    main()
