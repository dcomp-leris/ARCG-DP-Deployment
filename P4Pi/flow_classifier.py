import cProfile
import logging
from scapy.all import sniff, sendp, UDP, Ether, IP
from scapy.layers.inet6 import IPv6
import threading
import time
from queue import Queue, Empty
from packet_classifier import PacketClassifier
import hashlib
import socket
import yaml
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI
import crcmod
import ipaddress
from influxdb_client_3 import InfluxDBClient3, Point


''' General Variables '''
#config_file = '/home/cls/config.yaml'
config_file = 'config.yaml'
# Model path configuration
model_path = 'dt_model.joblib'
#model_path = '/home/cls/rf_model.joblib'

# Network configuration
SRC_INTERFACE = 'eth1'  # Interface listen to TG


# Store the flows to avoid sending of the consecutive packets of the flows
#lookup_table = {} # lookup table to cache the  packets of the flow

# logging and counting the packets
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s') # added to track the packets

# Initialize counters
packets_received = 0
packets_forwarded = 0


# Packet and time counter
#cached_pkt_start = 0
#cached_pkt_end = 0

#cached_time_start =0
#cached_time_end =0


#cached_pkts = 0
#cached_time = 0

# load the Classifier
# classifier = PacketClassifier(model_path)  #'/home/alireza/my_code/Classifier/dt_model.joblib')  # model_path

# Global variables for monitoring
#packets_forwarded = 0
#bytes_forwarded = 0
start_time = time.time()
#q_cache = Queue()


# Assuming classifier and container_table are defined elsewhere
global last_reset_time
last_reset_time = time.time()
#lookup_table = {}

# Initialize the dictionary
my_dict = {}

counter_CG_class = 0
CG_class_IPs = []
CG_first_octet = 13

def connectDB():
    token = "QIrU2j0_lzhvmPXJehNbnd9JIjA3c-DWu-smeAwdEWk0XGJIfjGTovzeJIH40mjtf5mxAV39AOfv45at9j-m8w==" #ADD TOKEN
    org = "Research"
    host = "https://us-east-1-1.aws.cloud2.influxdata.com"

    client = InfluxDBClient3(host=host, token=token, org=org)
    #client = 1
    return client


client = connectDB()
database = "CG-Monitoramento"
id = "test"


# Function to add or update an entry in the dictionary
def add_or_update_entry(key, value, allow_update=True):
    if key in my_dict.keys():
        if allow_update:
            #print(f"Key '{key}' exists. Updating the value.")
            my_dict[key] = value  # Update the existing entry
            return True
        else:
            #print(f"Key '{key}' exists. Update not allowed.")
            return False
    else:

        my_dict[key] = value
        return True
        '''
        if allow_update:
            #print(f"Key '{key}' does not exist. Adding new entry.")
            my_dict[key] = value  # Insert a new entry
            return True
        else:
            #print(f"Key '{key}' does not exist. Blocking action.")
            return False'''

# Convert IP address to bits

def ip_to_bits(ip):
    try:
        # Try to parse the IP address using ipaddress module
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        raise ValueError("Invalid IP address format")

    # Check if the IP address is IPv4
    if ip_obj.version == 4:
        return ''.join(format(int(octet), '08b') for octet in ip.split('.'))
    # Check if the IP address is IPv6
    elif ip_obj.version == 6:
        return ''.join(format(int(octet, 16), '016b') for octet in ip_obj.exploded.split(':'))



'''def ip_to_bits(ip):
    return ''.join(format(int(octet), '08b') for octet in ip.split('.'))'''

# Convert integer to bits
def port_to_bits(integer, bit_length=16):
    return format(integer, f'0{bit_length}b')

# Convert bits to CRC16
def bits_to_crc16(bits):
    crc16_func = crcmod.predefined.mkPredefinedCrcFun('crc-16')

    # Convert bit string to bytes
    byte_array = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

    crc = crc16_func(byte_array)
    return crc





''' Functions Definition '''
def load_config(yaml_file):
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)
    return config


# Set the reset time for lookup table

reset_time  = 8000      # it is set with config file
entry_num = 10          # it is set with config file

def reset_lookup_table_if_needed():
    global my_dict, last_reset_time
    current_time = time.time()
    if (current_time - last_reset_time) * 1000 >= reset_time  or len(my_dict) >= entry_num:  # Check if 100ms have passed
        my_dict = {}  # Reset the table
        last_reset_time = current_time
        classifier = PacketClassifier(model_path)






def forward_packet(packet):

    global packets_forwarded, bytes_forwarded, lookup_table, q_cache, i , packets_received, classifier, counter_CG_class, CG_first_octet, CG_class_IPs, client, database, id

    reset_lookup_table_if_needed()  # Check if it's time to reset the lookup_table
    controller = SimpleSwitchThriftAPI(9090)

    if (IP in packet or IPv6 in packet) and UDP in packet: #if IP in packet and UDP in packet:

        pkt_type = "IPv6" if IPv6 in packet else "IPv4"
        # print('Received pkt', pkt_type)
        #bytes_forwarded += len(packet)
        #flowkey_local = hashlib.sha256(str((packet[IP].src, packet[IP].dst, packet[UDP].dport)).encode().hex().encode()).hexdigest()
        #flowkey_reverse =  hashlib.sha256(str((packet[IP].dst, packet[IP].src, packet[UDP].dport)).encode().hex().encode()).hexdigest()

        # logging
        packets_received += 1
        #print(f'Received packet {packets_received}  from {packet[IP].src} to {packet[IP].dst} on iface {SRC_INTERFACE}', time.time())
        #print(f'pkt_type:receiving,pkt_no:{packets_received},from:{packet[IP].src},to: {packet[IP].dst},iface:{SRC_INTERFACE},',"Time:", time.time())
        #logging.debug(f"Received packet from {packet[IP].src} to {packet[IP].dst}")

        # Classification the packet

        result = classifier.classify_packet(packet)
        if not result or len(result)==2 or len(result)==1 or len(result)< 3 or result[1] is None:
            #q_cache.put([flowkey_local,packet])
            return
        else:
            # flow_class = "AR" if result[1] in ('AR_UL', 'AR_DL' ,'AR') else "CG" if result[1] in ('CG_UL', 'CG_DL','CG') else "Other"
            flow_class = "CG" if result[1] in ('CG_UL', 'CG_DL','CG') else "Other"
            if pkt_type=="IPv4":
                dst_ip = str(packet[IP].dst)
                src_ip = str(packet[IP].src)
                binary_ip_dst = ip_to_bits(str(packet[IP].dst))
                ip_crc16_dst = bits_to_crc16(binary_ip_dst)
                # ip_crc16 = crc16_from_hex(hex_ip)                                   # ip in crc16
                # port_crc16 = crc16_from_hex(format(packet[UDP].dport, 'x'))         # port in crc16
                binary_port_dst = port_to_bits(packet[UDP].dport)
                ip_port_concat = binary_ip_dst + binary_port_dst

                #port_crc16_dst = bits_to_crc16(binary_port_dst)
                # port_crc16 = bits_to_crc16(binary_port)  packet[IPv6]

                #flow_id_dst = ip_crc16_dst + port_crc16_dst   # flow_id crc using ip & port
                flow_id_dst = bits_to_crc16(ip_port_concat)
                unique_flow_flag = add_or_update_entry(flow_id_dst, flow_class, False)
                #print("tag",unique_flow_flag)

                ### Reverse Flow ID
                # src_ip = str(packet[IP].src)
                binary_ip_src = ip_to_bits(str(packet[IP].src))
                ip_crc16_src = bits_to_crc16(binary_ip_src)
                # ip_crc16 = crc16_from_hex(hex_ip)                                   # ip in crc16
                # port_crc16 = crc16_from_hex(format(packet[UDP].dport, 'x'))         # port in crc16
                binary_port_src = port_to_bits(packet[UDP].sport)

                port_crc16_src = bits_to_crc16(binary_port_src)
                # port_crc16 = bits_to_crc16(binary_port)  packet[IPv6]

                flow_id_src = ip_crc16_src + port_crc16_src   # flow_id crc using ip & port
                unique_flow_flag = add_or_update_entry(flow_id_src, flow_class, False)
                #print("tag",unique_flow_flag)





            elif  pkt_type=="IPv6":
                dst_ip = str(packet[IPv6].dst)
                src_ip = str(packet[IPv6].src)
                binary_ip_dst = ip_to_bits(str(packet[IPv6].dst))
                #ip_crc16_dst = bits_to_crc16(binary_ip_dst)
                # ip_crc16 = crc16_from_hex(hex_ip)                                   # ip in crc16                # port_crc16 = crc16_from_hex(format(packet[UDP].dport, 'x'))         # port in cr>                binary_port = port_to_bits(packet[UDP].dport)
                binary_port_dst = port_to_bits(packet[UDP].dport)
                #port_crc16_dst = bits_to_crc16(binary_port_dst)
                # port_crc16 = bits_to_crc16(binary_port)


                #flow_id_dst = ip_crc16_dst + port_crc16_dst   # flow_id crc using ip & port
                ip_port_concat = binary_ip_dst + binary_port_dst
                flow_id_dst = bits_to_crc16(ip_port_concat)
                unique_flow_flag = add_or_update_entry(flow_id_dst, flow_class, False)
                #print("tag",unique_flow_flag)



                binary_ip_src = ip_to_bits(str(packet[IPv6].src))
                ip_crc16_src = bits_to_crc16(binary_ip_src)
                # ip_crc16 = crc16_from_hex(hex_ip)                                   # ip in crc16                # port_crc16 = crc16_from_hex(format(packet[UDP].dport, 'x'))         # port in cr>                binary_port = port_to_bits(packet[UDP].dport)
                binary_port_src = port_to_bits(packet[UDP].sport)
                port_crc16_src = bits_to_crc16(binary_port_src)
                # port_crc16 = bits_to_crc16(binary_port)

                flow_id_src = ip_crc16_src + port_crc16_src   # flow_id crc using ip & port
                unique_flow_flag = add_or_update_entry(flow_id_src, flow_class, False)
                #print("tag",unique_flow_flag)






            if flow_class == "CG" and unique_flow_flag:  # or flow_class == "AR":
         # High Priority--> CG flow if it was CG & AR
                #controller.table_add('flow_queue', 'assign_q', [str(flow_id)], ['2'])
                controller.register_write('flow_queue', flow_id_dst, 2)
                #controller.register_write('flow_queue', flow_id_src, 2)

                print(f'DST IP {dst_ip} DST Port {packet[UDP].dport} in Queue 2')
                print(f'SRC IP {src_ip} SRC Port {packet[UDP].sport} in Queue 2')


                counter_CG_class = counter_CG_class + 1
                print(counter_CG_class)
                if pkt_type == "IPv4":
                    CG_class_IPs.append((src_ip.split('.')[0], dst_ip.split('.')[0]))
                else:
                    CG_class_IPs.append(('1', '1'))

                if counter_CG_class >= 5:
                    counter_CG_IP = 0

                    for ips in CG_class_IPs:
                        if int(ips[0]) == CG_first_octet or int(ips[1]) == CG_first_octet:
                            counter_CG_IP = counter_CG_IP + 1

                    rate = (counter_CG_IP / counter_CG_class) * 100
                    print(rate)
                    counter_CG_class = 0
                    CG_class_IPs = []

                    point = (
                        Point("Rating")
                        .tag("ID", id)
                        .field("rate", rate)
                    )
                    client.write(database=database, record=point)



            elif flow_class == "Other" and unique_flow_flag:
                # controller.table_add('flow_queue', 'assign_q', [str(flow_id)], ['1'])     # Medium Priority --> UDP packets if it was other
                controller.register_write('flow_queue', flow_id_dst, 1)
                #controller.register_write('flow_queue', flow_id_src, 1)
                # print(f'IP {dst_ip}, Port {packet[UDP].dport} in Queue 1')
                print(f'DST IP {dst_ip} DST Port {packet[UDP].dport} in Queue 1')
                print(f'SRC IP {src_ip} SRC Port {packet[UDP].sport} in Queue 1')
            elif unique_flow_flag:
                controller.register_write('flow_queue', flow_id_dst, 0)
                #controller.register_write('flow_queue', flow_id_src, 0)
                #controller.table_add('flow_queue', 'assign_q', [str(flow_id)], ['0'])     # No Priority --> TCP or other
                print(f'DST IP {dst_ip} DST Port {packet[UDP].dport} in Queue 0')
                print(f'SRC IP {src_ip} SRC Port {packet[UDP].sport} in Queue 0')



        '''if flowkey_local in lookup_table.keys():
            iface, src_mac, dst_mac = container_table[lookup_table[flowkey_local]]
            forwarded_packet = Ether(src=src_mac, dst=dst_mac) / packet[IP]
            sendp(forwarded_packet, iface=iface, verbose=False)
            packets_forwarded += 1
            print('************************************************')
            print(f'pkt_type:forwarding[lookup],pkt_no:{packets_forwarded},from:{forwarded_packet[IP].src},to: {forwarded_packet[IP].dst},iface:{iface},',"Time:", time.time())
            print('************************************************')

        else:
            # Classification the packet
            result = classifier.classify_packet(packet)
            if not result or len(result)==2 or len(result)==1 or result[1] is None:
                q_cache.put([flowkey_local,packet])
                return
            flow_class = "AR" if result[1] in ('AR_UL', 'AR_DL' ,'AR') else "CG" if result[1] in ('CG_UL', 'CG_DL','CG') else "Other"
            lookup_table[flowkey_local] = flow_class # result[0]] = flow_class
            print(f"====================")    # Received pkts {packets_received}")
            print('Forwarding starts:',(packet[IP].src,packet[IP].dst,packet[UDP].dport),'==>',flow_class)
            print(f'Features [{result[2]}]')
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(str([(packet[IP].src,packet[IP].dst,packet[UDP].sport,packet[UDP].dport),result[2],result[1]]).encode(), ('192.168.140.2', 12348))
            print("====================")


            # Limit lookup_table to 10 entries
            if len(lookup_table) >= entry_num:
            # This is a simple way to remove an entry; you may want to refine this logic
                lookup_table.pop(next(iter(lookup_table)))  # Remove an arbitrary (the first) entry


            #if result[0] not in lookup_table:
                #lookup_table[result[0]] = flow_class

            iface, src_mac, dst_mac = container_table[flow_class] #lookup_table[result[0]]]
            forwarded_packet = Ether(src=src_mac, dst=dst_mac) / packet[IP]



            #cached_pkt_start = 0
            #cached_pkt_end = 0
            #cached_time_start =0
            #cached_time_end =0
            cached_pkts = 0
            cached_time = 0

            cached_time_start = time.time()
            while not q_cache.empty():
                cache_packet = None
                #cached_pkt_start = packets_forwarded # To calculate cached packets to classification
                cached_pkts+=1
                #cached_time_start = time.time()
                cache_packet= q_cache.get()
                #print('cache packet--?',cache_packet)
                #hasher.digest()
                #if result[0] not in lookup_table:
                #lookup_table[result[0]] = flow_class
                if  (flowkey_local in cache_packet[0]) or (flowkey_reverse in cache_packet[0]):
                    my_pkt = Ether(src=src_mac, dst=dst_mac) / cache_packet[1][IP]
                    sendp(my_pkt, iface=iface, verbose=False)
                    packets_forwarded += 1
                    print(f'pkt_type:forwarding[cached],pkt_no:{packets_forwarded},from:{forwarded_packet[IP].src},to: {forwarded_packet[IP].dst},iface:{iface},',"Time:", time.time())
                else:
                    continue
            cached_time = time.time() - cached_time_start
            sendp(forwarded_packet, iface=iface, verbose=False)
            # logging
            #print('Forwarded', time.time())
            packets_forwarded += 1
            #cached_pkt_end = packets_forwarded
            #cached_pkts = int(cached_pkt_end) - int(cached_pkt_start)
            #cached_time_end = time.time()
            #cached_time = cached_time_end - cached_time_start
            #print(f'Forwarded packet {packets_forwarded}  from {forwarded_packet[IP].src} to {forwarded_packet[IP].dst} on iface {iface}', time.time())
            print(f'pkt_type:forwarding[classified],pkt_no:{packets_forwarded},from:{forwarded_packet[IP].src},to: {forwarded_packet[IP].dst},iface:{iface},',"Time:", time.time())  #'c_time: ',cached_time, 'c_pkts: ', cached_pkts)
'''



        # Classification the packet



def main():
    global classifier, reset_time
    #config_file = '/home/cls/config.yaml'
    config = load_config(config_file)

    model_path = config['cls_config']['model'][config['cls_config']['model']['selection']]['path']
    SRC_INTERFACE = config['cls_config']['ingress']['interface']
    reset_time = config['cls_config']['lookup_table']['reset_time']
    entry_num = config['cls_config']['lookup_table']['reset_entry_num']
    classifier = PacketClassifier(model_path)

    print('The model in this classifier is ', config['cls_config']['model']['selection'],' loaded from ', model_path)
    print(f'The reset time for lookup table [and model loading!] is {reset_time}')

    print(f"Listening for UDP packets on {SRC_INTERFACE}...")
    sniff(iface=SRC_INTERFACE, prn=forward_packet, store=False)

    print(f"Total packets received: {packets_received}")
    print(f"Total packets forwarded: {packets_forwarded}")

if __name__ == "__main__":
    main()

    #profiler = cProfile.Profile()
    #profiler.run('main()')
    #profiler.print_stats()