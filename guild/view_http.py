import os
import sys

import werkzeug

# Manually setup package level access for consistent API usage
from werkzeug import serving
werkzeug.serving = serving

import guild

def start(host, port, config):
    server = _init_server(host, port, config)
    sys.stdout.write("Guild View running on port %i\n" % port)
    server.serve_forever()

def _init_server(host, port, config):
    app = _init_app(config)
    return werkzeug.serving.make_server(host, port, app, threaded=True)

def _init_app(config):
    return _apply_static(_base_app(config))

def _base_app(config):
    Rule = werkzeug.routing.Rule
    routes = werkzeug.routing.Map([
        Rule("/data/runs", endpoint=_handle_runs),
        Rule("/data/series/<path:path>", endpoint=_handle_series),
        Rule("/data/flags", endpoint=_handle_flags),
        Rule("/data/attrs", endpoint=_handle_attrs),
        Rule("/data/output", endpoint=_handle_output),
        Rule("/data/compare", endpoint=_handle_compare),
        Rule("/data/sources", endpoint=_handle_sources),
        Rule("/data/settings", endpoint=_handle_settings),
        Rule("/data/project", endpoint=_handle_project),
        Rule("/data/tf/<path:path>", endpoint=_handle_tf_data),
        Rule("/", redirect_to="/train"),
        Rule("/<path:path>", endpoint=_handle_app_page)
    ])
    def app(env, start_response):
        req = werkzeug.wrappers.Request(env)
        try:
            return _dispatch(req, routes)(env, start_response)
        except werkzeug.exceptions.HTTPException as e:
            return _handle_error(e, env, start_response)
    return app

def _dispatch(req, routes):
    handler, values = _find_handler(req, routes)
    return handler(req, **values)

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

def _handle_app_page(req, path):
    return werkzeug.wrappers.Response("TODO: handle app page '%s'\n" % path)

def _handle_runs(req):
    return werkzeug.wrappers.Response("TODO: handle runs\n")

def _handle_series(req, path):
    return werkzeug.wrappers.Response("TODO: handle series %s\n" % path)

def _handle_flags(req):
    return werkzeug.wrappers.Response("TODO: handle flags\n")

def _handle_attrs(req):
    return werkzeug.wrappers.Response("TODO: handle attrs\n")

def _handle_output(req):
    return werkzeug.wrappers.Response("TODO: handle output\n")

def _handle_compare(req):
    return werkzeug.wrappers.Response("TODO: handle compare\n")

def _handle_sources(req):
    return werkzeug.wrappers.Response("TODO: handle sources\n")

def _handle_settings(req):
    return werkzeug.wrappers.Response("TODO: handle settings\n")

def _handle_project(req):
    return werkzeug.wrappers.Response("TODO: handle project\n")

def _handle_tf_data(req, path):
    return werkzeug.wrappers.Response("TODO: handle tf data '%s'\n" % path)
