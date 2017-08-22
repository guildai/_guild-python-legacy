import ast
import glob
import os

import guild.log

###################################################################
# Keras project
###################################################################

class KerasProject(guild.project.Project):

    def __init__(self, scripts, project_dir):
        if len(scripts) == 0:
            raise RuntimeError("Keras project requires at least one script")
        self._scripts = scripts
        data = _project_data_for_scripts(scripts)
        super(KerasProject, self).__init__(
            data,
            None,
            project_dir,
            "zero-config generated Keras project")

    def reload(self):
        self.data = _project_data_for_scripts(self._scripts)

def _project_data_for_scripts(scripts):
    return {
        "models": {
            _script_name(script): _script_model_data(script)
            for script in scripts
        },
        "views": {
            "train": {
                "scope": "run",
                "content": [
                    "keras-fields"
                ],
                "sidebar": [
                    "flags",
                    "attrs"
                ]
            }
        },
        "components+": {
            "keras-fields": {
                "element": "guild-fields",
                "foo-config": 123
            }
        }
    }

def _script_name(script):
    name, _ext = os.path.splitext(os.path.basename(script))
    return name

def _script_model_data(script):
    data = {
        "train": _script_train_spec(script)
    }
    _apply_flags_for_script(script, data)
    return data

def _script_train_spec(script):
    args = [_keras_run_path(), script, "$RUNDIR"]
    return " ".join([_quote_arg(arg) for arg in args])

def _quote_arg(arg):
    return arg if arg.find(" ") == -1 else '"%s"' % arg

def _keras_run_path():
    this_dir = os.path.dirname(__file__)
    return os.path.join(this_dir, "keras_run.py")

def _apply_flags_for_script(script, data):
    flags = _script_flags(script)
    if flags:
        data["flags"] = flags

def _script_flags(_script):
    # Currently not inferring flags from script
    return {}

###################################################################
# Plugin API: try project
###################################################################

def try_project(args):
    scripts = _keras_scripts(args)
    if scripts:
        guild.log.debug("%i Keras script(s) found", len(scripts),
                        source="keras-plugin")
        return KerasProject(scripts, args.project_dir)
    else:
        guild.log.debug("no Keras scripts found",
                        source="keras-plugin")
        return None

def _keras_scripts(args):
    keras_scripts = []
    for script in _python_scripts(args):
        debug_parts = ["testing script '%s' -" % script]
        is_script = _is_keras_script(script, debug_parts)
        guild.log.debug(" ".join(debug_parts), source="keras-plugin")
        if is_script:
            keras_scripts.append(script)
    return keras_scripts

def _python_scripts(args):
    return glob.glob(os.path.join(args.project_dir, "*.py"))

def _is_keras_script(script, debug_parts):
    try:
        parsed = ast.parse(open(script, "r").read())
    except SyntaxError as e:
        guild.log.exception("parsing %s" % script)
        debug_parts.append("%s, skipping" % e)
        return False
    else:
        return _is_keras_ast(parsed, debug_parts)

def _is_keras_ast(parsed, debug_parts):
    conditions = [
        (_imports_keras_condition, "imports-keras"),
        (_calls_fit_condition, "calls-fit")
    ]
    return _ast_meets_conditions(parsed, conditions, debug_parts)

def _ast_meets_conditions(parsed, conditions, debug_parts):
    working = list(conditions)
    for node in ast.walk(parsed):
        for condition in working:
            condition_fun, _name = condition
            condition_met = condition_fun(node)
            if condition_met:
                working.remove(condition)
        if len(working) == 0:
            debug_parts.append("appears to be a Keras script")
            return True
    assert len(working) > 0
    debug_parts.append(
        "does not appear to be a Keras script (failed conditions: %s)"
        % ", ".join([name for _, name in working]))
    return False

def _imports_keras_condition(node):
    if (isinstance(node, ast.ImportFrom)
        and _is_keras_module_name(node.module)):
        return True
    elif isinstance(node, ast.Import):
        for name in node.names:
            if (isinstance(name, ast.alias)
                and _is_keras_module_name(name.name)):
                return True
    return False

def _is_keras_module_name(name):
    return name == "keras" or name.startswith("keras.")

def _calls_fit_condition(node):
    if (isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "fit"):
        return True
    return False
