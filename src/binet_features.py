import ipaddress
import numpy as np

def classify_ip(ip):
    '''
    str ip - ip address string to attempt to classify.
    treat ipv6 addresses as N/A
    '''
    try:
        ip_addr = ipaddress.ip_address(ip)
        if isinstance(ip_addr,ipaddress.IPv6Address):
            return 'ipv6'
        elif isinstance(ip_addr,ipaddress.IPv4Address):
            # split on .
            octs = ip_addr.exploded.split('.')
            if 0 < int(octs[0]) < 127: return 'A'
            elif 127 < int(octs[0]) < 192: return 'B'
            elif 191 < int(octs[0]) < 224: return 'C'
            else: return 'N/A'
    except ValueError:
        return 'N/A'

def avg_duration(x):
    return np.average(x)

def n_dports_gt1024(x):
    count = 0
    for p in x:
        if p>1024: count += 1
    return count
n_dports_gt1024.__name__ = 'n_dports>1024'

def n_dports_lt1024(x):
    count = 0
    for p in x:
        if p<1024: count += 1
    return count
n_dports_lt1024.__name__ = 'n_dports<1024'

def n_sports_gt1024(x):
    count = 0
    for p in x:
        if p>1024: count += 1
    return count
n_sports_gt1024.__name__ = 'n_sports>1024'

def n_sports_lt1024(x):
    count = 0
    for p in x:
        if p<1024: count += 1
    return count
n_sports_lt1024.__name__ = 'n_sports<1024'

def label_atk_v_norm(x):
    for l in x:
        if 'Botnet' in l: return 'Attack'
    return 'Normal'
#label_atk_v_norm.__name__ = 'label'

def background_flow_count(x):
    count = 0
    for l in x:
        if 'Background' in l: count += 1
    return count

def normal_flow_count(x):
    if x.size == 0: return 0
    count = 0
    for l in x:
        if 'Normal' in l: count += 1
    return count

def n_conn(x):
    return x.size

def n_tcp(x):
    count = 0
    for p in x:
        if p == 'tcp': count += 1
    return count

def n_udp(x):
    count = 0
    for p in x:
        if p == 'udp': count += 1
    return count

def n_icmp(x):
    count = 0
    for p in x:
        if p == 'icmp': count += 1
    return count

def n_s_a_p_address(x):
    count = 0
    for i in x:
        if classify_ip(i) == 'A': count += 1
    return count

def n_d_a_p_address(x):
    count = 0
    for i in x:
        if classify_ip(i) == 'A': count += 1
    return count

def n_s_b_p_address(x):
    count = 0
    for i in x:
        if classify_ip(i) == 'B': count += 1
    return count

def n_d_b_p_address(x):
    count = 0
    for i in x:
        if classify_ip(i) == 'A': count += 1
    return count

def n_s_c_p_address(x):
    count = 0
    for i in x:
        if classify_ip(i) == 'C': count += 1
    return count

def n_d_c_p_address(x):
    count = 0
    for i in x:
        if classify_ip(i) == 'C': count += 1
    return count

def n_s_na_p_address(x):
    count = 0
    for i in x:
        if classify_ip(i) == 'N/A': count += 1
    return count

def n_d_na_p_address(x):
    count = 0
    for i in x:
        if classify_ip(i) == 'N/A': count += 1
    return count

def n_s_ipv6(x):
    count = 0
    for i in x:
        if classify_ip(i) == 'ipv6': count += 1
    return count

def n_d_ipv6(x):
    count = 0
    for i in x:
        if classify_ip(i) == 'ipv6': count += 1
    return count

def n_attack(x):
    '''
    Count the number of attacks,
    to do this we need to simply count number of flows labeled with botnet
    Do not use this feature for model training.
    '''
    count = 0
    for i in x:
        if 'Botnet' in i: count += 1
    return count


