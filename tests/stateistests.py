"""
stateistests.py

"""


import unittest
import fabric
from fabric import *


class StateIsTest(unittest.TestCase):
    """"""
    
    def setUp(self):
        """"""
        self.hostname = ""
        self.diskinfo = []
        self.kernel = ""
        self.ifconfig = []


    def test_get_hostname(self):
        """"""
        self.assertEqual(self.hostname, get_hostname())


    def test_get_diskinfo(self):
        """"""
        self.assertEqual(self.diskinfo, get_diskinfo())

    
    def test_get_kernel(self):
        """"""
        self.assertEqual(self.kernel, get_kernel())


    def test_get_ifconfig(self):
        """"""
        self.assertEqual(self.ifconfig, get_ifconfig())


if __name__=="__main__":
    unittest.main()
