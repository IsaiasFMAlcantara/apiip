import ipaddress
from ipv4binary import get_ip_class

def calculate_ipv4(ip: str, subnet: str) -> dict:
    ip_network = ipaddress.IPv4Network(f"{ip}/{subnet}", strict=False)
    ip_obj = ipaddress.IPv4Address(ip)

    # Cálculo de endereços
    first_host = ip_network.network_address + 1
    last_host = ip_network.broadcast_address - 1

    # Converte IP e máscaras para formato binário
    def to_binary_str(ip_str):
        return '.'.join(f"{int(octet):08b}" for octet in ip_str.split('.'))

    binary_ip = to_binary_str(ip)
    binary_subnet_mask = to_binary_str(str(ip_network.netmask))
    binary_wildcard_mask = to_binary_str(str(ip_network.hostmask))

    # Calcula valores adicionais
    binary_id = f"{int(ip_obj):032b}"
    integer_id = int(ip_obj)
    hex_id = hex(integer_id)
    in_addr_arpa = '.'.join(reversed(ip.split('.'))) + '.in-addr.arpa'
    ipv4_packed = ip_obj.packed.hex()
    prefix_6to4 = f"2002:{ipv4_packed[:4]}:{ipv4_packed[4:]}::/48"

    return {
        "IP Address": ip,
        "IP Address (Binary)": binary_ip,
        "Subnet Mask (Binary)": binary_subnet_mask,
        "Wildcard Mask (Binary)": binary_wildcard_mask,
        "Network Address": str(ip_network.network_address),
        "Usable Host IP Range": f"{first_host} - {last_host}",
        "First Host": str(first_host),
        "Last Host": str(last_host),
        "Broadcast Address": str(ip_network.broadcast_address),
        "Total Number of Hosts": ip_network.num_addresses,
        "Number of Usable Hosts": ip_network.num_addresses - 2,
        "Subnet Mask": str(ip_network.netmask),
        "Wildcard Mask": str(ip_network.hostmask),
        "IP Class": get_ip_class(ip),
        "CIDR Notation": f"/{ip_network.prefixlen}",
        "IP Type": "Private" if ip_network.is_private else "Public",
        "Short": f"{ip} /{ip_network.prefixlen}",
        "Binary ID": binary_id,
        "Integer ID": integer_id,
        "Hex ID": hex_id,
        "in-addr.arpa": in_addr_arpa,
        "IPv4 Mapped Address": f"::ffff:{ip}",
        "6to4 Prefix": prefix_6to4
    }
