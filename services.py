import ipaddress

def get_ip_class(ip: str) -> str:
    """Retorna a classe do IP com base no primeiro octeto."""
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

def to_binary_str(ip_str: str) -> str:
    """Converte um endereço IP em string binária."""
    return '.'.join(f"{int(octet):08b}" for octet in ip_str.split('.'))

def calculate_ipv4(ip: str, subnet: str) -> dict:
    """Calcula informações sobre um endereço IPv4 e sua sub-rede."""
    try:
        ip_network = ipaddress.IPv4Network(f"{ip}/{subnet}", strict=False)
        ip_obj = ipaddress.IPv4Address(ip)

        # Cálculo de endereços
        first_host = ip_network.network_address + 1
        last_host = ip_network.broadcast_address - 1

        # Converte IP e máscaras para formato binário
        binary_ip = to_binary_str(ip)
        binary_subnet_mask = to_binary_str(str(ip_network.netmask))
        binary_wildcard_mask = to_binary_str(str(ip_network.hostmask))

        # Retorna um dicionário com os campos solicitados
        return {
            "IP Class": get_ip_class(ip),  # Classe do IP
            "Subnet Mask": str(ip_network.netmask),  # Máscara de sub-rede
            "Usable Host IP Range": f"{first_host} - {last_host}",  # Faixa de hosts utilizáveis
            "Network Address": str(ip_network.network_address),  # Endereço de rede
            "First Host": str(first_host),  # Primeiro IP utilizável
            "Last Host": str(last_host),  # Último IP utilizável
            "Broadcast Address": str(ip_network.broadcast_address),  # Endereço de broadcast
            "IP Address (Binary)": binary_ip,  # IP em binário
            "Subnet Mask (Binary)": binary_subnet_mask,  # Máscara de sub-rede em binário
            "Wildcard Mask (Binary)": binary_wildcard_mask,  # Máscara wildcard em binário
            "CIDR Notation": f"/{ip_network.prefixlen}",  # Notação CIDR
            "IP Type": "Private" if ip_network.is_private else "Public",  # Tipo de endereço
            "Total Number of Hosts": ip_network.num_addresses,
            "Number of Usable Hosts": ip_network.num_addresses - 2,
        }

    except ValueError as e:
        return {"error": str(e)}  # Retorna um erro se houver uma exceção de valor


def valida_imc(genero: str, imc: float) -> str:
    faixas = {
        'H': [(20, 'Abaixo do normal'), (24.99, 'Normal'), (29.99, 'Obesidade leve'), (39.99, 'Obesidade Moderada'),
              (float('inf'), 'Obesidade Mórbida')],
        'M': [(19, 'Abaixo do normal'), (23.90, 'Normal'), (28.99, 'Obesidade leve'), (38.99, 'Obesidade Moderada'),
              (float('inf'), 'Obesidade Mórbida')]
    }

    for limite, classificacao in faixas[genero]:
        if imc <= limite:
            return classificacao


def calcular_imc(genero: str, peso: float, altura: float) -> dict:
    imc = round(peso / (altura ** 2), 2)
    return {
        'imc': imc,
        'classificacao': valida_imc(genero, imc)
    }
