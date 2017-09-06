import json
import logging
import os

import werkzeug
from werkzeug import serving

import guild.app
import guild.project_util
import guild.view

# Manually setup package level access for consistent API usage
werkzeug.serving = serving

DEFAULT_MAX_EPOCHS = 400

####################################################################
# App page handler
####################################################################

class AppPageHandler(object):
    """Use SharedDataMiddleware to serve index.html statically."""

    def __init__(self, paths):
        index_path = guild.app.generated("components", "index.html")
        exports = {
            path: index_path for path in paths
        }
        self.static = werkzeug.wsgi.SharedDataMiddleware(
            _not_found_app, exports)

    def __call__(self, _view, _req, _path):
        return lambda env, start_resp: self.static(env, start_resp)

def _not_found_app(_env, _start_resp):
    _raise_not_found()

####################################################################
# Server
####################################################################

def start(host, port, view, log_level=logging.WARNING):
    _init_logging(log_level)
    server = _init_server(host, port, view)
    server.serve_forever()

def _init_logging(level):
    logger = logging.getLogger("werkzeug")
    logger.setLevel(level)

def _init_server(host, port, view):
    app = _init_app(view)
    return werkzeug.serving.make_server(host, port, app, threaded=True)

####################################################################
# App
####################################################################

def _init_app(view):
    return _apply_static(_base_app(view))

def _base_app(view):
    return _base_app_for_routes(_routes(), view)

def _routes():
    return werkzeug.routing.Map([
        _handler("/data/runs", _handle_runs),
        _handler("/data/series/<path:path>", _handle_series),
        _handler("/data/flags", _handle_flags),
        _handler("/data/attrs", _handle_attrs),
        _handler("/data/output", _handle_output),
        _handler("/data/compare", _handle_compare),
        _handler("/data/sources", _handle_sources),
        _handler("/data/settings", _handle_settings),
        _handler("/data/project", _handle_project),
        _handler("/data/tf/<path:path>", _handle_tf_data),
        _redirect("/", "/train"),
        _handler("/<path:_path>", _app_page_handler())
    ])

def _base_app_for_routes(routes, view):
    def app(env, start_response):
        req = werkzeug.wrappers.Request(env)
        try:
            return _dispatch(req, view, routes)(env, start_response)
        except werkzeug.exceptions.HTTPException as e:
            return _handle_error(e, env, start_response)
    return app

def _redirect(pattern, location):
    return werkzeug.routing.Rule(pattern, redirect_to=location)

def _handler(pattern, endpoint):
    return werkzeug.routing.Rule(pattern, endpoint=endpoint)

def _dispatch(req, view, routes):
    handler, values = _find_handler(req, routes)
    return handler(view, req, **values)

def _find_handler(req, routes):
    return routes.bind_to_environ(req.environ).match()

def _handle_error(error, env, start_response):
    return error(env, start_response)

def _apply_static(app):
    routes = {
        "/assets": os.path.join(guild.app.home(), "assets")
    }
    return werkzeug.wsgi.SharedDataMiddleware(app, routes)

####################################################################
# Helpers
####################################################################

def _run_id(req):
    run_id = req.args.get("run")
    if run_id:
        try:
            return int(run_id)
        except ValueError:
            _raise_bad_request("run must be a valid run ID")
    else:
        return None

def _raise_bad_request(msg):
    raise werkzeug.exceptions.BadRequest(msg)

def _raise_not_found(msg=""):
    raise werkzeug.exceptions.NotFound(msg)

def _json_resp(encoded_json):
    resp = werkzeug.wrappers.Response(encoded_json)
    resp.content_type = "application/json"
    return resp

def _view_lookup(fun, *args):
    try:
        result = fun(*args)
    except LookupError:
        _raise_not_found()
    else:
        return _json_resp(json.dumps(result))

####################################################################
# Handlers
####################################################################

def _handle_runs(view, _req):
    return _json_resp(json.dumps(view.formatted_runs()))

def _handle_series(view, req, path):
    series_pattern = _series_pattern_for_path(path)
    max_epochs = _max_epochs_for_params(req.args)
    return _view_lookup(view.series, _run_id(req), series_pattern, max_epochs)

def _series_pattern_for_path(path):
    return path

def _max_epochs_for_params(params):
    max_str = params.get("max_epochs")
    if not max_str:
        return DEFAULT_MAX_EPOCHS
    elif max_str == "all":
        return None
    else:
        try:
            return int(max_str)
        except ValueError:
            _raise_bad_request("max_epochs must be 'all' or an integer")

def _handle_flags(view, req):
    return _view_lookup(view.flags, _run_id(req))

def _handle_attrs(view, req):
    return _view_lookup(view.attrs, _run_id(req))

def _handle_output(_view, _req):
    _raise_bad_request("TODO: handle output")

def _handle_compare(view, req):
    run_ids = _run_ids_for_params(req.args)
    sources = _sources_for_params(req.args)
    try:
        return _view_lookup(view.compare, run_ids, sources)
    except ValueError as e:
        _raise_bad_request("invalid source: %s" % e.args[0])

def _sources_for_params(params):
    sources = params.get("sources", "").split(",")
    return sorted(set(sources))

def _run_ids_for_params(params):
    raw = params.get("runs")
    if raw is None:
        return None
    return [_run_id_from_string(s) for s in raw.split(",")]

def _run_id_from_string(id_str):
    try:
        return int(id_str)
    except ValueError:
        _raise_bad_request("invalid run_id: %s" % id_str)

def _handle_sources(view, _req):
    return _view_lookup(view.sources)

def _handle_settings(view, _req):
    return _json_resp(json.dumps(view.settings))

def _handle_project(view, _req):
    project = view.resolved_project()
    return _json_resp(guild.project_util.project_to_json(project))

def _handle_tf_data(view, _req, path):
    try:
        status, headers, body = view.tf_data(path)
    except guild.view.NotSupportedError:
        pass
    else:
        status_str = "%i %s" % status
        return werkzeug.wrappers.Response(body, status_str, headers)

def _app_page_handler():
    paths = [
        "/train",
    ]
    return AppPageHandler(paths)
