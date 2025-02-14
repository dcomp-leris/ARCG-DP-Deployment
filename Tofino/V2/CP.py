'''
# Version 2.0.0
# Author: Mateus
# Lab: LERIS
'''
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


#newtable classification
#tree1
#FS
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T1_FS.add_with_classify_T1_FS(metadata_frame_size_start=0, metadata_frame_size_end=42, classify_result=3)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T1_FS.add_with_classify_T1_FS(metadata_frame_size_start=43, metadata_frame_size_end=1667, classify_result=2)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T1_FS.add_with_classify_T1_FS(metadata_frame_size_start=1668, metadata_frame_size_end=65535, classify_result=0)

#IPG
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T1_IPG.add_with_classify_T1_IPG(metadata_ipg_20lsb_start=0, metadata_ipg_20lsb_end=1403, classify_result=1)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T1_IPG.add_with_classify_T1_IPG(metadata_ipg_20lsb_start=1404, metadata_ipg_20lsb_end=1048575, classify_result=2)

#t2
#IFG
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T2_IFG.add_with_classify_T2_IFG(metadata_ifg_20lsb_start=0, metadata_ifg_20lsb_end=31502, classify_result=3)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T2_IFG.add_with_classify_T2_IFG(metadata_ifg_20lsb_start=31503, metadata_ifg_20lsb_end=1048575, classify_result=0)

#IPG
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T2_IPG.add_with_classify_T2_IPG(metadata_ipg_20lsb_start=0, metadata_ipg_20lsb_end=1403, classify_result=1)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T2_IPG.add_with_classify_T2_IPG(metadata_ipg_20lsb_start=1404, metadata_ipg_20lsb_end=1048575, classify_result=2)

#T3
#FS
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T3_FS.add_with_classify_T3_FS(metadata_frame_size_start=0, metadata_frame_size_end=42, classify_result=3)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T3_FS.add_with_classify_T3_FS(metadata_frame_size_start=43, metadata_frame_size_end=65535, classify_result=0)

#IFG
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T3_IFG.add_with_classify_T3_IFG(metadata_ifg_20lsb_start=0, metadata_ifg_20lsb_end=57938, classify_result=2)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T3_IFG.add_with_classify_T3_IFG(metadata_ifg_20lsb_start=57939, metadata_ifg_20lsb_end=1048575, classify_result=0)

#IPG
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T3_IPG.add_with_classify_T3_IPG(metadata_ipg_20lsb_start=0, metadata_ipg_20lsb_end=1403, classify_result=1)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T3_IPG.add_with_classify_T3_IPG(metadata_ipg_20lsb_start=1404, metadata_ipg_20lsb_end=1048575, classify_result=2)


#T4
#IFG
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T4_IFG.add_with_classify_T4_IFG(metadata_ifg_20lsb_start=0, metadata_ifg_20lsb_end=57831, classify_result=6)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T4_IFG.add_with_classify_T4_IFG(metadata_ifg_20lsb_start=57832, metadata_ifg_20lsb_end=1048575, classify_result=5)

#FS
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T4_FS.add_with_classify_T4_FS(metadata_frame_size_start=0, metadata_frame_size_end=44, classify_result=3)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T4_FS.add_with_classify_T4_FS(metadata_frame_size_start=45, metadata_frame_size_end=65535, classify_result=2)

#IPG
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T4_IPG.add_with_classify_T4_IPG(metadata_ipg_20lsb_start=0, metadata_ipg_20lsb_end=1403, classify_result=1)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T4_IPG.add_with_classify_T4_IPG(metadata_ipg_20lsb_start=1403, metadata_ipg_20lsb_end=218208, classify_result=2)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T4_IPG.add_with_classify_T4_IPG(metadata_ipg_20lsb_start=218208, metadata_ipg_20lsb_end=1048575, classify_result=3)

#T5
#FS
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T5_FS.add_with_classify_T5_FS(metadata_frame_size_start=0, metadata_frame_size_end=42, classify_result=3)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T5_FS.add_with_classify_T5_FS(metadata_frame_size_start=43, metadata_frame_size_end=65535, classify_result=0)
#IPG
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T5_IPG.add_with_classify_T5_IPG(metadata_ipg_20lsb_start=0, metadata_ipg_20lsb_end=1382, classify_result=1)
bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_T5_IPG.add_with_classify_T5_IPG(metadata_ipg_20lsb_start=1383, metadata_ipg_20lsb_end=1048575, classify_result=2)

#FINAL CLASS
with open("/home/leris/p4code/alireza/RF_deployment/CLONE_EGRESS/change_mirror/TABLES/5trees/majority.txt", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue  # Skip empty lines

        # Expected format: t1=1,t2=2,t3=2,t4=2,t5=2,m=2
        parts = line.split(',')
        votes = {}
        for part in parts:
            key, value = part.split('=')
            votes[key.strip()] = int(value.strip())

        # Use the BFRT API to add the entry
        bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_majority.add_with_final_classification(
            metadata_classT1 = votes['t1'],
            metadata_classT2 = votes['t2'],
            metadata_classT3 = votes['t3'],
            metadata_classT4 = votes['t4'],
            metadata_classT5 = votes['t5'],
            majority        = votes['m']
        )

#bfrt.RF_deployment_5trees.pipe.SwitchIngress.table_majority.add_with_final_classification(metadata_classT1 = t1, metadata_classT2 = t2, metadata_classT3 = t3, metadata_classT1=t4, metadata_classT1=t5, majority = majority)


