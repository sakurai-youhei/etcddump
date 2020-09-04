'''
Created on 2020/09/04

@author: sakurai
'''
from codecs import open
from json import load
from os import environ
from os import stat
from unittest import main
from unittest import skipIf
from unittest import TestCase

from etcd import Client

from etcddump.operations import Dumper
from etcddump.tests.etcdwrap import EtcdWrap
from etcddump.tests.test_basic import tempfile


if "ETCDDUMP_ETCD" in environ:
    EtcdWrap._etcd_ = environ["ETCDDUMP_ETCD"]


class DumperTest(TestCase):
    @skipIf(not EtcdWrap.is_available(), "No etcd command available")
    def test_order_of_entries_on_dump(self):
        backup = tempfile()

        with EtcdWrap() as etcd:
            try:
                client = Client(etcd.host, etcd.port)
                for i in range(10):
                    client.write("/{}".format(i), i ** i)
                Dumper(etcd.client_urls[0]).dump(filename=backup)
            finally:
                etcd.terminate()

        self.assertGreater(stat(backup).st_size, 0)
        with open(backup, encoding="utf-8") as fp:
            lastindex = 0
            for i, entry in enumerate(load(fp)):
                self.assertEqual(entry["key"], "/{}".format(i))
                self.assertEqual(entry["value"], str(i ** i))
                self.assertTrue(i <= lastindex < entry["index"])
                lastindex = entry["index"]


if __name__ == "__main__":
    main()
