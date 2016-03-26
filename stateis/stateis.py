"""
stateis.py

"""


import argparse
import fabric
from fabric.api import *
from prettytable import PrettyTable


def stats():
    with hide("running", "stdout", "stderr", "status"):
        hostname = get_hostname()
        diskinfo = get_diskinfo()
        kernel = get_kernel()

    stats_table = build_stats_table(hostname, kernel)
    print("\n")
    print(stats_table)
    print("\n")

    fabric.network.disconnect_all()

    return None


@runs_once
def build_stats_table(hostname, kernel):
    table_headers = [
        "Hostname", "Kernel Version"
    ]

    stats_table = PrettyTable(table_headers)
    stats_table.align["Hostname"] = "l"
    stats_table.align["Kernel Version"] = "r"
    stats_table.padding_width = 1
    stats_table.add_row([hostname,kernel])

    return stats_table


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


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output_type", help="Specify the type of output " + \
                    "you'd like the results to be", type=str)
    args = parser.parse_args()
    if args.output_type == "table":
        execute(stats)
