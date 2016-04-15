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
    """
    Main execute to gather server stats and compile them into a list of lists
    """
    stats = []

    with hide("running", "stdout", "stderr", "status"):
        stats.append(get_hostname())
        diskinfo = get_diskinfo()
        stats.append(get_kernel())
        for item in diskinfo:
            stats.append(item)

    fabric.network.disconnect_all()

    return stats


@runs_once
def build_stats_table(stats_out):
    """
    Builds the stats table according to predetermined headers and their
    associated values grabbed by the functions below
    """
    table_headers = [
        "IP Address", "Hostname", "Kernel", "Used GB", "Avail GB", "Perc %"
    ]

    stats_table = PrettyTable(table_headers)
    stats_table.align["IP Address"] = "l"
    stats_table.align["Hostname"] = "l"
    stats_table.align["Kernel"] = "r"
    stats_table.align["Used GB"] = "r"
    stats_table.align["Avail GB"] = "r"
    stats_table.align["Perc %"] = "r"
    stats_table.padding_width = 1

    for key in stats_out:
        vm_stats = [key]
        for item in stats_out[key]:
            vm_stats.append(item)
        stats_table.add_row(vm_stats)

    return stats_table


@runs_once
def print_stats_table(stats_table):
    """
    Prints table created in build_stats_table
    """
    print("\n")
    print(stats_table)
    print("\n")

    return None


def get_hostname():
    """
    Gets hostname
    """
    return str(run("hostname"))


def get_diskinfo():
    """
    Gets hard disk space information
    """
    df_output = run("df -h").split("\n")[1:]

    disk_used = 0
    disk_avail = 0
    disk_percent = 0

    for i in range(len(df_output)):
        df_line_split = df_output[i].split()

        disk_used += _calculate_disk_gb(df_line_split[2])
        disk_avail += _calculate_disk_gb(df_line_split[3])
        disk_percent += float(df_line_split[4][:-1])

    return [disk_used, disk_avail, disk_percent]


def _calculate_disk_gb(disk_str):
    """
    Converts and returns strings with K, M, or G in the last character to
    the proper float value.
    """
    disk_used = 0

    if disk_str == "0":
        disk_used += 0
    elif disk_str[-1] == "K":
        disk_used += float(disk_str[:-1])/1000000
    elif disk_str[-1] == "M":
        disk_used += float(disk_str[:-1])/1000
    elif disk_str[-1] == "G":
        disk_used += float(disk_str[:-1])

    return disk_used


def get_kernel():
    """
    Gets kernel information
    """
    return str(run("uname -r"))


def get_ifconfig():
    """
    Gets ifconfig info
    """
    ifconfig = run("ifconfig").split("\n")[1]
    address = None
    netmask = None

    return ifconfig


if __name__=="__main__":
    """
    Main function + argument parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("output_type", help="Specify the type of output " + \
                    "you'd like the results to be", type=str)
    args = parser.parse_args()

    if args.output_type == "table":
        stats_out = execute(stats)
        print_stats_table(build_stats_table(stats_out))
