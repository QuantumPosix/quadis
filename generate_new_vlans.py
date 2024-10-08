#!/bin/python3
def calculate_new_vlans(base_vlan, range_start, range_end, sub_vlans_per_vlan):
    """
    Calculates new VLANs based on a base VLAN, a range of numbers, and the number of sub-VLANs per VLAN.

    Args:
        base_vlan (int): The base VLAN number.
        range_start (int): The starting number of the range.
        range_end (int): The ending number of the range.
        sub_vlans_per_vlan (int): The number of sub-VLANs to create for each new VLAN.

    Returns:
        list: A list of new VLAN numbers.
    """

    new_vlans = []
    for number in range(range_start, range_end + 1):
        new_vlan = base_vlan + (number - 1) * 10
        for sub_vlan in range(new_vlan, new_vlan + sub_vlans_per_vlan + 1):
            new_vlans.append(sub_vlan)
    return new_vlans

# Example usage:
base_vlan = 1100
sub_vlans_per_vlan = 4
range_start = 1
range_end = 50

new_vlans = calculate_new_vlans(base_vlan, range_start, range_end, sub_vlans_per_vlan)

for vlan_id in new_vlans:
    #for ex4550
    # commands = f"""
    # set groups QinQ_vl{vlan_id} interfaces <*> mtu 9216
    # set groups QinQ_vl{vlan_id} interfaces <*> unit 0 family ethernet-switching port-mode access
    # set groups QinQ_vl{vlan_id} interfaces <*> unit 0 family ethernet-switching vlan members vlan{vlan_id}
    # set protocols vstp vlan {vlan_id} bridge-priority 24k
    # set vlans vlan{vlan_id} description vlan{vlan_id}
    # set vlans vlan{vlan_id} vlan-id {vlan_id}
    # set vlans vlan{vlan_id} dot1q-tunneling
    # """
    #for qfx5130
    commands = f"""
    set groups QinQ_vl{vlan_id} interfaces <*> flexible-vlan-tagging
    set groups QinQ_vl{vlan_id} interfaces <*> native-vlan-id {vlan_id}
    set groups QinQ_vl{vlan_id} interfaces <*> input-native-vlan-push disable
    set groups QinQ_vl{vlan_id} interfaces <*> mtu 9216
    set groups QinQ_vl{vlan_id} interfaces <*> encapsulation extended-vlan-bridge
    set groups QinQ_vl{vlan_id} interfaces <*> unit 0 vlan-id-list 1-4000
    set groups QinQ_vl{vlan_id} interfaces <*> unit 0 input-vlan-map push
    set groups QinQ_vl{vlan_id} interfaces <*> unit 0 output-vlan-map pop
    set vlans vlan{vlan_id} description vlan{vlan_id}
    set vlans vlan{vlan_id} interface ae0.{vlan_id}
    set interfaces ae0 unit {vlan_id} vlan-id {vlan_id}
    set protocols vstp vlan {vlan_id} bridge-priority 24k
    """
    #for core
    # commands = f"""
    # set protocols igmp-snooping vlan vlan{vlan_id}
    # set vlans vlan{vlan_id} description QinQ_Vlan{vlan_id}
    # set vlans vlan{vlan_id} vlan-id {vlan_id}
    # """
    print(commands, end="")