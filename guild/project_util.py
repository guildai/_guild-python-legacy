import copy
import json
import os

import guild.project
import guild.util

def runs_dir_for_project(project):
    runs_dir = guild.util.find_apply(
        [lambda: _project_runs_dir(project),
         lambda: _default_runs_dir()])
    return os.path.abspath(os.path.join(project.dir, runs_dir))

def runs_dir_for_project_dir(project_dir):
    runs_dir = _default_runs_dir()
    return os.path.abspath(os.path.join(project_dir, runs_dir))

def _project_runs_dir(project):
    return project.attr("runs_dir")

def _default_runs_dir():
    return "runs"

def project_to_json(project):
    return json.dumps(project.data)

def apply_project_include(include_project, target_project):
    applied_data = {}
    _apply_include_acc(include_project.data, applied_data)
    _apply_include_acc(target_project.data, applied_data)
    return guild.project.copy_with_new_data(target_project, applied_data)

def _apply_include_acc(data, acc):
    if isinstance(data, dict) and isinstance(acc, dict):
        _apply_dict_acc(data, acc)
    elif isinstance(data, list) and isinstance(acc, list):
        _apply_list_acc(data, acc)

def _apply_dict_acc(data, acc):
    for key0, val in data.items():
        merge_key = key0.endswith("+")
        key = key0[:-1] if merge_key else key0
        if merge_key and key in acc:
            _apply_include_acc(val, acc[key])
        else:
            acc[key] = _deep_copy_normalize_keys(val)

def _deep_copy_normalize_keys(x):
    if isinstance(x, dict):
        x_copy = {}
        for key, val in x.items():
            if key.endswith("+"):
                key = key[:-1]
            x_copy[key] = _deep_copy_normalize_keys(val)
        return x_copy
    else:
        return copy.deepcopy(x)

def _apply_list_acc(data, acc):
    acc.extend(data)

def resolve_extends(project):
    templates = _project_templates(project)
    resolved_data = copy.deepcopy(project.data)
    _apply_extends(resolved_data, templates)
    return guild.project.copy_with_new_data(project, resolved_data)

def _project_templates(project):
    templates = {}
    _acc_templates(project.data, [], templates)
    return templates

def _acc_templates(item, path, acc):
    for item_keys, item in _iter_template_item(item):
        for item_key in item_keys:
            item_path = path + [item_key]
            if isinstance(item, dict):
                acc[item_key] = item
                acc[_template_key(item_path)] = item
            _acc_templates(item, item_path, acc)

def _iter_template_item(item):
    if isinstance(item, list):
        return _iter_template_list(item)
    elif isinstance(item, dict):
        return _iter_template_dict(item)
    else:
        return []

def _iter_template_list(l):
    for index, item in enumerate(l):
        if isinstance(item, dict) and "id" in item:
            yield [str(index), item["id"]], item
        else:
            yield [str(index)], item

def _iter_template_dict(d):
    for key, item in d.items():
        if isinstance(item, dict) and "id" in item:
            yield [key, item["id"]], item
        else:
            yield [key], item

def _template_key(path):
    return "/".join(path)

def _apply_extends(data, templates):
    if isinstance(data, list):
        _apply_extends_list(data, templates)
    elif isinstance(data, dict):
        _apply_extends_dict(data, templates)

def _apply_extends_list(l, templates):
    for item in l:
        _apply_extends(item, templates)

def _apply_extends_dict(d, templates):
    _apply_extends_item(d, templates)
    for item in d.values():
        _apply_extends(item, templates)

def _apply_extends_item(item, templates):
    extends_ref = item.get("extends")
    if extends_ref:
        del item["extends"] # delete first to prevent cycles
        extended = templates.get(extends_ref)
        if extended:
            assert isinstance(extended, dict)
            _apply_extends_dict(extended, templates)
            _apply_extended_attrs(extended, item)

def _apply_extended_attrs(attrs, target):
    for key, val in attrs.items():
        if key not in target:
            target[key] = val
