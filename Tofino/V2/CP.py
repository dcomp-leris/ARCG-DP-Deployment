#Add and enable ports (16/0=264, 16/1=265)
bfrt.port.port.add(DEV_PORT=136, SPEED="BF_SPEED_10G", FEC="BF_FEC_TYP_NONE", PORT_ENABLE =True,AUTO_NEGOTIATION="PM_AN_FORCE_DISABLE")
bfrt.port.port.add(DEV_PORT=137, SPEED="BF_SPEED_10G", FEC="BF_FEC_TYP_NONE", PORT_ENABLE =True,AUTO_NEGOTIATION="PM_AN_FORCE_DISABLE")
bfrt.port.port.add(DEV_PORT=448, SPEED="BF_SPEED_100G", FEC="BF_FEC_TYP_NONE", PORT_ENABLE =True)
bfrt.port.port.add(DEV_PORT=440, SPEED="BF_SPEED_100G", FEC="BF_FEC_TYP_NONE", PORT_ENABLE =True)
#bfrt.port.port.add(DEV_PORT=128, SPEED="BF_SPEED_100G", FEC="BF_FEC_TYP_NONE", PORT_ENABLE=True, AUTO_NEGOTIATION="PM_AN_FORCE_DISABLE")


#2/0
bfrt.port.port.add(DEV_PORT=144, SPEED="BF_SPEED_10G", FEC="BF_FEC_TYP_NONE")
bfrt.port.port.mod(DEV_PORT=144, LOOPBACK_MODE='BF_LPBK_MAC_NEAR')




#Enable mirror session 1 in TM
# bfrt.mirror.cfg.entry_with_normal(sid=1, direction='INGRESS', session_enable=True, ucast_egress_port=128, ucast_egress_port_valid=True, max_pkt_len=48).push()
bfrt.mirror.cfg.entry_with_normal(sid=1, direction='EGRESS', session_enable=True, ucast_egress_port=128, ucast_egress_port_valid=True, max_pkt_len=48).push()

bfrt.tf2.tm.port.sched_cfg.mod(dev_port=136, max_rate_enable=True)
bfrt.tf2.tm.port.sched_cfg.mod(dev_port=137, max_rate_enable=True)
#max_burst_size = BYTES
#max_rate = KILOBITS/SEC

#VERSAO BPS
# bfrt.tf2.tm.port.sched_shaping.mod(dev_port=136, unit='BPS', max_rate=100000, max_burst_size=4500) #kilobits/sec and
# bfrt.tf2.tm.port.sched_shaping.mod(dev_port=137, unit='BPS', max_rate=100000, max_burst_size=4500)

#VERSAO PPS
# bfrt.tf2.tm.port.sched_shaping.mod(dev_port=136, unit='PPS', max_rate=15000, max_burst_size=100) #kilobits/sec and
# bfrt.tf2.tm.port.sched_shaping.mod(dev_port=137, unit='PPS', max_rate=15000, max_burst_size=100)


#VERSOA ALTERAR WEIGHT DAS FILAS (classic = 1, l4s = 4, cg = 0)
# bfrt.tf2.tm.queue.sched_cfg.mod(pipe=1, pg_id=1, pg_queue=0,dwrr_weight=1)
# bfrt.tf2.tm.queue.sched_cfg.mod(pipe=1, pg_id=1, pg_queue=1,dwrr_weight=3)
# bfrt.tf2.tm.queue.sched_cfg.mod(pipe=1, pg_id=1, pg_queue=2,dwrr_weight=1)
# bfrt.tf2.tm.queue.sched_cfg.mod(pipe=1, pg_id=1, pg_queue=16,dwrr_weight=1)
# bfrt.tf2.tm.queue.sched_cfg.mod(pipe=1, pg_id=1, pg_queue=17,dwrr_weight=3)
# bfrt.tf2.tm.queue.sched_cfg.mod(pipe=1, pg_id=1, pg_queue=18,dwrr_weight=1)

#VERSAO ALTERAR RATE DAS FILAS
##bfrt.tf2.tm.queue.sched_cfg.mod(pipe=1, pg_id=1, pg_queue=0,max_rate_enable=True)
##bfrt.tf2.tm.queue.sched_cfg.mod(pipe=1, pg_id=1, pg_queue=1,max_rate_enable=True)
##bfrt.tf2.tm.queue.sched_cfg.mod(pipe=1, pg_id=1, pg_queue=2,max_rate_enable=True)
##bfrt.tf2.tm.queue.sched_cfg.mod(pipe=1, pg_id=1, pg_queue=16,max_rate_enable=True)
##bfrt.tf2.tm.queue.sched_cfg.mod(pipe=1, pg_id=1, pg_queue=17,max_rate_enable=True)
##bfrt.tf2.tm.queue.sched_cfg.mod(pipe=1, pg_id=1, pg_queue=18,max_rate_enable=True)

# bfrt.tf2.tm.queue.sched_shaping.mod(pipe=1,pg_id=1, pg_queue=0,unit='PPS', min_rate = 2000) #pps
# bfrt.tf2.tm.queue.sched_shaping.mod(pipe=1,pg_id=1, pg_queue=1,unit='PPS', min_rate = 2000)
# bfrt.tf2.tm.queue.sched_shaping.mod(pipe=1,pg_id=1, pg_queue=2,unit='PPS', min_rate = 2000)
# bfrt.tf2.tm.queue.sched_shaping.mod(pipe=1,pg_id=1, pg_queue=16,unit='PPS', min_rate = 2000)
# bfrt.tf2.tm.queue.sched_shaping.mod(pipe=1,pg_id=1, pg_queue=17,unit='PPS', min_rate = 2000)
# bfrt.tf2.tm.queue.sched_shaping.mod(pipe=1,pg_id=1, pg_queue=18,unit='PPS', min_rate = 2000)



# bfrt.tf2.tm.queue.sched_shaping.mod(pipe=1,pg_id=1, pg_queue=0,unit='BPS') #pps
# bfrt.tf2.tm.queue.sched_shaping.mod(pipe=1,pg_id=1, pg_queue=1,unit='BPS')
# bfrt.tf2.tm.queue.sched_shaping.mod(pipe=1,pg_id=1, pg_queue=2,unit='BPS')
# bfrt.tf2.tm.queue.sched_shaping.mod(pipe=1,pg_id=1, pg_queue=16,unit='BPS')
# bfrt.tf2.tm.queue.sched_shaping.mod(pipe=1,pg_id=1, pg_queue=17,unit='BPS')
# bfrt.tf2.tm.queue.sched_shaping.mod(pipe=1,pg_id=1, pg_queue=18,unit='BPS')


##bfrt.tf2.tm.queue.sched_shaping.mod(pipe=1,pg_id=1, pg_queue=0,unit='BPS', max_rate = 0) #pps
##bfrt.tf2.tm.queue.sched_shaping.mod(pipe=1,pg_id=1, pg_queue=1,unit='BPS', max_rate = 90000)
##bfrt.tf2.tm.queue.sched_shaping.mod(pipe=1,pg_id=1, pg_queue=2,unit='BPS', max_rate = 10000)
##bfrt.tf2.tm.queue.sched_shaping.mod(pipe=1,pg_id=1, pg_queue=16,unit='BPS',max_rate = 0)
##bfrt.tf2.tm.queue.sched_shaping.mod(pipe=1,pg_id=1, pg_queue=17,unit='BPS', max_rate = 90000)
##bfrt.tf2.tm.queue.sched_shaping.mod(pipe=1,pg_id=1, pg_queue=18,unit='BPS', max_rate = 10000)



#table entries for the index of the registers (egress) - NOT WORKING (dont know loopback port number)
# bfrt.L4S_Classic_CG.pipe.Egress.define_index_for_registers_table.add_with_define_index_for_registers_action(
#     bridge_qid=0,
#     egress_port=136,
#     index=0
# )



# #LPF PACKET SIZE CONFIG
bfrt.RF_deployment_5trees.pipe.SwitchIngress.lpf_packet_size.add(0,'SAMPLE', 100000000, 100000000,0)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.lpf_frame_size.add(0,'SAMPLE', 100000000, 100000000,0)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.lpf_ipg.add(0,'SAMPLE', 100000000, 100000000,0)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.lpf_ifg.add(0,'SAMPLE', 100000000, 100000000,0)


#TABLE CLASSIFICATION
#tree1
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree1.add_with_classify_result1(metadata_frame_size_start=1668, metadata_frame_size_end=65535, metadata_ipg_20lsb_start=0, metadata_ipg_20lsb_end = 1403, classify_result=1)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree1.add_with_classify_result2(metadata_frame_size_start=43, metadata_frame_size_end=1267, metadata_ipg_20lsb_start = 0, metadata_ipg_20lsb_end = 1048575, classify_result=2)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree1.add_with_classify_result2(metadata_frame_size_start=1268, metadata_frame_size_end=1667, metadata_ipg_20lsb_start=0, metadata_ipg_20lsb_end = 1048575, classify_result=2)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree1.add_with_classify_result2(metadata_frame_size_start=166, metadata_frame_size_end=65535, metadata_ipg_20lsb_start=1404, metadata_ipg_20lsb_end = 1048575, classify_result=2)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree1.add_with_classify_result3(metadata_frame_size_start=0, metadata_frame_size_end=42, metadata_ipg_20lsb_start=0, metadata_ipg_20lsb_end = 1048575, classify_result=3)

#tree2
#ar
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree2.add_with_classify_result1(metadata_ifg_20lsb_start = 31503,metadata_ifg_20lsb_end = 1048575, metadata_ipg_20lsb_start= 0, metadata_ipg_20lsb_end = 973, metadata_packet_size_start = 0, metadata_packet_size_end = 65535, classify_result=1)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree2.add_with_classify_result1(metadata_ifg_20lsb_start = 31503,metadata_ifg_20lsb_end = 1048575, metadata_ipg_20lsb_start= 974, metadata_ipg_20lsb_end = 1403, metadata_packet_size_start = 0, metadata_packet_size_end = 65535, classify_result=1)
#cg
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree2.add_with_classify_result2(metadata_ifg_20lsb_start = 31503,metadata_ifg_20lsb_end = 139620, metadata_ipg_20lsb_start= 1404, metadata_ipg_20lsb_end = 1048575, metadata_packet_size_start = 0, metadata_packet_size_end = 65535, classify_result=2)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree2.add_with_classify_result2(metadata_ifg_20lsb_start = 139621,metadata_ifg_20lsb_end = 1048575, metadata_ipg_20lsb_start= 1404, metadata_ipg_20lsb_end = 1048575, metadata_packet_size_start = 0, metadata_packet_size_end = 65535, classify_result=2)
#other
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree2.add_with_classify_result3(metadata_ifg_20lsb_start = 0,metadata_ifg_20lsb_end = 31502, metadata_ipg_20lsb_start= 0, metadata_ipg_20lsb_end = 1048575, metadata_packet_size_start = 0, metadata_packet_size_end = 55, classify_result=3)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree2.add_with_classify_result3(metadata_ifg_20lsb_start = 0,metadata_ifg_20lsb_end = 13604, metadata_ipg_20lsb_start= 0, metadata_ipg_20lsb_end = 1048575, metadata_packet_size_start = 56, metadata_packet_size_end = 65535, classify_result=3)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree2.add_with_classify_result3(metadata_ifg_20lsb_start = 13605,metadata_ifg_20lsb_end = 31502, metadata_ipg_20lsb_start= 0, metadata_ipg_20lsb_end = 1048575, metadata_packet_size_start = 56, metadata_packet_size_end = 65535, classify_result=3)

#tree3
#ar
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree3.add_with_classify_result1(metadata_ifg_20lsb_start = 57939,metadata_ifg_20lsb_end = 1048575, metadata_ipg_20lsb_start= 0, metadata_ipg_20lsb_end = 969, metadata_frame_size_start = 0, metadata_frame_size_end = 65535, classify_result=1)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree3.add_with_classify_result1(metadata_ifg_20lsb_start = 57938,metadata_ifg_20lsb_end = 1048575, metadata_ipg_20lsb_start= 969, metadata_ipg_20lsb_end = 1403, metadata_frame_size_start = 0, metadata_frame_size_end = 65535, classify_result=1)
#cg
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree3.add_with_classify_result2(metadata_ifg_20lsb_start = 0,metadata_ifg_20lsb_end = 20925, metadata_ipg_20lsb_start= 0, metadata_ipg_20lsb_end = 1048575, metadata_frame_size_start = 45, metadata_frame_size_end = 65535, classify_result=2)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree3.add_with_classify_result2(metadata_ifg_20lsb_start = 20926,metadata_ifg_20lsb_end = 57938, metadata_ipg_20lsb_start= 0, metadata_ipg_20lsb_end = 1048575, metadata_frame_size_start = 45, metadata_frame_size_end = 65535, classify_result=2)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree3.add_with_classify_result2(metadata_ifg_20lsb_start = 57938,metadata_ifg_20lsb_end = 1048575, metadata_ipg_20lsb_start= 1403, metadata_ipg_20lsb_end = 1048575, metadata_frame_size_start = 42, metadata_frame_size_end = 65535, classify_result=2)
#other
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree3.add_with_classify_result3(metadata_ifg_20lsb_start = 0,metadata_ifg_20lsb_end = 57938, metadata_ipg_20lsb_start= 0, metadata_ipg_20lsb_end = 1048575, metadata_frame_size_start = 0, metadata_frame_size_end = 44, classify_result=3)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree3.add_with_classify_result3(metadata_ifg_20lsb_start = 57938,metadata_ifg_20lsb_end = 1048575, metadata_ipg_20lsb_start= 1403, metadata_ipg_20lsb_end = 1048575, metadata_frame_size_start = 0, metadata_frame_size_end = 42, classify_result=3)

#tree4
#ar
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree4.add_with_classify_result1(metadata_ifg_20lsb_start = 57832,metadata_ifg_20lsb_end = 1048575, metadata_ipg_20lsb_start= 0, metadata_ipg_20lsb_end = 1062, metadata_frame_size_start = 0, metadata_frame_size_end = 65535, metadata_packet_size_start = 0, metadata_packet_size_end = 65535,classify_result=1)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree4.add_with_classify_result1(metadata_ifg_20lsb_start = 57832,metadata_ifg_20lsb_end = 1048575, metadata_ipg_20lsb_start= 1063, metadata_ipg_20lsb_end = 1403, metadata_frame_size_start = 0, metadata_frame_size_end = 65535, metadata_packet_size_start = 0, metadata_packet_size_end = 65535,classify_result=1)
#cg
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree4.add_with_classify_result2(metadata_ifg_20lsb_start = 0,metadata_ifg_20lsb_end = 57831, metadata_ipg_20lsb_start= 0, metadata_ipg_20lsb_end = 1048575, metadata_frame_size_start = 45, metadata_frame_size_end = 65535, metadata_packet_size_start = 0, metadata_packet_size_end = 39,classify_result=2)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree4.add_with_classify_result2(metadata_ifg_20lsb_start = 0,metadata_ifg_20lsb_end = 57831, metadata_ipg_20lsb_start= 0, metadata_ipg_20lsb_end = 1048575, metadata_frame_size_start = 45, metadata_frame_size_end = 65535, metadata_packet_size_start = 40, metadata_packet_size_end = 65535,classify_result=2)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree4.add_with_classify_result2(metadata_ifg_20lsb_start = 57832,metadata_ifg_20lsb_end = 1048575, metadata_ipg_20lsb_start= 1404, metadata_ipg_20lsb_end = 218209, metadata_frame_size_start = 0, metadata_frame_size_end = 65535, metadata_packet_size_start = 0, metadata_packet_size_end = 65535,classify_result=2)
#other
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree4.add_with_classify_result3(metadata_ifg_20lsb_start = 0,metadata_ifg_20lsb_end = 57831, metadata_ipg_20lsb_start= 0, metadata_ipg_20lsb_end = 1048575, metadata_frame_size_start = 0, metadata_frame_size_end = 44, metadata_packet_size_start = 0, metadata_packet_size_end = 65535,classify_result=3)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree4.add_with_classify_result3(metadata_ifg_20lsb_start = 57832,metadata_ifg_20lsb_end = 1048575, metadata_ipg_20lsb_start= 218209, metadata_ipg_20lsb_end = 1048575, metadata_frame_size_start = 0, metadata_frame_size_end = 65535, metadata_packet_size_start = 0, metadata_packet_size_end = 65535,classify_result=3)


#tree5
#ar
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree5.add_with_classify_result1(metadata_ipg_20lsb_start= 0, metadata_ipg_20lsb_end = 1382, metadata_frame_size_start = 42, metadata_frame_size_end = 1942,classify_result=1)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree5.add_with_classify_result1(metadata_ipg_20lsb_start= 0, metadata_ipg_20lsb_end = 1382, metadata_frame_size_start = 1943, metadata_frame_size_end = 65535,classify_result=1)
#cg
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree5.add_with_classify_result2(metadata_ipg_20lsb_start= 1382, metadata_ipg_20lsb_end = 1489, metadata_frame_size_start = 43, metadata_frame_size_end = 65535,classify_result=2)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree5.add_with_classify_result2(metadata_ipg_20lsb_start= 1489, metadata_ipg_20lsb_end = 1048575, metadata_frame_size_start = 43, metadata_frame_size_end = 65535,classify_result=2)
#other
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_tree5.add_with_classify_result3(metadata_ipg_20lsb_start= 0, metadata_ipg_20lsb_end = 1048575, metadata_frame_size_start = 0, metadata_frame_size_end = 42,classify_result=3)



#majority
#if one of them is 3,4 or 5
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_check_majority.add_with_set_majority(contador1_start=3, contador1_end=5, majority=1) 
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_check_majority.add_with_set_majority(contador2_start=3, contador2_end=5, majority=2) 
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_check_majority.add_with_set_majority(contador3_start=3, contador3_end=5, majority=3) 
#if there is two 2's
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_check_majority.add_with_set_majority(contador1_start=2, contador1_end=2, contador2_start=2, contador2_end=2, majority=1) 
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_check_majority.add_with_set_majority(contador1_start=2, contador1_end=2, contador3_start=2, contador3_end=2, majority=1) 
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_check_majority.add_with_set_majority(contador2_start=2, contador2_end=2, contador3_start=2, contador3_end=2, majority=2) 
