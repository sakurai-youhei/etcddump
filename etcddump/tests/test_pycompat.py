'''
Created on 2020/09/03

@author: sakurai
'''
from unittest import main
from unittest import TestCase


class PyCompatTest(TestCase):
    def test_import(self):
        __import__("etcddump")
        __import__("etcddump.cli")
        __import__("etcddump.operations")


if __name__ == "__main__":
    main()
