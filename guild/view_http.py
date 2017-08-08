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
    Rule = werkzeug.routing.Rule
    routes = werkzeug.routing.Map([
        Rule('/data', endpoint='_handle_data')
    ])
    def app(env, start_response):
        req = werkzeug.wrappers.Request(env)
        try:
            return _dispatch(req, routes)(env, start_response)
        except werkzeug.exceptions.HTTPException as e:
            return e
    return app

def _dispatch(req, routes):
    handler, values = _find_handler(req, routes)
    return handler(req, values)

def _find_handler(req, routes):
    endpoint, values = routes.bind_to_environ(req.environ).match()
    return getattr(guild.view_http, endpoint), values

def _handle_data(req, values):
    return werkzeug.wrappers.Response("Yo hello\n")
