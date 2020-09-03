# -*- coding: utf-8 -*-

'''
Created on 2020/09/03

@author: sakurai
'''

from atexit import register
from os import environ
from os import remove
from os import stat
try:
    from random import choices
except ImportError:
    from random import choice

    def choices(seq, k=1):
        r = []
        for _ in range(k):
            r.append(choice(seq))
        return r
from string import printable
from tempfile import NamedTemporaryFile
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
from unittest import main
from unittest import skipIf
from unittest import TestCase

from etcd import Client

from etcddump.operations import Dumper
from etcddump.operations import Restorer
from etcddump.tests.etcdwrap import EtcdWrap


if "ETCDDUMP_ETCD" in environ:
    EtcdWrap._etcd_ = environ["ETCDDUMP_ETCD"]


class BaseTestOnPy3(TestCase):

    def _randompath(self, length):
        return urlparse("///" + "".join(choices(printable, k=length - 1))).path

    def _testdata(self, length, count):
        with EtcdWrap() as etcd:
            try:
                client = Client(etcd.host, etcd.port)
                while count:
                    path = self._randompath(length)
                    data = "".join(choices(printable, k=length))
                    try:
                        client.write(path, data)
                        if data == client.read(path):
                            yield path, data
                    except Exception:
                        pass
                    count -= 1
            finally:
                etcd.terminate()

    def _tempfile(self):
        with NamedTemporaryFile(delete=False) as fp:
            register(remove, fp.name)
            return fp.name

    def assertRestration(self, backup, expects, msg=None):
        with EtcdWrap() as etcd:
            try:
                Restorer(etcd.listen_client_urls[0]).restore(filename=backup)
                client = Client(etcd.host, etcd.port)
                for key in expects:
                    self.assertEqual(client.read(key).value, expects[key], msg)
            finally:
                etcd.terminate()

    @skipIf(not EtcdWrap.is_available(), "No etcd command available")
    def test_empty_backup_restore(self):
        backup = self._tempfile()

        with EtcdWrap() as etcd:
            try:
                Dumper(etcd.listen_client_urls[0]).dump(filename=backup)
            finally:
                etcd.terminate()

        self.assertGreater(stat(backup).st_size, 0)
        self.assertRestration(backup, {})

    @skipIf(not EtcdWrap.is_available(), "No etcd command available")
    def test_a_few_dirs_backup_restore(self):
        backup = self._tempfile()

        with EtcdWrap() as etcd:
            try:
                client = Client(etcd.host, etcd.port)
                client.write("/a", None, dir=True)
                client.write("/b", None, dir=True)
                client.write("/c", None, dir=True)
                Dumper(etcd.listen_client_urls[0]).dump(filename=backup)
            finally:
                etcd.terminate()

        self.assertGreater(stat(backup).st_size, 0)
        self.assertRestration(backup, {"/a": None, "/b": None, "/c": None})

    @skipIf(not EtcdWrap.is_available(), "No etcd command available")
    def test_unicode_backup_restore(self):
        backup = self._tempfile()

        with EtcdWrap() as etcd:
            try:
                client = Client(etcd.host, etcd.port)
                if isinstance(u"", str):
                    client.write(u"/パス", u"/データ")
                else:
                    client.write(u"/パス".encode("utf-8"),
                                 u"/データ".encode("utf-8"))
                Dumper(etcd.listen_client_urls[0]).dump(filename=backup)
            finally:
                etcd.terminate()

        self.assertGreater(stat(backup).st_size, 0)
        self.assertRestration(backup, {u"/パス": u"/データ"})

    @skipIf(not EtcdWrap.is_available(), "No etcd command available")
    def test_fuzzy_backup_restore(self):
        data = dict(self._testdata(256, 100))
        backup = self._tempfile()

        with EtcdWrap() as etcd:
            try:
                client = Client(etcd.host, etcd.port)
                for key in data.copy():
                    client.write(key, data[key])
                Dumper(etcd.listen_client_urls[0]).dump(filename=backup)
            finally:
                etcd.terminate()

        self.assertGreater(stat(backup).st_size, 0)
        self.assertRestration(backup, data)


if __name__ == "__main__":
    main()
