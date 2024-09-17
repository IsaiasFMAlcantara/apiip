import ipaddress
from ipv4binary import get_ip_class  # Importa a função do arquivo ipv4binary.py

def calculate_ipv4(ip, subnet):
    ip_network = ipaddress.IPv4Network(f"{ip}/{subnet}", strict=False)
    ip_obj = ipaddress.IPv4Address(ip)
    first_host = ip_network.network_address + 1
    last_host = ip_network.broadcast_address - 1

    # Calcular valores adicionais
    binary_id = f"{int(ip_obj):032b}"
    integer_id = int(ip_obj)
    hex_id = hex(int(ip_obj))
    in_addr_arpa = '.'.join(reversed(ip.split('.'))) + '.in-addr.arpa'
    ipv4_mapped = f"::ffff:{ip}"
    ipv4_packed = ip_obj.packed.hex()
    prefix_6to4 = f"2002:{ipv4_packed[:4]}:{ipv4_packed[4:]}::/48"

    response = {
        "IP Address": ip,
        "Network Address": str(ip_network.network_address),
        "Usable Host IP Range": f"{first_host} - {last_host}",
        "First Host":first_host,
        "Last Host": last_host,
        "Broadcast Address": str(ip_network.broadcast_address),
        "Total Number of Hosts": ip_network.num_addresses,
        "Number of Usable Hosts": ip_network.num_addresses - 2,
        "Subnet Mask": str(ip_network.netmask),
        "Wildcard Mask": str(ip_network.hostmask),
        "Binary Subnet Mask": f"{bin(int(ip_network.netmask))}",
        "IP Class": get_ip_class(ip),
        "CIDR Notation": f"/{ip_network.prefixlen}",
        "IP Type": "Private" if ip_network.is_private else "Public",
        "Short": f"{ip} /{ip_network.prefixlen}",
        "Binary ID": binary_id,
        "Integer ID": integer_id,
        "Hex ID": hex_id,
        "in-addr.arpa": in_addr_arpa,
        "IPv4 Mapped Address": ipv4_mapped,
        "6to4 Prefix": prefix_6to4
    }

    return response
