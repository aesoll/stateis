"""
stateis.py

"""

import fabric
from fabric.api import *


def get_hostname():
    """Gets hostname"""
    return str(run("hostname"))


def get_diskinfo():
    """Gets hard disk space information"""
    df_output = run("df -h").split("\n")
    df_list = []

    for i in range(len(df_output)):
         df_list.append(df_output[i])

    return df_list


def get_kernel():
    """Gets kernel information"""
    return str(run("uname -r"))


def get_ifconfig():
    """Gets ifconfig info"""
    ifconfig = run("ifconfig").split("\n")[1]
    address = None
    netmask = None

    return ifconfig


def temp_tests():
    print(get_hostname())
    print(get_diskinfo())
    print(get_kernel())
    print(get_ifconfig())


if __name__=="__main__":
    execute(temp_tests())
