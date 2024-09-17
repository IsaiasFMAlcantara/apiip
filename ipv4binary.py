import ipaddress


def get_ip_class(ip):
    first_octet = int(ip.split('.')[0])
    if 1 <= first_octet <= 126:
        return 'A'
    elif 128 <= first_octet <= 191:
        return 'B'
    elif 192 <= first_octet <= 223:
        return 'C'
    elif 224 <= first_octet <= 239:
        return 'D'
    else:
        return 'E'


def calculate_ipv4_binary(ip, subnet):
    ip_network = ipaddress.IPv4Network(f"{ip}/{subnet}", strict=False)
    ip_obj = ipaddress.IPv4Address(ip)

    # Calcular valores em binário
    binary_ip = '.'.join(f"{int(octet):08b}" for octet in ip.split('.'))
    binary_network_address = '.'.join(f"{int(octet):08b}" for octet in str(ip_network.network_address).split('.'))
    binary_first_host = '.'.join(f"{int(octet):08b}" for octet in str(ip_network.network_address + 1).split('.'))
    binary_last_host = '.'.join(f"{int(octet):08b}" for octet in str(ip_network.broadcast_address - 1).split('.'))
    binary_broadcast_address = '.'.join(f"{int(octet):08b}" for octet in str(ip_network.broadcast_address).split('.'))
    binary_subnet_mask = '.'.join(f"{int(octet):08b}" for octet in str(ip_network.netmask).split('.'))
    binary_wildcard_mask = '.'.join(f"{int(octet):08b}" for octet in str(ip_network.hostmask).split('.'))

    response = {
        "IP Address (Binary)": binary_ip,
        "Network Address (Binary)": binary_network_address,
        "Usable Host IP Range (Binary)": f"{binary_first_host} - {binary_last_host}",
        "Broadcast Address (Binary)": binary_broadcast_address,
        "Total Number of Hosts": ip_network.num_addresses,
        "Number of Usable Hosts": ip_network.num_addresses - 2,
        "Subnet Mask (Binary)": binary_subnet_mask,
        "Wildcard Mask (Binary)": binary_wildcard_mask,
        "Binary Subnet Mask": f"{bin(int(ip_network.netmask))}",
        "CIDR Notation": f"/{ip_network.prefixlen}",
        "IP Class": get_ip_class(ip),
        "IP Type": "Private" if ip_network.is_private else "Public",
        "Short": f"{binary_ip} /{ip_network.prefixlen}"
    }

    return response
