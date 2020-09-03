etcddump
========

A dump &amp; load tool for etcd, which respects all key properties (including indexes) of public keys.

Fork from original, fixed utf-8 encoded keys and values.

Installation
------------

You can install etcddump from sources by cloning this repository and run

.. code:: bash

    $ sudo python setup.py install
-
Alternatively you may use pip:

.. code:: bash

    $ sudo pip install etcddump



After you've installed etcddump, the program ``etcdumper`` will be available on your system

The only dependency of ``etcddump`` is  `python-ectd <https://github.com/jplana/python-etcd>`_ version 0.3.0 or later.

Portable pyz package
--------------------

You can build portable package with all dependencies embedded by running ``pyzbuild.cmd`` on Windows.

The ``etcddump.pyz`` package can run on not only Windows but also other operating systems like Linux.

.. code:: bash

    $ chmod +x etcddump.pyz
    $ ./etcddump.pyz --help

The script for packaging is written & added by `Youhei Sakurai <https://github.com/sakurai-youhei>`.

Usage
-----

Usage is really simple and has been thought so that it resembles how most dumper programs work.

.. code:: bash

    # dump to stdout
    etcdumper dump https://etcd.example.com:4001

    # dump to file
    etcdumper --file dump.json dump https://etcd.example.com:4001

    # restore from file
    etcdumper --file dump.json restore http://localhost:4001

    # try to maintain the same indexes as in the original cluster
    etcdumper --file dump.json --preserve-indexes restore https://etcd.example.com:4001

    #dump & restore in one command using pipes
    etcdumper dump https://etcd.example.com:4001 | etcdumper restore http://localhost:4001
