import os
import subprocess

import guild.log
import guild.task_support

# Defer time consuming imports until 'start'
event_multiplexer = None
event_accumulator = None

event_loaders = {}

DEFAULT_INTERVAL = 5 # seconds

def start(op, stop, interval=DEFAULT_INTERVAL):
    global event_multiplexer
    global event_accumulator
    # pylint: disable=redefined-outer-name,import-error
    from tensorboard.backend.event_processing import event_multiplexer
    from tensorboard.backend.event_processing import event_accumulator
    guild.task_support.loop((_log_events, [op]), interval, stop)

def _log_events(op):
    scalars = _latest_scalars(op.opdir)
    guild.log.debug("tensorflow scalars: %s", scalars)
    op.db.log_series_values(scalars.items())

def _latest_scalars(opdir):
    _refresh_event_loaders(opdir)
    _sync_file_system(opdir)
    data = {}
    for run, reader in event_loaders.items():
        _add_scalars_from_events(reader.Load(), run, data)
    return data

def _refresh_event_loaders(opdir):
    for subdir in event_multiplexer.GetLogdirSubdirectories(opdir):
        name = os.path.relpath(subdir, opdir)
        if name not in event_loaders:
            event_loaders[name] = _init_event_loader(subdir)

def _init_event_loader(path):
    # pylint: disable=protected-access
    return event_accumulator._GeneratorFromPath(path)

def _add_scalars_from_events(events, run, data):
    for event in events:
        if event.HasField("summary"):
            _add_scalars_from_summary(event.summary.value, run, event, data)

def _add_scalars_from_summary(summary, run, event, data):
    for value in summary:
        if value.HasField("simple_value"):
            _add_scalar(
                run, value.tag, event.wall_time, event.step,
                value.simple_value, data)

def _add_scalar(run, tag, time, step, value, data):
    vals = data.setdefault(_tf_tag_path(run, tag), [])
    vals.append([int(time * 1000), step, _legal_json(value)])

def _tf_tag_path(run, tag):
    if run and run != ".":
        return "tf/" + run + "/" + tag
    else:
        return "tf/" + tag

def _legal_json(val):
    if val != val: # test for float('nan')
        return None
    else:
        return val

def _sync_file_system(opdir):
    try:
        # Try syncing opdir file system (may fail on some
        # versions of sync)
        subprocess.check_call(
            ["sync", "-f", opdir], stderr=open(os.devnull, 'w'))
    except subprocess.CalledProcessError:
        # Fall back on older version of sync without args
        try:
            subprocess.check_call(["sync"])
        except subprocess.CalledProcessError:
            guild.log.exception("syncing file system")
