"""
stateis.py

"""


import argparse
import fabric
from fabric.api import *
from prettytable import PrettyTable


env.user = ""
env.password = ""
env.hosts = []


def stats():
    """"""
    stats = []

    with hide("running", "stdout", "stderr", "status"):
        stats.append(get_hostname())
        #stats.append(diskinfo = get_diskinfo()
        stats.append(get_kernel())

    print(stats)
    fabric.network.disconnect_all()

    return stats


@runs_once
def build_stats_table(stats_out):
    """"""
    table_headers = [
        "IP Address", "Hostname", "Kernel"
    ]

    stats_table = PrettyTable(table_headers)
    stats_table.align["IP Address"] = "l"
    stats_table.align["Hostname"] = "l"
    stats_table.align["Kernel"] = "r"
    stats_table.padding_width = 1

    for key in stats_out:
        vm_stats = [key]
        for item in stats_out[key]:
            vm_stats.append(item)
        stats_table.add_row(vm_stats)

    return stats_table


@runs_once
def print_stats_table(stats_table):
    """"""
    print("\n")
    print(stats_table)
    print("\n")

    return None


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
    """"""
    parser = argparse.ArgumentParser()
    parser.add_argument("output_type", help="Specify the type of output " + \
                    "you'd like the results to be", type=str)
    args = parser.parse_args()
    
    if args.output_type == "table":
        stats_out = execute(stats)
        print(stats_out)
        print_stats_table(build_stats_table(stats_out))
