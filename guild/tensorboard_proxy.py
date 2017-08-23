import http.client
import os
import subprocess

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
            ["tensorboard", "--logdir", self.logdir, "--port", str(self.port)],
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
            self._conn = http.client.HTTPConnection("localhost", self.port)
        return self._conn

if __name__ == "__main__":
    proxy = TensorBoardProxy(
        "tensorboard",
        "/home/garrett/SCM/guild-examples/mnist2/runs",
        6006)
    proxy.start()
    print(proxy.data("runs"))
    print(proxy.data("runs"))
    proxy.stop()
