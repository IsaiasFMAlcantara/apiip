import ipaddress

def get_ip_class(ip: str) -> str:
    """Retorna a classe do IP com base no primeiro octeto."""
    first_octet = int(ip.split('.')[0])  # Obtém o primeiro octeto do IP
    if 1 <= first_octet <= 126:
        return 'A'  # Classe A
    elif 128 <= first_octet <= 191:
        return 'B'  # Classe B
    elif 192 <= first_octet <= 223:
        return 'C'  # Classe C
    elif 224 <= first_octet <= 239:
        return 'D'  # Classe D (multicast)
    else:
        return 'E'  # Classe E (reservada)

def to_binary_str(ip_str: str) -> str:
    """Converte um endereço IP em string binária."""
    return '.'.join(f"{int(octet):08b}" for octet in ip_str.split('.'))  # Converte cada octeto para binário

def calculate_ipv4(ip: str, subnet: str) -> dict:
    """Calcula informações sobre um endereço IPv4 e sua sub-rede."""
    try:
        # Cria um objeto IPv4Network com o IP e a máscara de sub-rede
        ip_network = ipaddress.IPv4Network(f"{ip}/{subnet}", strict=False)
        ip_obj = ipaddress.IPv4Address(ip)  # Cria um objeto IPv4Address para o IP

        # Cálculo de endereços utilizáveis
        first_host = ip_network.network_address + 1  # Primeiro endereço utilizável
        last_host = ip_network.broadcast_address - 1  # Último endereço utilizável

        # Converte IP e máscaras para formato binário
        binary_ip = to_binary_str(ip)  # IP em binário
        binary_subnet_mask = to_binary_str(str(ip_network.netmask))  # Máscara de sub-rede em binário
        binary_wildcard_mask = to_binary_str(str(ip_network.hostmask))  # Máscara wildcard em binário

        # Cálculo de valores adicionais
        binary_id = f"{int(ip_obj):032b}"  # Representação binária do ID do IP
        integer_id = int(ip_obj)  # ID do IP como inteiro
        hex_id = hex(integer_id)  # ID do IP em hexadecimal
        in_addr_arpa = '.'.join(reversed(ip.split('.'))) + '.in-addr.arpa'  # Formato in-addr.arpa
        ipv4_packed = ip_obj.packed.hex()  # Representação empacotada do IP em hexadecimal
        prefix_6to4 = f"2002:{ipv4_packed[:4]}:{ipv4_packed[4:]}::/48"  # Prefixo 6to4

        # Retorna um dicionário com todas as informações calculadas
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
            "Number of Usable Hosts": ip_network.num_addresses - 2,  # Subtrai 2 para excluir a rede e o broadcast
            "Subnet Mask": str(ip_network.netmask),
            "Wildcard Mask": str(ip_network.hostmask),
            "IP Class": get_ip_class(ip),  # Classe do IP
            "CIDR Notation": f"/{ip_network.prefixlen}",  # Notação CIDR
            "IP Type": "Private" if ip_network.is_private else "Public",  # Tipo de IP
            "Short": f"{ip} /{ip_network.prefixlen}",  # Representação curta
            "Binary ID": binary_id,
            "Integer ID": integer_id,
            "Hex ID": hex_id,
            "in-addr.arpa": in_addr_arpa,
            "IPv4 Mapped Address": f"::ffff:{ip}",  # Endereço IPv4 mapeado
            "6to4 Prefix": prefix_6to4  # Prefixo 6to4
        }

    except ValueError as e:
        return {"error": str(e)}  # Retorna um erro se houver uma exceção de valor