#!/usr/bin/env python3

from scapy.all import Packet, bind_layers, BitField, ShortField, IntField, Ether, IP, UDP, sendp, get_if_hwaddr, sniff, PacketListField
import pandas as pd
import sys
from time import time, perf_counter_ns


class InBandNetworkTelemetry(Packet):
    # fields_desc = [
    #     BitField("switchID_t", 0, 31),
    #     BitField("ingress_port", 0, 9),
    #     BitField("egress_port", 0, 9),
    #     BitField("egress_spec", 0, 9),
    #     BitField("priority", 0, 3),
    #     BitField("qid", 0, 5),
    #     BitField("ingress_global_timestamp", 0, 48),
    #     BitField("egress_global_timestamp", 0, 48),
    #     BitField("enq_timestamp", 0, 32),
    #     BitField("enq_qdepth", 0, 19),
    #     BitField("deq_timedelta", 0, 32),
    #     BitField("deq_qdepth", 0, 19),
    #     BitField("processing_time", 0, 32)
    # ]
    fields_desc = [ BitField("swid", 0, 6),
                    BitField("ingress_port", 0, 9),
                    BitField("egress_port",0,9),
                    BitField("egress_spec",0,9),
                    BitField("qid",0,7),
                    BitField("ingress_global_timestamp",0,32),
                    BitField("egress_global_timestamp",0,32),
                    BitField("enq_timestamp",0,32),
                    BitField("enq_qdepth",0,32),
                    BitField("deq_timedelta",0,32),
                    BitField("deq_qdepth",0,32),
                    BitField("processing_time",0,32),
                    BitField("number_of_packets_for_average",0,32)
                  ]
    """any thing after this packet is extracted is padding"""

    def extract_padding(self, p):
        return "", p


class NodeCount(Packet):
    name = "nodeCount"
    fields_desc = [ShortField("id", 0),
                   ShortField("count", 0),
                   PacketListField("INT", [], InBandNetworkTelemetry, count_from=lambda pkt: (pkt.count * 1))]


class INTTOFINO:
    def __init__(self):
        self.id = 0
        # self.downlink_enq_qdepth = 0
        # self.downlink_deq_qdepth = 0
        # self.downlink_deq_timedelta = 0
        # self.downlink_processing_time = 0
        # self.uplink_enq_qdepth = 0
        # self.uplink_deq_qdepth = 0
        # self.uplink_deq_timedelta = 0
        # self.uplink_processing_time = 0
        self.queue_delay_port_137 = 0
        self.number_of_packets_for_average_port_137 = 0
        self.queue_delay_port_136 = 0
        self.number_of_packets_for_average_port_136 = 0


def handle_pkt(pkt, queues):
    if IP in pkt and pkt[IP].proto == 253 and pkt[NodeCount].count > 0:
        dataINT = INTTOFINO()
        int_id = pkt[NodeCount].id
        timestamp = perf_counter_ns()
        int_header = pkt[NodeCount].INT[-1]
        qid = int_header[InBandNetworkTelemetry].qid
        for int_pkt in pkt[NodeCount].INT:
            telemetry = int_pkt[InBandNetworkTelemetry]
            #print("INT ID: ", int_id)
            if telemetry.swid == 1: #PORTA 137
                #print(f"Queue {qid} - Downlink/WiFi")
                # dataINT.downlink_enq_qdepth = telemetry.enq_qdepth
                # dataINT.downlink_deq_qdepth = telemetry.deq_qdepth
                # dataINT.downlink_deq_timedelta = telemetry.deq_timedelta
                # dataINT.downlink_processing_time = telemetry.processing_time
                dataINT.queue_delay_port_137 = telemetry.processing_time
                dataINT.number_of_packets_for_average_port_137 = telemetry.number_of_packets_for_average
                #dataINT.queue_delay_port_136 = telemetry.processing_time
                #dataINT.number_of_packets_for_average_port_136 = telemetry.number_of_packets_for_average
                
            else: #PORTA 136 VOLTA
                #print(f"Queue {qid} - Uplink/Wired") 
                # dataINT.uplink_enq_qdepth = telemetry.enq_qdepth
                # dataINT.uplink_deq_qdepth = telemetry.deq_qdepth
                # dataINT.uplink_deq_timedelta = telemetry.deq_timedelta
                # dataINT.uplink_processing_time = telemetry.processing_time
                dataINT.queue_delay_port_136 = telemetry.processing_time
                dataINT.number_of_packets_for_average_port_136 = telemetry.number_of_packets_for_average
                #dataINT.queue_delay_port_136 = telemetry.processing_time
                #dataINT.number_of_packets_for_average_port_136 = telemetry.number_of_packets_for_average


            # '''print("Enqueue Timestamp:", telemetry.enq_timestamp)
            # print("Enqueue Queue Depth:", telemetry.enq_qdepth)
            # print("Dequeue Timedelta:", telemetry.deq_timedelta)
            # print("Dequeue Queue Depth:", telemetry.deq_qdepth)
            # if telemetry.switchID_t == 1:
            #     print("------------------------------")
            # else:
            #     print("\n")'''

            # '''print("queue_delay:", telemetry.processing_time)
            # print("number_of_packets_for_average:", telemetry.number_of_packets_for_average)
            # if telemetry.swid == 1:
            #     print("------------------------------")
            # else:
            #     print("\n")'''
            
        print("QID: ", qid)
        print("INT ID: ", int_id)
        print("Timestamp: ", timestamp)
        print("queue_delay_port_137: ", dataINT.queue_delay_port_137)
        print("number_of_packets_for_average_port_137: ", dataINT.number_of_packets_for_average_port_137)
        print("queue_delay_port_136: ", dataINT.queue_delay_port_136)
        print("number_of_packets_for_average_port_136: ", dataINT.number_of_packets_for_average_port_136)
        print()

        
        # int_df = pd.DataFrame([{'id': int_id,
        #                         'timestamp': timestamp,
        #                         'queue_delay_port_137': dataINT.queue_delay_port_137,
        #                         'number_of_packets_for_average_port_137': dataINT.number_of_packets_for_average_port_137,
        #                         'dataINT.queue_delay_port_136': dataINT.queue_delay_port_136,
        #                         'umber_of_packets_for_average_port_136': dataINT.number_of_packets_for_average_port_136,
        #                         # 'downlink enq_qdepth': dataINT.downlink_enq_qdepth,
        #                         # 'downlink deq_qdepth': dataINT.downlink_deq_qdepth,
        #                         # 'uplink enq_qdepth': dataINT.uplink_enq_qdepth,
        #                         # 'uplink deq_qdepth': dataINT.uplink_deq_qdepth
        #                        }])
        
        #CHATGPT:
        int_df = pd.DataFrame([{'id': int_id,
                        'timestamp': timestamp,
                        'queue_delay_port_137': dataINT.queue_delay_port_137,
                        'number_of_packets_for_average_port_137': dataINT.number_of_packets_for_average_port_137,
                        'queue_delay_port_136': dataINT.queue_delay_port_136,
                        'number_of_packets_for_average_port_136': dataINT.number_of_packets_for_average_port_136,
                     }])

                   
        queues[qid] = pd.concat([queues[qid], int_df], ignore_index=True)
        



def main():
    if len(sys.argv) == 3:
        int_columns = [ 'id',
                        'timestamp',
                        'queue_delay_port_137',
                        'number_of_packets_for_average_port_137',
                        'queue_delay_port_136',
                        'number_of_packets_for_average_port_136',
                      ]
        queues = []
        numq = 2 # number of queues, change when add more queues
        while numq > 0:
            queues.append(pd.DataFrame(columns=int_columns))
            numq = numq - 1
        
        iface = 'enp2s0np0' #'wlp6s0'
        bind_layers(IP, NodeCount, proto=253)
        bind_layers(Ether, IP)
        timeEx = int(sys.argv[2])

        print("Waiting packets...")
        sniff(iface=iface, prn=lambda x: handle_pkt(x, queues), timeout=timeEx)

        print("Saving collect INT data...")
        experiment = sys.argv[1]
        #path = f'../scenarios/{experiment}'
        path = 'data'
        nq_saved = 0
        for qid, queue in enumerate(queues):
            if len(queue.index) > 0:
                filename = f'receiver_queue{qid}.csv'
                queue.to_csv(f'{path}/{filename}')
                nq_saved = nq_saved + 1
        print(f"Successfully saved {nq_saved} queues")
    else:
        print("2 arguments are expected: ID and duration (in seconds) of the experiment...")    


if __name__ == '__main__':
    main()
