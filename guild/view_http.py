import json
import os
import sys

import werkzeug

# Manually setup package level access for consistent API usage
from werkzeug import serving
werkzeug.serving = serving

import guild # pylint: disable=wrong-import-position

####################################################################
# Server
####################################################################

def start(host, port, view):
    server = _init_server(host, port, view)
    sys.stdout.write("Guild View running on port %i\n" % port)
    server.serve_forever()

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
        _handler("/<path:path>", _handle_app_page)
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
        "/assets": os.path.join(guild.app.home(), "assets"),
        "/components": os.path.join(guild.app.home(), "components")
    }
    return werkzeug.wsgi.SharedDataMiddleware(app, routes)

####################################################################
# Response
####################################################################

def _json_resp(val):
    return werkzeug.wrappers.Response(json.dumps(val))

####################################################################
# Handlers
####################################################################

def _handle_app_page(_view, _req, path):
    return werkzeug.wrappers.Response("TODO: handle app page '%s'\n" % path)

def _handle_runs(view, _req):
    return _json_resp(view.runs())

def _handle_series(_view, _req, path):
    return werkzeug.wrappers.Response("TODO: handle series %s\n" % path)

def _handle_flags(_view, _req):
    return werkzeug.wrappers.Response("TODO: handle flags\n")

def _handle_attrs(_view, _req):
    return werkzeug.wrappers.Response("TODO: handle attrs\n")

def _handle_output(_view, _req):
    return werkzeug.wrappers.Response("TODO: handle output\n")

def _handle_compare(_view, _req):
    return werkzeug.wrappers.Response("TODO: handle compare\n")

def _handle_sources(_view, _req):
    return werkzeug.wrappers.Response("TODO: handle sources\n")

def _handle_settings(_view, _req):
    return werkzeug.wrappers.Response("TODO: handle settings\n")

def _handle_project(_view, _req):
    return werkzeug.wrappers.Response("TODO: handle project\n")

def _handle_tf_data(_view, _req, path):
    return werkzeug.wrappers.Response("TODO: handle tf data '%s'\n" % path)
