import ast
import glob
import os

import guild.log

def try_project(args):
    script = _find_keras_script(args)
    if script:
        return _project_for_script(script)
    else:
        return None

def _find_keras_script(args):
    scripts = _keras_scripts(args)
    if len(scripts) == 1:
        return scripts[0]
    else:
        for script in scripts:
            if _script_name(script) == args.model:
                return script
        return None

def _keras_scripts(args):
    keras_scripts = []
    for script in _python_scripts(args):
        debug_parts = ["[keras-plugin] testing script '%s':" % script]
        is_script = _is_keras_script(script, debug_parts)
        _log_debug_parts(debug_parts)
        if is_script:
            keras_scripts.append(script)
    return keras_scripts

def _log_debug_parts(parts):
    guild.log.debug(" ".join(parts))

def _python_scripts(args):
    return glob.glob(os.path.join(args.project_dir, "*.py"))

def _is_keras_script(script, debug_parts):
    try:
        parsed = ast.parse(script)
    except SyntaxError:
        debug_parts.append("syntax error, skipping")
        return False
    else:
        return _is_keras_ast(parsed, debug_parts)

def _is_keras_ast(parsed, debug_parts):
    conditions = [
        (_imports_keras_condition, "imports keras"),
        (_calls_fit_condition, "calls fit")
    ]
    return _ast_meets_conditions(parsed, conditions, debug_parts)

def _ast_meets_conditions(parsed, conditions, debug_parts):
    working = list(conditions)
    for node in ast.walk(parsed):
        for condition in working:
            condition_fun, condition_name = condition
            condition_met = condition_fun(node)
            debug_parts.append("%s=%s" % (condition_name, condition_met))
            if condition_met:
                working.remove(condition)
        if len(conditions) == 0:
            debug_parts.append("(assuming is keras script)")
            return True
    debug_parts.append("(assuming is not keras script)")
    return False

def _imports_keras_condition(_node):
    return False

def _calls_fit_condition(_node):
    return False

def _script_name(script):
    name, _ext = os.path.basename(os.path.splitext(script))
    return name

def _project_for_script(script):
    data = {
    }
    return guild.project.Project(data, "<generated from %s>" % script)
