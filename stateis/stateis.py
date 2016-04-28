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
        stats.append(get_kernel())
        for item in get_diskinfo():
            stats.append(item)
        stats.append(get_processes())
        stats.append(get_ram_usage())
        stats.append(get_uptime())

    fabric.network.disconnect_all()

    return stats


@runs_once
def build_stats_table(stats_out):
    """
    Builds the stats table according to predetermined headers and their
    associated values grabbed by the functions below
    """
    table_headers = [
        "IP Address", "Hostname", "Kernel", "Used GB", "Avail GB", "% Used GB",
        "# Proc", "RAM Use", "Uptime"
    ]

    stats_table = PrettyTable(table_headers)
    stats_table.align["IP Address"] = "l"
    stats_table.align["Hostname"] = "l"
    stats_table.align["Kernel"] = "r"
    stats_table.align["Used GB"] = "r"
    stats_table.align["Avail GB"] = "r"
    stats_table.align["% Used GB"] = "r"
    stats_table.align["# Proc"] = "r"
    stats_table.align["RAM Use"] = "r"
    stats_table.align["Uptime"] = "r"
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


@runs_once
def build_xml_file(stats_out):
    xml_string = "<servers>\n"

    for key in stats_out:
        xml_string += "\t<server>\n"
        xml_string += "\t\t<ip>" + key + "</ip>\n"
        xml_string += "\t\t<hostname>" + stats_out[key][0] + "</hostname>\n"
        xml_string += "\t\t<kernel>" + str(stats_out[key][1]) + "</kernel>\n"
        xml_string += "\t\t<gbused>" + str(stats_out[key][2]) + "</gbused>\n"
        xml_string += "\t\t<gbavail>" + str(stats_out[key][3]) + "</gbavail>\n"
        xml_string += "\t\t<gbpercent>" + str(stats_out[key][4]) + "</gbpercent>\n"
        xml_string += "\t\t<numproc>" + str(stats_out[key][5]) + "</numproc>\n"
        xml_string += "\t\t<ramuse>" + stats_out[key][6] + "</ramuse>\n"
        xml_string += "\t\t<uptime>" + stats_out[key][7] + "</uptime>\n"
        xml_string += "\t</server>\n"
    xml_string += "</servers>\n"

    return xml_string


@runs_once
def write_xml_file(xml_string):
    xml_file = open("stateis_output.xml", "w")
    xml_file.write(xml_string)
    xml_file.close()

    return None


def get_hostname():
    """
    Gets hostname using hostname
    """
    return str(run("hostname"))


def get_kernel():
    """
    Gets kernel information using uname -r
    """
    return str(run("uname -r"))


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


def get_processes():
    """
    Gets the number of running processes on the server using ps
    """
    process_num = 0

    for process in run("ps").split("\n")[0:]:
        process_num += 1

    return process_num


def get_ram_usage():
    """
    Gets the output of free -m and calculates ram usage on the server
    """
    raw_ram_list = run("free -m").split("\n")[1]
    filtered_ram_list = filter(None, raw_ram_list.split(" "))
    ram_total = filtered_ram_list[1]
    ram_used = filtered_ram_list[2]
    ram_usage = _calculate_ram_usage(ram_total, ram_used)

    return ram_usage


def _calculate_ram_usage(ram_total, ram_used):
    """
    Takes 2 string arguments and divides the two to calculate the percentage
    of RAM used
    """
    ram_calc = float(ram_used)/float(ram_total)

    if ram_calc > .99:
        return "100%"
    else:
        return str(ram_calc)[2:4] + "%"


def get_uptime():
    uptime = run("uptime").split(" ")

    return uptime[2] + uptime[3][:-1]


if __name__=="__main__":
    """
    Main function + argument parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("output_type", help="Specify the type of output " + \
                    "you'd like the results to be", type=str)
    args = parser.parse_args()
    stats_out = execute(stats)

    if args.output_type == "table":
        print_stats_table(build_stats_table(stats_out))
    elif args.output_type == "xml":
        write_xml_file(build_xml_file(stats_out))
