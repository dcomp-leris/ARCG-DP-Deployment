#!/usr/bin/python3

import os
import sys
import pdb
import time

#
# This is optional if you use proper PYTHONPATH
#
##########3NAO PEGAR ESSE CAMINHO?
SDE_INSTALL   = os.environ['SDE_INSTALL']
SDE_PYTHON2   = os.path.join(SDE_INSTALL, 'lib', 'python2.7', 'site-packages')
sys.path.append(SDE_PYTHON2)
sys.path.append(os.path.join(SDE_PYTHON2, 'tofino'))

PYTHON3_VER   = '{}.{}'.format(
    sys.version_info.major,
    sys.version_info.minor)
SDE_PYTHON3   = os.path.join(SDE_INSTALL, 'lib', 'python' + PYTHON3_VER,
                             'site-packages')
sys.path.append(SDE_PYTHON3)
sys.path.append(os.path.join(SDE_PYTHON3, 'tofino'))
sys.path.append(os.path.join(SDE_PYTHON3, 'tofino', 'bfrt_grpc'))

# Here is the most important module
import bfrt_grpc.client as gc

#
# Connect to the BF Runtime Server
#
for bfrt_client_id in range(10):
    try:
        interface = gc.ClientInterface(
            grpc_addr = 'localhost:50052',
            client_id = bfrt_client_id,
            device_id = 0,
            num_tries = 1)
        print('Connected to BF Runtime Server as client', bfrt_client_id)
        break;
    except:
        print('Could not connect to BF Runtime server')
        quit

#
# Get the information about the running program
#
bfrt_info = interface.bfrt_info_get()
print('The target runs the program ', bfrt_info.p4_name_get())

#
# Establish that you are using this program on the given connection
#
if bfrt_client_id == 0:
    interface.bind_pipeline_config(bfrt_info.p4_name_get())

################### You can now use BFRT CLIENT ###########################




# This is just an example. Put in your own code
from tabulate import tabulate

# Print the list of tables in the "pipe" node
dev_tgt = gc.Target(0, pipe_id=1)


### Reading a register ###
# Listar todos os métodos e atributos de bfrt_info
# print(dir(bfrt_info))
sorted_tables = bfrt_info.table_list_sorted
# print(sorted_tables)

#print(bfrt_info.table_list)
# table_counter_packets_frame = bfrt_info.table_get("pipe.SwitchIngress.counter_packets_frame")
table_flow_id_reg = bfrt_info.table_get("pipe.SwitchIngress.flow_id_reg")
table_packet_size_reg = bfrt_info.table_get("pipe.SwitchIngress.packet_size_reg")
table_ipg_cloned_packets_reg = bfrt_info.table_get("pipe.SwitchIngress.ipg_cloned_packets_reg")
table_frame_size_reg = bfrt_info.table_get("pipe.SwitchIngress.frame_size_reg")
table_ifg_reg = bfrt_info.table_get("pipe.SwitchIngress.ifg_reg")
# table_drop_cloned_pkt = bfrt_info.table_get("pipe.SwitchIngress.drop_cloned_pkt")
# table_queue_delay = bfrt_info.table_get("pipe.SwitchIngress.queue_delay")
# table_counter1_reg = bfrt_info.table_get("pipe.SwitchIngress.counter1_reg")
# table_counter2_reg = bfrt_info.table_get("pipe.SwitchIngress.counter2_reg")
# table_counter3_reg = bfrt_info.table_get("pipe.SwitchIngress.counter3_reg")
# table_metadata_classify_reg = bfrt_info.table_get("pipe.SwitchIngress.metadata_classify_reg")
table_metadata_classT1 = bfrt_info.table_get("pipe.SwitchIngress.metadata_classT1")
table_metadata_classT2 = bfrt_info.table_get("pipe.SwitchIngress.metadata_classT2")
table_metadata_classT3 = bfrt_info.table_get("pipe.SwitchIngress.metadata_classT3")
table_metadata_classT4 = bfrt_info.table_get("pipe.SwitchIngress.metadata_classT4")
table_metadata_classT5 = bfrt_info.table_get("pipe.SwitchIngress.metadata_classT5")


# Alireza added 
table_ingress_host_ifg_reg = bfrt_info.table_get("pipe.SwitchIngress.ingress_host_ifg_reg")
# help(table_drop_cloned_pkt)


# tm_table_sched_shaping = bfrt_info.table_get("tf2.tm.queue.sched_shaping")
# tm_table_sched_cfg = bfrt_info.table_get("tf2.tm.queue.sched_cfg")
# table_totalPkts_IPG = bfrt_info.table_get("pipe.Egress.totalPkts_IPG")
# table_IPG_reg = bfrt_info.table_get("pipe.Egress.IPG_reg")
# table_packet_size_reg = bfrt_info.table_get("pipe.Egress.packet_size_reg")
#for (data, key) in table_totalPkts_IPG.entry_get(dev_tgt, []):
#    print(key.to_dict(), data.to_dict())
# help(bfrt_info.table_get)
#print(dir(bfrt_info.table_get))
# traffic_manager = bfrt_info.table_get("tm")

#help(tm_table_sched_shaping.make_key)
 


#only CG values (positions 4 = port 136, positions 5 = port 137)
# key_totalPkts_136_Classic = table_totalPkts_IPG.make_key([gc.KeyTuple('$REGISTER_INDEX', 0)])
# key_totalPkts_137_Classic = table_totalPkts_IPG.make_key([gc.KeyTuple('$REGISTER_INDEX', 1)])
# key_totalPkts_136_L4S = table_totalPkts_IPG.make_key([gc.KeyTuple('$REGISTER_INDEX', 2)])
# key_totalPkts_137_L4S = table_totalPkts_IPG.make_key([gc.KeyTuple('$REGISTER_INDEX', 3)])
# key_totalPkts_136_CG = table_totalPkts_IPG.make_key([gc.KeyTuple('$REGISTER_INDEX', 4)])
# key_totalPkts_137_CG = table_totalPkts_IPG.make_key([gc.KeyTuple('$REGISTER_INDEX', 5)])

# key_IPG_reg_136_Classic = table_IPG_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 0)])
# key_IPG_reg_137_Classic = table_IPG_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 1)])
# key_IPG_reg_136_L4S = table_IPG_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 2)])
# key_IPG_reg_137_L4S = table_IPG_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 3)])
# key_IPG_reg_136_CG = table_IPG_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 4)])
# key_IPG_reg_137_CG = table_IPG_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 5)])

# key_packet_size_reg_136_Classic = table_packet_size_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 0)])
# key_packet_size_reg_137_Classic = table_packet_size_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 1)])
# key_packet_size_reg_136_L4S = table_packet_size_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 2)])
# key_packet_size_reg_137_L4S = table_packet_size_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 3)])
# key_packet_size_reg_136_CG = table_packet_size_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 4)])
# key_packet_size_reg_137_CG = table_packet_size_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 5)])

#test_key  = table_totalPkts_IPG.make_key([gc.KeyTuple('$REGISTER_INDEX', 0)])
#test_key  = table_totalPkts_IPG.make_key([gc.KeyTuple('$REGISTER_INDEX', 3)])

#print(dir(bfrt_info))


# print("FlowID, PS, IPG, FS, IFG, Pkt#_FLOW, Frm#, Qdelay_SUM")
# print("FlowID, t1, t2, t3, t4, t5")
print("FlowID, PS, IPG, FS, IFG t1, t2, t3, t4, t5, host_ifg")

while True:

    #FLOWID
    key_flow_id_reg = table_flow_id_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 0)])
    flow_id_reg_read_result = table_flow_id_reg.entry_get(dev_tgt, [key_flow_id_reg], {"from_hw": True}) #, "print_zero": False})
    flow_id_reg_entry_data, _ = next(flow_id_reg_read_result)
    flow_id_reg_entry_dict = flow_id_reg_entry_data.to_dict()
    flow_id_reg_f1_value = flow_id_reg_entry_dict["SwitchIngress.flow_id_reg.f1"]
    flow_id_reg_value = flow_id_reg_f1_value[0]
    #print(flow_id_reg_value)

    #t1
    key_metadata_classT1 = table_metadata_classT1.make_key([gc.KeyTuple('$REGISTER_INDEX', flow_id_reg_value)])
    metadata_classT1_read_result = table_metadata_classT1.entry_get(dev_tgt, [key_metadata_classT1], {"from_hw": True}) #, "print_zero": False})
    metadata_classT1_entry_data, _ = next(metadata_classT1_read_result)
    metadata_classT1_entry_dict = metadata_classT1_entry_data.to_dict()
    metadata_classT1_f1_value = metadata_classT1_entry_dict["SwitchIngress.metadata_classT1.f1"]
    metadata_classT1_value = metadata_classT1_f1_value[0]

    #t2
    key_metadata_classT2 = table_metadata_classT2.make_key([gc.KeyTuple('$REGISTER_INDEX', flow_id_reg_value)])
    metadata_classT2_read_result = table_metadata_classT2.entry_get(dev_tgt, [key_metadata_classT2], {"from_hw": True}) #, "print_zero": False})
    metadata_classT2_entry_data, _ = next(metadata_classT2_read_result)
    metadata_classT2_entry_dict = metadata_classT2_entry_data.to_dict()
    metadata_classT2_f1_value = metadata_classT2_entry_dict["SwitchIngress.metadata_classT2.f1"]
    metadata_classT2_value = metadata_classT2_f1_value[0]

    #t3
    key_metadata_classT3 = table_metadata_classT3.make_key([gc.KeyTuple('$REGISTER_INDEX', flow_id_reg_value)])
    metadata_classT3_read_result = table_metadata_classT3.entry_get(dev_tgt, [key_metadata_classT3], {"from_hw": True}) #, "print_zero": False})
    metadata_classT3_entry_data, _ = next(metadata_classT3_read_result)
    metadata_classT3_entry_dict = metadata_classT3_entry_data.to_dict()
    metadata_classT3_f1_value = metadata_classT3_entry_dict["SwitchIngress.metadata_classT3.f1"]
    metadata_classT3_value = metadata_classT3_f1_value[0]

    #t4
    key_metadata_classT4 = table_metadata_classT4.make_key([gc.KeyTuple('$REGISTER_INDEX', flow_id_reg_value)])
    metadata_classT4_read_result = table_metadata_classT4.entry_get(dev_tgt, [key_metadata_classT4], {"from_hw": True}) #, "print_zero": False})
    metadata_classT4_entry_data, _ = next(metadata_classT4_read_result)
    metadata_classT4_entry_dict = metadata_classT4_entry_data.to_dict()
    metadata_classT4_f1_value = metadata_classT4_entry_dict["SwitchIngress.metadata_classT4.f1"]
    metadata_classT4_value = metadata_classT4_f1_value[0]

    #t5
    key_metadata_classT5 = table_metadata_classT5.make_key([gc.KeyTuple('$REGISTER_INDEX', flow_id_reg_value)])
    metadata_classT5_read_result = table_metadata_classT5.entry_get(dev_tgt, [key_metadata_classT5], {"from_hw": True}) #, "print_zero": False})
    metadata_classT5_entry_data, _ = next(metadata_classT5_read_result)
    metadata_classT5_entry_dict = metadata_classT5_entry_data.to_dict()
    metadata_classT5_f1_value = metadata_classT5_entry_dict["SwitchIngress.metadata_classT5.f1"]
    metadata_classT5_value = metadata_classT5_f1_value[0]


    

    #PACKET SIZE
    key_packet_size_reg = table_packet_size_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', flow_id_reg_value)])
    packet_size_reg_read_result = table_packet_size_reg.entry_get(dev_tgt, [key_packet_size_reg], {"from_hw": True}) #, "print_zero": False})
    packet_size_reg_entry_data, _ = next(packet_size_reg_read_result)
    packet_size_reg_entry_dict = packet_size_reg_entry_data.to_dict()
    packet_size_reg_f1_value = packet_size_reg_entry_dict["SwitchIngress.packet_size_reg.f1"]
    packet_size_reg_value = packet_size_reg_f1_value[0]

    # #IPG
    key_ipg_cloned_packets_reg = table_ipg_cloned_packets_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', flow_id_reg_value)])
    ipg_cloned_packets_reg_read_result = table_ipg_cloned_packets_reg.entry_get(dev_tgt, [key_ipg_cloned_packets_reg], {"from_hw": True}) #, "print_zero": False})
    ipg_cloned_packets_reg_entry_data, _ = next(ipg_cloned_packets_reg_read_result)
    ipg_cloned_packets_reg_entry_dict = ipg_cloned_packets_reg_entry_data.to_dict()
    ipg_cloned_packets_reg_f1_value = ipg_cloned_packets_reg_entry_dict["SwitchIngress.ipg_cloned_packets_reg.f1"]
    ipg_cloned_packets_reg_value = ipg_cloned_packets_reg_f1_value[0]

    # #FRAME SIZE
    key_frame_size_reg = table_frame_size_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', flow_id_reg_value)])
    frame_size_reg_read_result = table_frame_size_reg.entry_get(dev_tgt, [key_frame_size_reg], {"from_hw": True}) #, "print_zero": False})
    frame_size_reg_entry_data, _ = next(frame_size_reg_read_result)
    frame_size_reg_entry_dict = frame_size_reg_entry_data.to_dict()
    frame_size_reg_f1_value = frame_size_reg_entry_dict["SwitchIngress.frame_size_reg.f1"]
    frame_size_reg_value = frame_size_reg_f1_value[0]

    # #ifg
    # print(dir(table_ifg_reg))
    key_ifg_reg = table_ifg_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', flow_id_reg_value)])
    ifg_reg_read_result = table_ifg_reg.entry_get(dev_tgt, [key_ifg_reg], {"from_hw": True}) #, "print_zero": False})
    ifg_reg_entry_data, _ = next(ifg_reg_read_result)
    ifg_reg_entry_dict = ifg_reg_entry_data.to_dict()
    ifg_reg_f1_value = ifg_reg_entry_dict["SwitchIngress.ifg_reg.f1"]
    ifg_reg_value = ifg_reg_f1_value[0]


    # Alireza added
    #host_ifg
    key_ingress_host_ifg_reg = table_ingress_host_ifg_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', flow_id_reg_value)])
    ingress_host_ifg_reg_read_result = table_ingress_host_ifg_reg.entry_get(dev_tgt, [key_ingress_host_ifg_reg], {"from_hw": True}) #, "print_zero": False})
    ingress_host_ifg_reg_entry_data, _ = next(ingress_host_ifg_reg_read_result)
    ingress_host_ifg_reg_entry_dict = ingress_host_ifg_reg_entry_data.to_dict()
    ingress_host_ifg_reg_f1_value = ingress_host_ifg_reg_entry_dict["SwitchIngress.ingress_host_ifg_reg.f1"]
    ingress_host_ifg_reg_value = ingress_host_ifg_reg_f1_value[0]
    # Alireza Added




    # #counter_packets PER FLOWWWWWWWWWWWWWW
    # # print("oi")
    # # print(dir(table_ifg_reg))  # Lista os campos da chave da tabela
    # # print(dir(table_drop_cloned_pkt.info))  # Lista os campos da chave da tabela
    # # print(table_drop_cloned_pkt.info.data_fields)  # Lista os campos de dados

    # # print(dir(table_drop_cloned_pkt))

    # key_drop_cloned_pkt = table_drop_cloned_pkt.make_key([gc.KeyTuple('$REGISTER_INDEX', flow_id_reg_value)])
    # drop_cloned_pkt_read_result = table_drop_cloned_pkt.entry_get(dev_tgt, [key_drop_cloned_pkt], {"from_hw": True}) #, "print_zero": False})
    # drop_cloned_pkt_entry_data, _ = next(drop_cloned_pkt_read_result)
    # drop_cloned_pkt_entry_dict = drop_cloned_pkt_entry_data.to_dict()
    # drop_cloned_pkt_f1_value = drop_cloned_pkt_entry_dict["SwitchIngress.drop_cloned_pkt.f1"]
    # drop_cloned_pkt_value = drop_cloned_pkt_f1_value[0]

    # #frame_counter
    # key_counter_packets_frame = table_counter_packets_frame.make_key([gc.KeyTuple('$REGISTER_INDEX', flow_id_reg_value)])
    # counter_packets_frame_read_result = table_counter_packets_frame.entry_get(dev_tgt, [key_counter_packets_frame], {"from_hw": True}) #, "print_zero": False})
    # counter_packets_frame_entry_data, _ = next(counter_packets_frame_read_result)
    # counter_packets_frame_entry_dict = counter_packets_frame_entry_data.to_dict()
    # counter_packets_frame_f1_value = counter_packets_frame_entry_dict["SwitchIngress.counter_packets_frame.f1"]
    # counter_packets_frame_value = counter_packets_frame_f1_value[0]

    # #queue_delay
    # key_queue_delay = table_queue_delay.make_key([gc.KeyTuple('$REGISTER_INDEX', 0)])
    # queue_delay_read_result = table_queue_delay.entry_get(dev_tgt, [key_queue_delay], {"from_hw": True}) #, "print_zero": False})
    # queue_delay_entry_data, _ = next(queue_delay_read_result)
    # queue_delay_entry_dict = queue_delay_entry_data.to_dict()
    # queue_delay_f1_value = queue_delay_entry_dict["SwitchIngress.queue_delay.f1"]
    # queue_delay_value = queue_delay_f1_value[0]


    # print("FlowID, PS, IPG, FS, IFG, Pkt#_FLOW, Frm#, Qdelay_SUM")

    #print("FlowID, t1, t2, t3, t4, t5")
    #print("FlowID, PS, IPG, FS, IFG t1, t2, t3, t4, t5")
    print(f"{flow_id_reg_value}, {packet_size_reg_value}, {ipg_cloned_packets_reg_value}, {frame_size_reg_value}, {ifg_reg_value}, {metadata_classT1_value}, {metadata_classT2_value}, {metadata_classT3_value}, {metadata_classT4_value}, {metadata_classT5_value}")


    #print(f"{flow_id_reg_value}, {packet_size_reg_value}, {ipg_cloned_packets_reg_value}, {frame_size_reg_value}, {ifg_reg_value}, {drop_cloned_pkt_value}, {counter_packets_frame_value}, {queue_delay_value}")



    #PACKETS PER FRAME AND NUMBER OF FRAMES
    #key_counter_packets_frame


    #TOTAL PKTS
    #Classic
    #136
    # totalPkts_IPG_136_Classic_read_result = table_totalPkts_IPG.entry_get(dev_tgt, [key_totalPkts_136_Classic], {"from_hw": True}) #, "print_zero": False})
    # totalPkts_IPG_136_Classic_entry_data, _ = next(totalPkts_IPG_136_Classic_read_result)
    # totalPkts_IPG_136_Classic_entry_dict = totalPkts_IPG_136_Classic_entry_data.to_dict()
    # #print(data_dict0)
    # totalPkts_IPG_136_Classic_f1_value = totalPkts_IPG_136_Classic_entry_dict["Egress.totalPkts_IPG.f1"]
    # totalPkts_IPG_136_Classic_value = totalPkts_IPG_136_Classic_f1_value[0]

    #137
    # totalPkts_IPG_137_Classic_read_result = table_totalPkts_IPG.entry_get(dev_tgt, [key_totalPkts_137_Classic], {"from_hw": True}) #, "print_zero": False})
    # totalPkts_IPG_137_Classic_entry_data, _ = next(totalPkts_IPG_137_Classic_read_result)
    # totalPkts_IPG_137_Classic_entry_dict = totalPkts_IPG_137_Classic_entry_data.to_dict()
    # #print(data_dict0)
    # totalPkts_IPG_137_Classic_f1_value = totalPkts_IPG_137_Classic_entry_dict["Egress.totalPkts_IPG.f1"]
    # totalPkts_IPG_137_Classic_value = totalPkts_IPG_137_Classic_f1_value[0]

    #L4S
    #136
    # totalPkts_IPG_136_L4S_read_result = table_totalPkts_IPG.entry_get(dev_tgt, [key_totalPkts_136_L4S], {"from_hw": True}) #, "print_zero": False})
    # totalPkts_IPG_136_L4S_entry_data, _ = next(totalPkts_IPG_136_L4S_read_result)
    # totalPkts_IPG_136_L4S_entry_dict = totalPkts_IPG_136_L4S_entry_data.to_dict()
    # #print(data_dict0)
    # totalPkts_IPG_136_L4S_f1_value = totalPkts_IPG_136_L4S_entry_dict["Egress.totalPkts_IPG.f1"]
    # totalPkts_IPG_136_L4S_value = totalPkts_IPG_136_L4S_f1_value[0]

    #137
    # totalPkts_IPG_137_L4S_read_result = table_totalPkts_IPG.entry_get(dev_tgt, [key_totalPkts_137_L4S], {"from_hw": True}) #, "print_zero": False})
    # totalPkts_IPG_137_L4S_entry_data, _ = next(totalPkts_IPG_137_L4S_read_result)
    # totalPkts_IPG_137_L4S_entry_dict = totalPkts_IPG_137_L4S_entry_data.to_dict()
    # #print(data_dict0)
    # totalPkts_IPG_137_L4S_f1_value = totalPkts_IPG_137_L4S_entry_dict["Egress.totalPkts_IPG.f1"]
    # totalPkts_IPG_137_L4S_value = totalPkts_IPG_137_L4S_f1_value[0]

    #CG
    #136
    # totalPkts_IPG_136_CG_read_result = table_totalPkts_IPG.entry_get(dev_tgt, [key_totalPkts_136_CG], {"from_hw": True}) #, "print_zero": False})
    # totalPkts_IPG_136_CG_entry_data, _ = next(totalPkts_IPG_136_CG_read_result)
    # totalPkts_IPG_136_CG_entry_dict = totalPkts_IPG_136_CG_entry_data.to_dict()
    # #print(data_dict0)
    # totalPkts_IPG_136_CG_f1_value = totalPkts_IPG_136_CG_entry_dict["Egress.totalPkts_IPG.f1"]
    # totalPkts_IPG_136_CG_value = totalPkts_IPG_136_CG_f1_value[0]

    #137
    # totalPkts_IPG_137_CG_read_result = table_totalPkts_IPG.entry_get(dev_tgt, [key_totalPkts_137_CG], {"from_hw": True}) #, "print_zero": False})
    # totalPkts_IPG_137_CG_entry_data, _ = next(totalPkts_IPG_137_CG_read_result)
    # totalPkts_IPG_137_CG_entry_dict = totalPkts_IPG_137_CG_entry_data.to_dict()
    # #print(data_dict0)
    # totalPkts_IPG_137_CG_f1_value = totalPkts_IPG_137_CG_entry_dict["Egress.totalPkts_IPG.f1"]
    # totalPkts_IPG_137_CG_value = totalPkts_IPG_137_CG_f1_value[0]

    ###################
    #IPG
    #Classic
    #136
    # IPG_reg_136_Classic_read_result = table_IPG_reg.entry_get(dev_tgt, [key_IPG_reg_136_Classic], {"from_hw": True}) #, "print_zero": False})
    # IPG_reg_136_Classic_entry_data, _ = next(IPG_reg_136_Classic_read_result)
    # IPG_reg_136_Classic_entry_dict = IPG_reg_136_Classic_entry_data.to_dict()
    # #print(IPG_reg_136_Classic_entry_dict)
    # IPG_reg_136_Classic_f1_value = IPG_reg_136_Classic_entry_dict["Egress.IPG_reg.f1"]
    # IPG_reg_136_Classic_value = IPG_reg_136_Classic_f1_value[0]

    #137
    # IPG_reg_137_Classic_read_result = table_IPG_reg.entry_get(dev_tgt, [key_IPG_reg_137_Classic], {"from_hw": True}) #, "print_zero": False})
    # IPG_reg_137_Classic_entry_data, _ = next(IPG_reg_137_Classic_read_result)
    # IPG_reg_137_Classic_entry_dict = IPG_reg_137_Classic_entry_data.to_dict()
    # #print(data_dict0)
    # IPG_reg_137_Classic_f1_value = IPG_reg_137_Classic_entry_dict["Egress.IPG_reg.f1"]
    # IPG_reg_137_Classic_value = IPG_reg_137_Classic_f1_value[0]

    #L4S
    #136
    # IPG_reg_136_L4S_read_result = table_IPG_reg.entry_get(dev_tgt, [key_IPG_reg_136_L4S], {"from_hw": True}) #, "print_zero": False})
    # IPG_reg_136_L4S_entry_data, _ = next(IPG_reg_136_L4S_read_result)
    # IPG_reg_136_L4S_entry_dict = IPG_reg_136_L4S_entry_data.to_dict()
    # #print(IPG_reg_136_L4S_entry_dict)
    # IPG_reg_136_L4S_f1_value = IPG_reg_136_L4S_entry_dict["Egress.IPG_reg.f1"]
    # IPG_reg_136_L4S_value = IPG_reg_136_L4S_f1_value[0]

    #137
    # IPG_reg_137_L4S_read_result = table_IPG_reg.entry_get(dev_tgt, [key_IPG_reg_137_L4S], {"from_hw": True}) #, "print_zero": False})
    # IPG_reg_137_L4S_entry_data, _ = next(IPG_reg_137_L4S_read_result)
    # IPG_reg_137_L4S_entry_dict = IPG_reg_137_L4S_entry_data.to_dict()
    # #print(data_dict0)
    # IPG_reg_137_L4S_f1_value = IPG_reg_137_L4S_entry_dict["Egress.IPG_reg.f1"]
    # IPG_reg_137_L4S_value = IPG_reg_137_L4S_f1_value[0]

    # #L4S
    # #136
    # IPG_reg_136_CG_read_result = table_IPG_reg.entry_get(dev_tgt, [key_IPG_reg_136_CG], {"from_hw": True}) #, "print_zero": False})
    # IPG_reg_136_CG_entry_data, _ = next(IPG_reg_136_CG_read_result)
    # IPG_reg_136_CG_entry_dict = IPG_reg_136_CG_entry_data.to_dict()
    # #print(IPG_reg_136_CG_entry_dict)
    # IPG_reg_136_CG_f1_value = IPG_reg_136_CG_entry_dict["Egress.IPG_reg.f1"]
    # IPG_reg_136_CG_value = IPG_reg_136_CG_f1_value[0]

    #137
    # IPG_reg_137_CG_read_result = table_IPG_reg.entry_get(dev_tgt, [key_IPG_reg_137_CG], {"from_hw": True}) #, "print_zero": False})
    # IPG_reg_137_CG_entry_data, _ = next(IPG_reg_137_CG_read_result)
    # IPG_reg_137_CG_entry_dict = IPG_reg_137_CG_entry_data.to_dict()
    # #print(data_dict0)
    # IPG_reg_137_CG_f1_value = IPG_reg_137_CG_entry_dict["Egress.IPG_reg.f1"]
    # IPG_reg_137_CG_value = IPG_reg_137_CG_f1_value[0]

    ####################
    #PACKET SIZE
    #Classic
    #136
    # packet_size_reg_136_Classic_read_result = table_packet_size_reg.entry_get(dev_tgt, [key_packet_size_reg_136_Classic], {"from_hw": True}) #, "print_zero": False})
    # packet_size_reg_136_Classic_entry_data, _ = next(packet_size_reg_136_Classic_read_result)
    # packet_size_reg_136_Classic_entry_dict = packet_size_reg_136_Classic_entry_data.to_dict()
    # #print(packet_size_reg_136_Classic_entry_dict)
    # packet_size_reg_136_Classic_f1_value = packet_size_reg_136_Classic_entry_dict["Egress.packet_size_reg.f1"]
    # packet_size_reg_136_Classic_value = packet_size_reg_136_Classic_f1_value[0]

    # #137
    # packet_size_reg_137_Classic_read_result = table_packet_size_reg.entry_get(dev_tgt, [key_packet_size_reg_137_Classic], {"from_hw": True}) #, "print_zero": False})
    # packet_size_reg_137_Classic_entry_data, _ = next(packet_size_reg_137_Classic_read_result)
    # packet_size_reg_137_Classic_entry_dict = packet_size_reg_137_Classic_entry_data.to_dict()
    # #print(packet_size_reg_137_Classic_entry_dict)
    # packet_size_reg_137_Classic_f1_value = packet_size_reg_137_Classic_entry_dict["Egress.packet_size_reg.f1"]
    # packet_size_reg_137_Classic_value = packet_size_reg_137_Classic_f1_value[0]

    # #L4S
    # #136
    # packet_size_reg_136_L4S_read_result = table_packet_size_reg.entry_get(dev_tgt, [key_packet_size_reg_136_L4S], {"from_hw": True}) #, "print_zero": False})
    # packet_size_reg_136_L4S_entry_data, _ = next(packet_size_reg_136_L4S_read_result)
    # packet_size_reg_136_L4S_entry_dict = packet_size_reg_136_L4S_entry_data.to_dict()
    # #print(packet_size_reg_136_L4S_entry_dict)
    # packet_size_reg_136_L4S_f1_value = packet_size_reg_136_L4S_entry_dict["Egress.packet_size_reg.f1"]
    # packet_size_reg_136_L4S_value = packet_size_reg_136_L4S_f1_value[0]

    # #137
    # packet_size_reg_137_L4S_read_result = table_packet_size_reg.entry_get(dev_tgt, [key_packet_size_reg_137_L4S], {"from_hw": True}) #, "print_zero": False})
    # packet_size_reg_137_L4S_entry_data, _ = next(packet_size_reg_137_L4S_read_result)
    # packet_size_reg_137_L4S_entry_dict = packet_size_reg_137_L4S_entry_data.to_dict()
    # #print(packet_size_reg_137_L4S_entry_dict)
    # packet_size_reg_137_L4S_f1_value = packet_size_reg_137_L4S_entry_dict["Egress.packet_size_reg.f1"]
    # packet_size_reg_137_L4S_value = packet_size_reg_137_L4S_f1_value[0]


    # #CG
    # #136
    # packet_size_reg_136_CG_read_result = table_packet_size_reg.entry_get(dev_tgt, [key_packet_size_reg_136_CG], {"from_hw": True}) #, "print_zero": False})
    # packet_size_reg_136_CG_entry_data, _ = next(packet_size_reg_136_CG_read_result)
    # packet_size_reg_136_CG_entry_dict = packet_size_reg_136_CG_entry_data.to_dict()
    # #print(packet_size_reg_136_CG_entry_dict)
    # packet_size_reg_136_CG_f1_value = packet_size_reg_136_CG_entry_dict["Egress.packet_size_reg.f1"]
    # packet_size_reg_136_CG_value = packet_size_reg_136_CG_f1_value[0]

    # #137
    # packet_size_reg_137_CG_read_result = table_packet_size_reg.entry_get(dev_tgt, [key_packet_size_reg_137_CG], {"from_hw": True}) #, "print_zero": False})
    # packet_size_reg_137_CG_entry_data, _ = next(packet_size_reg_137_CG_read_result)
    # packet_size_reg_137_CG_entry_dict = packet_size_reg_137_CG_entry_data.to_dict()
    # #print(packet_size_reg_137_CG_entry_dict)
    # packet_size_reg_137_CG_f1_value = packet_size_reg_137_CG_entry_dict["Egress.packet_size_reg.f1"]
    # packet_size_reg_137_CG_value = packet_size_reg_137_CG_f1_value[0]



    # #sleep for 5ms
    # #time.sleep(0.005)
    # #print(totalPkts_IPG_136_CG_f1_value)
    # # print(totalPkts_IPG_136_CG_value)
    # # print(totalPkts_IPG_137_CG_value)
    
    
    
    # wait_time = 10

    # min_threshold = 2 #MILISECONDS
    # coeficient = 10**6

    # #CLASSIC
    # if IPG_reg_136_Classic_value == 0 :
    #     estimated_rate_136_Classic = 0
    # else:
    #     estimated_rate_136_Classic = ((((coeficient * min_threshold)/IPG_reg_136_Classic_value) * 10**3) * packet_size_reg_136_Classic_value* 8)/wait_time #10 elevado a 9
    # if IPG_reg_137_Classic_value == 0:
    #     estimated_rate_137_Classic = 0
    # else:
    #     estimated_rate_137_Classic = ((((coeficient * min_threshold)/IPG_reg_137_Classic_value) * 10**3)*packet_size_reg_137_Classic_value* 8)/wait_time #10 elevado a 9
    # #L4S
    # if IPG_reg_136_L4S_value == 0:
    #     estimated_rate_136_L4S = 0
    # else:
    #     estimated_rate_136_L4S = ((((coeficient * min_threshold)/IPG_reg_136_L4S_value) * 10**3)*packet_size_reg_136_L4S_value * 8)/wait_time #10 elevado a 9
    # if IPG_reg_137_L4S_value == 0:
    #     estimated_rate_137_L4S = 0
    # else:
    #     estimated_rate_137_L4S = ((((coeficient * min_threshold)/IPG_reg_137_L4S_value) * 10**3)*packet_size_reg_137_L4S_value * 8)/wait_time #10 elevado a 9
    # #CG
    # if IPG_reg_136_CG_value == 0:
    #     estimated_rate_136_CG = 0
    # else:
    #     estimated_rate_136_CG = ((((coeficient * min_threshold)/IPG_reg_136_CG_value) * 10**3)*packet_size_reg_136_CG_value * 8)/wait_time #10 elevado a 9
    # if IPG_reg_137_CG_value == 0:
    #     estimated_rate_137_CG = 0
    # else:
    #     estimated_rate_137_CG = ((((coeficient * min_threshold)/IPG_reg_137_CG_value) * 10**3)*packet_size_reg_137_CG_value * 8)/wait_time #10 elevado a 6


    
        
    # key_sched_shaping_136_classic = tm_table_sched_shaping.make_key([
    #         gc.KeyTuple("pg_id", 1),           # Valor para 'pg_id'
    #         gc.KeyTuple("pg_queue", 0)        # Valor para 'pg_queue'
    #     ])

    # key_sched_shaping_136_L4S = tm_table_sched_shaping.make_key([
    #     gc.KeyTuple("pg_id", 1),           # Valor para 'pg_id'
    #     gc.KeyTuple("pg_queue", 1)        # Valor para 'pg_queue'
    # ])

    # key_sched_shaping_136_CG = tm_table_sched_shaping.make_key([
    #     gc.KeyTuple("pg_id", 1),           # Valor para 'pg_id'
    #     gc.KeyTuple("pg_queue", 2)        # Valor para 'pg_queue'
    # ])

    # key_sched_shaping_137_classic = tm_table_sched_shaping.make_key([
    #     gc.KeyTuple("pg_id", 1),           # Valor para 'pg_id'
    #     gc.KeyTuple("pg_queue", 16)        # Valor para 'pg_queue'
    # ])

    # key_sched_shaping_137_L4S = tm_table_sched_shaping.make_key([
    #     gc.KeyTuple("pg_id", 1),           # Valor para 'pg_id'
    #     gc.KeyTuple("pg_queue", 17)        # Valor para 'pg_queue'
    # ])

    # key_sched_shaping_137_CG = tm_table_sched_shaping.make_key([
    #     gc.KeyTuple("pg_id", 1),           # Valor para 'pg_id'
    #     gc.KeyTuple("pg_queue", 18)        # Valor para 'pg_queue'
    # ])
    # bandwidth = 100000
    # min_rate_everyone = 10000
    # rate_136_L4S = round(max(min_rate_everyone, estimated_rate_136_L4S))
    # rate_137_L4S = round(max(min_rate_everyone, estimated_rate_137_L4S))
    
    # rate_136_Classic = round(max(min_rate_everyone, estimated_rate_136_Classic))
    # rate_137_Classic = round(max(min_rate_everyone, estimated_rate_136_Classic))

    # rate_136_CG = round(max(min_rate_everyone, estimated_rate_136_CG, (bandwidth - rate_136_L4S - rate_136_Classic)))
    # rate_137_CG = round(max(min_rate_everyone, estimated_rate_137_CG, (bandwidth - rate_137_L4S - rate_137_Classic)))


    # print(f"Classic:")
    # print(f"Port 136:")
    # print(f"IPG: {IPG_reg_136_Classic_value}")
    # print(f"Number of packets: {totalPkts_IPG_136_Classic_value}")
    
    # print(f"Estimated rate: {estimated_rate_136_Classic}")
    # print(f"Real rate: {rate_136_Classic}")
    # print(f"Port 137:")
    # print(f"IPG: {IPG_reg_137_Classic_value}")
    # print(f"Number of packets: {totalPkts_IPG_137_Classic_value}")
    # print(f"Estimated rate: {estimated_rate_137_Classic}")
    # print(f"Real rate: {rate_137_Classic}")
    # print("##")
    # print("L4S:")
    # print(f"Port 136:")
    # print(f"IPG: {IPG_reg_136_L4S_value}")
    # print(f"Number of packets: {totalPkts_IPG_136_L4S_value}")
    # print(f"Estimated rate: {estimated_rate_136_L4S}")
    # print(f"Real rate: {rate_136_L4S}")
    # print(f"Port 137:")
    # print(f"IPG: {IPG_reg_137_L4S_value}")
    # print(f"Number of packets: {totalPkts_IPG_137_L4S_value}")
    # print(f"Estimated rate: {estimated_rate_137_L4S}")
    # print(f"Real rate: {rate_137_L4S}")
    # print("##")
    # print("CG:")
    # print(f"Port 136:")
    # print(f"IPG: {IPG_reg_136_CG_value}")
    # print(f"Number of packets: {totalPkts_IPG_136_CG_value}")
    # print(f"Estimated rate: {estimated_rate_136_CG}")
    # print(f"Real rate: {rate_136_CG}")
    # print(f"Port 137:")
    # print(f"IPG: {IPG_reg_137_CG_value}")
    # print(f"Number of packets: {totalPkts_IPG_137_CG_value}")
    # print(f"Estimated rate: {estimated_rate_137_CG}")
    # print(f"Real rate: {rate_137_CG}")



    #RESET

    # key_queue_delay = [
    #     table_queue_delay.make_key([gc.KeyTuple('$REGISTER_INDEX', 0)])
    # ]

    # data_reset_queue_delay = [
    #     table_queue_delay.make_data([gc.DataTuple('SwitchIngress.queue_delay.f1', 0)])
    # ]

    # table_queue_delay.entry_mod(dev_tgt, key_list=key_queue_delay, data_list=data_reset_queue_delay)




    # keys_IPG_reg = [
    #     table_IPG_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 0)]),
    #     table_IPG_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 1)]),
    #     table_IPG_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 2)]),
    #     table_IPG_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 3)]),
    #     table_IPG_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 4)]),  #Porta 136
    #     table_IPG_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 5)])   #Porta 137
    # ]

    # data_reset_IPG_reg = [
    #     table_IPG_reg.make_data([gc.DataTuple('Egress.IPG_reg.f1', 0)]),
    #     table_IPG_reg.make_data([gc.DataTuple('Egress.IPG_reg.f1', 0)]),
    #     table_IPG_reg.make_data([gc.DataTuple('Egress.IPG_reg.f1', 0)]),
    #     table_IPG_reg.make_data([gc.DataTuple('Egress.IPG_reg.f1', 0)]),
    #     table_IPG_reg.make_data([gc.DataTuple('Egress.IPG_reg.f1', 0)]),
    #     table_IPG_reg.make_data([gc.DataTuple('Egress.IPG_reg.f1', 0)])
    # ]
    # table_IPG_reg.entry_mod(dev_tgt, key_list=keys_IPG_reg, data_list=data_reset_IPG_reg)

    # keys_packet_size_reg = [
    #     table_packet_size_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 0)]),
    #     table_packet_size_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 1)]),
    #     table_packet_size_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 2)]),
    #     table_packet_size_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 3)]),
    #     table_packet_size_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 4)]),  #Porta 136
    #     table_packet_size_reg.make_key([gc.KeyTuple('$REGISTER_INDEX', 5)])   #Porta 137
    # ]

    # data_reset_packet_size_reg = [
    #     table_packet_size_reg.make_data([gc.DataTuple('Egress.packet_size_reg.f1', 0)]),
    #     table_packet_size_reg.make_data([gc.DataTuple('Egress.packet_size_reg.f1', 0)]),
    #     table_packet_size_reg.make_data([gc.DataTuple('Egress.packet_size_reg.f1', 0)]),
    #     table_packet_size_reg.make_data([gc.DataTuple('Egress.packet_size_reg.f1', 0)]),
    #     table_packet_size_reg.make_data([gc.DataTuple('Egress.packet_size_reg.f1', 0)]),
    #     table_packet_size_reg.make_data([gc.DataTuple('Egress.packet_size_reg.f1', 0)])
    # ]

    # table_packet_size_reg.entry_mod(dev_tgt, key_list=keys_packet_size_reg, data_list=data_reset_packet_size_reg)

    # keys_totalPkts_IPG = [
    #     table_totalPkts_IPG.make_key([gc.KeyTuple('$REGISTER_INDEX', 0)]),
    #     table_totalPkts_IPG.make_key([gc.KeyTuple('$REGISTER_INDEX', 1)]),
    #     table_totalPkts_IPG.make_key([gc.KeyTuple('$REGISTER_INDEX', 2)]),
    #     table_totalPkts_IPG.make_key([gc.KeyTuple('$REGISTER_INDEX', 3)]),
    #     table_totalPkts_IPG.make_key([gc.KeyTuple('$REGISTER_INDEX', 4)]),  #Porta 136
    #     table_totalPkts_IPG.make_key([gc.KeyTuple('$REGISTER_INDEX', 5)])   #Porta 137
    # ]

    # data_reset_packet_size_reg = [
    #     table_totalPkts_IPG.make_data([gc.DataTuple('Egress.totalPkts_IPG.f1', 0)]),
    #     table_totalPkts_IPG.make_data([gc.DataTuple('Egress.totalPkts_IPG.f1', 0)]),
    #     table_totalPkts_IPG.make_data([gc.DataTuple('Egress.totalPkts_IPG.f1', 0)]),
    #     table_totalPkts_IPG.make_data([gc.DataTuple('Egress.totalPkts_IPG.f1', 0)]),
    #     table_totalPkts_IPG.make_data([gc.DataTuple('Egress.totalPkts_IPG.f1', 0)]),
    #     table_totalPkts_IPG.make_data([gc.DataTuple('Egress.totalPkts_IPG.f1', 0)])
    # ]

    # table_totalPkts_IPG.entry_mod(dev_tgt, key_list=keys_totalPkts_IPG, data_list=data_reset_packet_size_reg)

    # # Header da tabela
    # print("Category,Port,IPG,Number of Packets,Packet size,Estimated Rate,Real Rate")

    # # Dados do Classic
    # print(f"Classic,136,{IPG_reg_136_Classic_value},{totalPkts_IPG_136_Classic_value},{packet_size_reg_136_Classic_value},{estimated_rate_136_Classic},{rate_136_Classic}")
    # print(f"Classic,137,{IPG_reg_137_Classic_value},{totalPkts_IPG_137_Classic_value},{packet_size_reg_137_Classic_value},{estimated_rate_137_Classic},{rate_137_Classic}")

    # # Dados do L4S
    # print(f"L4S,136,{IPG_reg_136_L4S_value},{totalPkts_IPG_136_L4S_value}, {packet_size_reg_136_L4S_value},{estimated_rate_136_L4S},{rate_136_L4S}")
    # print(f"L4S,137,{IPG_reg_137_L4S_value},{totalPkts_IPG_137_L4S_value}, {packet_size_reg_137_L4S_value},{estimated_rate_137_L4S},{rate_137_L4S}")

    # # Dados do CG
    # print(f"CG,136,{IPG_reg_136_CG_value},{totalPkts_IPG_136_CG_value},{packet_size_reg_136_CG_value},{estimated_rate_136_CG},{rate_136_CG}")
    # print(f"CG,137,{IPG_reg_137_CG_value},{totalPkts_IPG_137_CG_value},{packet_size_reg_137_CG_value},{estimated_rate_137_CG},{rate_137_CG}")


    # print("########################")

    # data_sched_shaping_classic_136 = tm_table_sched_shaping.make_data([
    #     gc.DataTuple("max_rate", rate_136_Classic)
    #     #gc.DataTuple("unit", 'PPS')
    # ])
    # data_sched_shaping_classic_137 = tm_table_sched_shaping.make_data([
    #     gc.DataTuple("max_rate", rate_137_Classic)
    #     #gc.DataTuple("unit", 'PPS')
    # ])

    # data_sched_shaping_L4S_136 = tm_table_sched_shaping.make_data([
    #     gc.DataTuple("max_rate", rate_136_L4S)
    #     #gc.DataTuple("unit", 'PPS')
    # ])
    # data_sched_shaping_L4S_137 = tm_table_sched_shaping.make_data([
    #     gc.DataTuple("max_rate", rate_137_L4S)
    #     #gc.DataTuple("unit", 'PPS')
    # ])

    # data_sched_shaping_CG_136 = tm_table_sched_shaping.make_data([
    #     gc.DataTuple("max_rate", rate_136_CG)
    #     #gc.DataTuple("unit", 'PPS')
    # ])
    # data_sched_shaping_CG_137 = tm_table_sched_shaping.make_data([
    #     gc.DataTuple("max_rate", rate_137_CG)
    #     #gc.DataTuple("unit", 'PPS')
    # ])

    

    # tm_table_sched_shaping.entry_mod(dev_tgt, [key_sched_shaping_136_classic], [data_sched_shaping_classic_136])
    # tm_table_sched_shaping.entry_mod(dev_tgt, [key_sched_shaping_136_L4S], [data_sched_shaping_L4S_136])
    # tm_table_sched_shaping.entry_mod(dev_tgt, [key_sched_shaping_136_CG], [data_sched_shaping_CG_136])

    # tm_table_sched_shaping.entry_mod(dev_tgt, [key_sched_shaping_137_classic], [data_sched_shaping_classic_137])
    # tm_table_sched_shaping.entry_mod(dev_tgt, [key_sched_shaping_137_L4S], [data_sched_shaping_L4S_137])
    # tm_table_sched_shaping.entry_mod(dev_tgt, [key_sched_shaping_137_CG], [data_sched_shaping_CG_137])




    # time.sleep(wait_time)
    
