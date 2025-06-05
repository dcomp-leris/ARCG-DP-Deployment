#!/usr/bin/env python3

import csv

from time import sleep, time, perf_counter_ns
from scapy.all import Packet, bind_layers, BitField, ShortField, IntField, XByteField, PacketListField, FieldLenField, Raw, Ether, IP, UDP, sendp, get_if_hwaddr, sniff


class InBandNetworkTelemetry(Packet):
    fields_desc = [ BitField("switchID_t", 0, 31),
                    BitField("ingress_port",0, 9),
                    BitField("egress_port",0, 9),
                    BitField("egress_spec", 0, 9),
                    BitField("priority", 0, 3),
                    BitField("qid", 0, 5),
                    BitField("ingress_global_timestamp", 0, 48),
                    BitField("egress_global_timestamp", 0, 48),
                    BitField("enq_timestamp",0, 32),
                    BitField("enq_qdepth",0, 19),
                    BitField("deq_timedelta", 0, 32),
                    BitField("deq_qdepth", 0, 19),
                    BitField("processing_time", 0, 32)
                  ]
    def extract_padding(self, p):
                return "", p

class nodeCount(Packet):
  name = "nodeCount"
  fields_desc = [ ShortField("id", 0),
                  ShortField("count", 0),
                  PacketListField("INT", [], InBandNetworkTelemetry, count_from=lambda pkt:(pkt.count*1))]

def main():

    dstIP0 = '172.16.0.1'
    dstIP1 = '172.16.0.1' 
    #dstIP2 = '10.10.10.3'  
    dstMAC = "00:15:4d:13:5c:a5"
    iface = 'enp2s0np0' #'wlp6s0'

    bind_layers(IP, nodeCount, proto = 253)
    
    id = 0
    path = 'data'
    with open(f'{path}/sender_queue0.csv', 'w', newline='') as file0, \
         open(f'{path}/sender_queue1.csv', 'w', newline='') as file1:
         #open(f'{path}/sender_queue2.csv', 'w', newline='') as file2:
        
        writer0 = csv.writer(file0)
        writer1 = csv.writer(file1)
        #writer2 = csv.writer(file2)
        
        writer0.writerow(['ID', 'Timestamp'])
        writer1.writerow(['ID', 'Timestamp'])
        #writer2.writerow(['ID', 'Timestamp'])

        while True:
            pkt0 = Ether(src=get_if_hwaddr(iface), dst=dstMAC) / IP(
            dst=dstIP0, proto=253, tos = 0x00) / nodeCount(id=id, count=0, INT=[])
            timestamp = perf_counter_ns()
            sendp(pkt0, iface=iface)
            writer0.writerow([id, timestamp])
            pkt0.show2()
            sleep(0.33)

            pkt1 = Ether(src=get_if_hwaddr(iface), dst=dstMAC) / IP(
            dst=dstIP1, proto=253,tos = 0x01) / nodeCount(id=id, count=0, INT=[])
            timestamp = perf_counter_ns()
            sendp(pkt1, iface=iface)
            writer1.writerow([id, timestamp])
            pkt1.show2()
            sleep(0.33)

            # pkt2 = Ether(src=get_if_hwaddr(iface), dst=dstMAC) / IP(
            # dst=dstIP2, proto=253) / nodeCount(id=id, count=0, INT=[])
            # timestamp = perf_counter_ns()
            # sendp(pkt2, iface=iface)
            # writer2.writerow([id, timestamp])
            # pkt2.show2()
            # sleep(0.33)

            id += 1

if __name__ == '__main__':
    main()
