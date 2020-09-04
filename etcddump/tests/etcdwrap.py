'''
Created on 2020/09/03

@author: sakurai
'''
from atexit import register
from contextlib import closing
from shutil import rmtree
from socket import AF_INET
from socket import SO_REUSEADDR
from socket import SOCK_STREAM
from socket import socket
from socket import SOL_SOCKET
from subprocess import check_call
try:
    from subprocess import DEVNULL
except ImportError:
    from subprocess import PIPE as DEVNULL
from subprocess import Popen
from tempfile import mkdtemp
from time import sleep


def find_free_port():
    """https://stackoverflow.com/a/45690594"""
    with closing(socket(AF_INET, SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        return s.getsockname()[1]


class EtcdWrap(Popen):
    _etcd_ = "etcd"

    def __init__(self, **kwargs):
        self.host = "localhost"
        self.port = find_free_port()
        self.client_urls = ["http://{}:{}".format(self.host, self.port)]
        self.peer_urls = ["http://{}:{}".format(self.host, find_free_port())]

        tempdir = mkdtemp()
        register(rmtree, tempdir)
        kwargs["args"] = [EtcdWrap._etcd_,
                          "--debug",
                          "--data-dir", tempdir,
                          "--listen-client-urls",
                          ",".join(self.client_urls),
                          "--advertise-client-urls",
                          ",".join(self.client_urls),
                          "--listen-peer-urls",
                          ",".join(self.peer_urls)]
        kwargs["stderr"] = DEVNULL
        Popen.__init__(self, **kwargs)

    @staticmethod
    def is_available():
        try:
            return check_call([EtcdWrap._etcd_, "--version"],
                              stdout=DEVNULL) == 0
        except Exception:
            return False

    def __enter__(self):
        sleep(1)
        return self

    def __exit__(self, exc_type, value, traceback):
        if exc_type == KeyboardInterrupt:
            return  # resume the KeyboardInterrupt
        self.wait()
