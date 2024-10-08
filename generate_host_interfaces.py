#!/bin/python3

import csv
import sys

def generate_host_interfaces(csv_file):
    """Generates commands based on a CSV file.

    Args:
        csv_file (str): The path to the CSV file.

    Returns:
        list: A list of generated commands.
    """

    commands = []
    interfaces = {}
    header = None

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Read header row
        for row in reader:
            # Map column names to their indices
            column_indices = {column: index for index, column in enumerate(header)}

            # Extract data based on column names
            host = row[column_indices['Assigned Hostname']] + ".example.domain.com"
            public_ip = row[column_indices['Host IP']]
            public_mac = row[column_indices['Public MAC Address']]
            bmc_ip = row[column_indices['MGMT IP']]
            bmc_mac = row[column_indices['BMC MAC Address']]
            # Check if host already exists in interfaces
            if host not in interfaces:
                interfaces[host] = {}

            for i in range(1, 5):
                interface_number = i
                interface_port = row[column_indices[f"em{i}port"]]
                interface_switch = row[column_indices[f"em{i}sw"]]
                interface_mac = row[column_indices[f"em{i} MAC Address"]]
                interface_speed = row[column_indices[f"em{i} speed"]]

                interfaces[host]["em" + str(interface_number) + "port"] = interface_port
                interfaces[host]["em" + str(interface_number) + "switch"] = interface_switch
                interfaces[host]["em" + str(interface_number) + "mac"] = interface_mac
                interfaces[host]["em" + str(interface_number) + "speed"] = interface_speed

    for host, interface_data in interfaces.items():
        for i in range(1, 5):
            em_port = interface_data["em" + str(i) + "port"]
            em_switch = interface_data["em" + str(i) + "switch"]
            em_mac = interface_data["em" + str(i) + "mac"]
            em_speed = interface_data["em" + str(i) + "speed"]
            command = f"quads --host {host} --add-interface --interface-name em{i} --interface-mac {em_mac} --interface-switch-ip {em_switch} --interface-port {em_port} --interface-vendor intel --interface-speed {em_speed}"
            commands.append(command)

    return commands
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    commands = generate_host_interfaces(csv_file)
    for command in commands:
        print(command)