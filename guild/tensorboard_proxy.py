# pylint: disable=wrong-import-order

import os
import subprocess

try:
    import httplib
except ImportError:
    import http.client
    httplib = http.client

import guild.log

class TensorBoardProxy(object):

    def __init__(self, tensorboard, logdir, port):
        self.tensorboard = tensorboard
        self.logdir = logdir
        self.port = port
        self._proc = None
        self._conn = None

    def running(self):
        return self._proc is not None and self._proc.poll() is None

    def start(self):
        if self.running():
            raise RuntimeError("proxy is running")
        guild.log.debug("starting TensorBoard proxy on port %s", self.port)
        devnull = open(os.devnull, "w")
        self._proc = subprocess.Popen(
            [_tensorboard_bin(), "--logdir", self.logdir, "--port", str(self.port)],
            stdout=devnull,
            stderr=devnull)

    def stop(self):
        guild.log.debug("stopping TensorBoard proxy")
        if self._proc is not None:
            self._proc.terminate()
        self._proc = None

    def data(self, path):
        c = self._connection()
        guild.log.debug("tensorboard data request: %s", path)
        c.request("GET", "/data/%s" % path)
        resp = c.getresponse()
        return ((resp.status, resp.reason), resp.getheaders(), resp.read())

    def _connection(self):
        if self._conn is None:
            self._conn = httplib.HTTPConnection("localhost", self.port)
        return self._conn

def _tensorboard_bin():
    return guild.app.external(
        "org_tensorflow_tensorboard/tensorboard/tensorboard")
