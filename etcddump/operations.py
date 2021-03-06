from codecs import open
import json
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import sys

import etcd


class BaseOperations(object):

    def __init__(self, url='http://localhost:4001'):
        self.get_client(url)

    def get_client(self, url, ca_cert=None, cert=None):
        parsed = urlparse(url)
        (h, p) = parsed.netloc.split(':')
        self.client = etcd.Client(host=h,
                                  port=int(p),
                                  protocol=parsed.scheme,
                                  allow_reconnect=False,
                                  ca_cert=ca_cert,
                                  cert=cert)

    def entry_from_result(self, entry):
        return {
            'key': entry.key,
            'value': entry.value,
            'ttl': entry.ttl,
            'dir': entry.dir,
            'index': entry.modifiedIndex
        }


class Dumper(BaseOperations):
    def walk(self, key):
        for entry in self.client.read(key, recursive=True).children:
            if entry.key:
                yield entry.modifiedIndex, self.entry_from_result(entry)

    def dump(self, filename=None):
        dumplist = [entry for _, entry in sorted(self.walk('/'))]
        if filename:
            with open(filename, 'w', encoding="utf-8") as f:
                json.dump(dumplist, f)
        else:
            print(json.dumps(dumplist))


class Restorer(BaseOperations):
    def fake_entry(self):
        return {
            'key': '/_etcd_dumper/bogus',
            'value': 'bogus',
            'ttl': 1,
            'dir': False
        }

    def restore(self, filename=None, preserve_indexes=False):
        if filename:
            with open(filename, 'r', encoding="utf-8") as f:
                data = json.load(f)
        else:
            with sys.stdin as f:
                data = json.load(f)

        lastidx = 0

        for entry in data:
            if preserve_indexes:
                self.fillin(entry['index'], lastidx)

            r = self.write(entry)
            lastidx = r.modifiedIndex

    def fillin(self, idx, lastidx):
        while (idx < (lastidx - 1)):
            r = self.write(self.fake_entry())
            idx = r.modifiedIndex
        return idx

    def escape(self, key, value, **kwargs):
        if not isinstance(key, str):
            key = key.encode('utf-8')
        if not kwargs.get("dir"):
            value = value.encode('utf-8')
        escaped = dict(key=key, value=value)
        escaped.update(kwargs)
        return escaped

    def write(self, entry):
        return self.client.write(**self.escape(**entry))
