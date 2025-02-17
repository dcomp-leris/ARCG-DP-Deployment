/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

#include "constants.p4"

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/


header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<6>    diffserv;
    bit<2>    ecn;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

header ipv6_t {
    bit<4>    version;
    bit<8>    trafficClass;
    bit<20>   flowLabel;
    bit<16>   payloadLen;
    bit<8>    nextHdr;
    bit<8>    hopLimit;
    bit<128>  srcAddr;
    bit<128>  dstAddr;
}

header udp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<16> length_;
    bit<16> checksum;
}

header rtp_t {
    bit<2> version;
    bit<1> padding;
    bit<1> extension;
    bit<4> csrcCounter;
    bit<1> marker;
    bit<7> payloadType;
    bit<16> seqNumber;
    bit<32> timestamp;
    bit<32> ssrcID;
    bit<16> csrcID;

}

header icmp_t {
    bit<224> head;
    bit<16> pattern;

}

header nodeCount_h{
    bit<16>  id;
    bit<16>  count;
}

header InBandNetworkTelemetry_h {
    switchID_v swid;
    ingress_port_v ingress_port;
    egress_port_v egress_port;
    egressSpec_v egress_spec;
    priority_v priority;
    qid_v qid;
    ingress_global_timestamp_v ingress_global_timestamp;
    egress_global_timestamp_v egress_global_timestamp;
    enq_timestamp_v enq_timestamp;
    enq_qdepth_v enq_qdepth;
    deq_timedelta_v deq_timedelta;
    deq_qdepth_v deq_qdepth;
    deq_timedelta_v processing_time;
}

struct ingress_metadata_t {
    bit<16>  count;
}

struct parser_metadata_t {
    bit<16>  remaining;
}

struct metadata {
    ingress_metadata_t   ingress_metadata;
    parser_metadata_t   parser_metadata;
    flowID_t flowID;
    bit<1> isRTP;
    int_t ps;
    timestamp_t ipi;
    int_t fs;
    timestamp_t ifi;
    bit<14> action_select1;
    bit<14> action_select2;
    bit<14> action_select3;
    bit<14> action_select4;
    bit<3> result_t1;
    bit<3> result_t2;
    bit<3> result_t3;
    bit<3> result_t4;
    bit<3> result_t5;
    bit<3> count_other;
    bit<3> count_CG;
    bit<3> count_AR;
    bit<1> classify;

}

struct headers {
    ethernet_t   ethernet;
    ipv4_t       ipv4;
    ipv6_t       ipv6;
    udp_t        udp;
    rtp_t        rtp;
    icmp_t       icmp;
    nodeCount_h        nodeCount;
    InBandNetworkTelemetry_h[MAX_HOPS] INT;
}

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
          TYPE_IPV4: parse_ipv4;
          TYPE_IPV6: parse_ipv6;
          default: accept;
        }
    }

    state parse_ipv4 {
      packet.extract(hdr.ipv4);
      transition select(hdr.ipv4.protocol) {
        PROTO_UDP: parse_udp;
        PROTO_INT: parse_count;
        PROTO_ICMP: parse_icmp;
        default: accept;
      }
    }

    state parse_ipv6 {
      packet.extract(hdr.ipv6);
      transition select(hdr.ipv6.nextHdr) {
        PROTO_UDP: parse_udp;
        default: accept;
      }
    }

    state parse_udp {
        packet.extract(hdr.udp);
        transition parse_rtp;
    }

    state parse_rtp {
        packet.extract(hdr.rtp);
        transition accept;
    }

    state parse_icmp {
        packet.extract(hdr.icmp);
        transition accept;
    }

    state parse_count{
        packet.extract(hdr.nodeCount);
        meta.parser_metadata.remaining = hdr.nodeCount.count;
        transition select(meta.parser_metadata.remaining) {
            0 : accept;
            default: parse_int;
        }
    }

    state parse_int {
        packet.extract(hdr.INT.next);
        meta.parser_metadata.remaining = meta.parser_metadata.remaining - 1;
        transition select(meta.parser_metadata.remaining) {
            0 : accept;
            default: parse_int;
        }
    }

}


/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {  }
}


/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
    
    register<bit<3>>(0xffff) flow_queue;
    register<bit<16>>(1) fid_reg;
    register<bit<4>>(0xffff) frames_pkts_counter;
    
    register<bit<32>>(0xffff) ps_register;
    register<bit<48>>(0xffff) ipi_register;
    register<bit<32>>(0xffff) fs_register;
    register<bit<48>>(0xffff) ifi_register;

    register<bit<48>>(0xffff) lpt_register;
    register<bit<48>>(0xffff) lfst_register;
    register<bit<16>>(0xffff) seqNumber_register;

    // these register are only for debug and logging
    counter(3, CounterType.packets) icmp_pkts;
    counter(1, CounterType.packets) debug;
    //register<bit<16>>(1) icmp_pattern_reg;
    register<bit<3>>(6) trees_result_reg; 

    action drop() {
        mark_to_drop(standard_metadata);
    }

    // to forward INT packets back to host
    action send_back() {
        standard_metadata.egress_spec = standard_metadata.ingress_port;
        bit<48> tmp_mac;
        bit<32> tmp_ip;

        tmp_mac = hdr.ethernet.srcAddr;
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = tmp_mac;

        tmp_ip = hdr.ipv4.srcAddr;
        hdr.ipv4.srcAddr = hdr.ipv4.dstAddr;
        hdr.ipv4.dstAddr = tmp_ip;
    }

    action find_flowID_ipv4() {
        bit<1> base = 0;
        bit<16> max = 0xffff;
        bit<16> hash_result;
        bit<48> IP_Port = hdr.ipv4.dstAddr ++ hdr.udp.dstPort;

        hash(
             hash_result,
             HashAlgorithm.crc16,
             base,
             {
                IP_Port
             },
             max
             );


        meta.flowID = hash_result;

    }

    action find_flowID_ipv6() {
        bit<1> base = 0;
        bit<16> max = 0xffff;
        bit<16> hash_result;
        bit<144> IP_Port = hdr.ipv6.dstAddr ++ hdr.udp.dstPort;

        hash(
             hash_result,
             HashAlgorithm.crc16,
             base,
             {
                IP_Port
             },
             max
             );


        meta.flowID = hash_result;

    }

    // FEATURES CLASSIFICATION ACTIONS
    action set_actionselect1(bit<14> featurevalue1){
        meta.action_select1 = featurevalue1 ;
    }

    action set_actionselect2(bit<14> featurevalue2){
        meta.action_select2 = featurevalue2 ;
    }
 
    action set_actionselect3(bit<14> featurevalue3){
        meta.action_select3 = featurevalue3;
    }

    action set_actionselect4(bit<14> featurevalue4){
        meta.action_select4 = featurevalue4;
    }

    // FEATURES CLASSIFICATION TABLES
    table t1_feature1_exact{
        key = {
            meta.fs : range ;
        }
        actions = {
	        NoAction;
            set_actionselect1;
        }
        size = 1024;
    } 

    table t1_feature2_exact{
        key = {
            meta.ps : range ;
        }
        actions = {
	        NoAction;
            set_actionselect2;
        }
    }

    table t1_feature3_exact{
        key = {
            meta.ipi : range ;
        }
        actions = {
	        NoAction;
            set_actionselect3;
        }
        size = 1024;
    }

    table t1_feature4_exact{
        key = {
            meta.ifi : range ;
        }
        actions = {
	        NoAction;
            set_actionselect4;
        }
        size = 1024;
    }

    table t2_feature1_exact{
        key = {
            meta.fs : range ;
        }
        actions = {
	        NoAction;
            set_actionselect1;
        }
        size = 1024;
    } 

    table t2_feature2_exact{
        key = {
            meta.ps : range ;
        }
        actions = {
	        NoAction;
            set_actionselect2;
        }
    }

    table t2_feature3_exact{
        key = {
            meta.ipi : range ;
        }
        actions = {
	        NoAction;
            set_actionselect3;
        }
        size = 1024;
    }

    table t2_feature4_exact{
        key = {
            meta.ifi : range ;
        }
        actions = {
	        NoAction;
            set_actionselect4;
        }
        size = 1024;
    }

    table t3_feature1_exact{
        key = {
            meta.fs : range ;
        }
        actions = {
	        NoAction;
            set_actionselect1;
        }
        size = 1024;
    } 

    table t3_feature2_exact{
        key = {
            meta.ps : range ;
        }
        actions = {
	        NoAction;
            set_actionselect2;
        }
    }

    table t3_feature3_exact{
        key = {
            meta.ipi : range ;
        }
        actions = {
	        NoAction;
            set_actionselect3;
        }
        size = 1024;
    }

    table t3_feature4_exact{
        key = {
            meta.ifi : range ;
        }
        actions = {
	        NoAction;
            set_actionselect4;
        }
        size = 1024;
    }

    table t4_feature1_exact{
        key = {
            meta.fs : range ;
        }
        actions = {
	        NoAction;
            set_actionselect1;
        }
        size = 1024;
    } 

    table t4_feature2_exact{
        key = {
            meta.ps : range ;
        }
        actions = {
	        NoAction;
            set_actionselect2;
        }
    }

    table t4_feature3_exact{
        key = {
            meta.ipi : range ;
        }
        actions = {
	        NoAction;
            set_actionselect3;
        }
        size = 1024;
    }

    table t4_feature4_exact{
        key = {
            meta.ifi : range ;
        }
        actions = {
	        NoAction;
            set_actionselect4;
        }
        size = 1024;
    }

    table t5_feature1_exact{
        key = {
            meta.fs : range ;
        }
        actions = {
	        NoAction;
            set_actionselect1;
        }
        size = 1024;
    } 

    table t5_feature2_exact{
        key = {
            meta.ps : range ;
        }
        actions = {
	        NoAction;
            set_actionselect2;
        }
    }

    table t5_feature3_exact{
        key = {
            meta.ipi : range ;
        }
        actions = {
	        NoAction;
            set_actionselect3;
        }
        size = 1024;
    }

    table t5_feature4_exact{
        key = {
            meta.ifi : range ;
        }
        actions = {
	        NoAction;
            set_actionselect4;
        }
        size = 1024;
    }

    action assign_q(bit<3> qid) {
        standard_metadata.priority = qid;
    }

    // set flow class, can be added diferent action and queue for AR
    action set_other() {
        //assign_q(1);
        flow_queue.write((bit<32>)meta.flowID, 1);
    }

    action set_cg_ar() {
        //assign_q(2);
        flow_queue.write((bit<32>)meta.flowID, 2);
    }

    // actions to save trees votes and count they
    action t1_set_result(bit<3> result) {
        meta.result_t1 = result;

        if (result == 1) meta.count_other = meta.count_other + 1;
        else if (result == 2) meta.count_CG = meta.count_CG + 1;
        else if (result == 3) meta.count_AR = meta.count_AR + 1;
    }

    action t2_set_result(bit<3> result) {
        meta.result_t2 = result;

        if (result == 1) meta.count_other = meta.count_other + 1;
        else if (result == 2) meta.count_CG = meta.count_CG + 1;
        else if (result == 3) meta.count_AR = meta.count_AR + 1;
    }

    action t3_set_result(bit<3> result) {
        meta.result_t3 = result;

        if (result == 1) meta.count_other = meta.count_other + 1;
        else if (result == 2) meta.count_CG = meta.count_CG + 1;
        else if (result == 3) meta.count_AR = meta.count_AR + 1;
    }

    action t4_set_result(bit<3> result) {
        meta.result_t4 = result;

        if (result == 1) meta.count_other = meta.count_other + 1;
        else if (result == 2) meta.count_CG = meta.count_CG + 1;
        else if (result == 3) meta.count_AR = meta.count_AR + 1;
    }

    action t5_set_result(bit<3> result) {
        meta.result_t5 = result;

        if (result == 1) meta.count_other = meta.count_other + 1;
        else if (result == 2) meta.count_CG = meta.count_CG + 1;
        else if (result == 3) meta.count_AR = meta.count_AR + 1;
    }

    // main trees tables
    table t1_classify_exact {
        key = {
            meta.action_select1: range;
            meta.action_select2: range;
            meta.action_select3: range;
            meta.action_select4: range;
        }
        actions = {
            t1_set_result;
            NoAction;
            drop;
        }
    }

    table t2_classify_exact {
        key = {
            meta.action_select1: range;
            meta.action_select2: range;
            meta.action_select3: range;
            meta.action_select4: range;
        }
        actions = {
            t2_set_result;
            NoAction;
            drop;
        }
    }

    table t3_classify_exact {
        key = {
            meta.action_select1: range;
            meta.action_select2: range;
            meta.action_select3: range;
            meta.action_select4: range;
        }
        actions = {
            t3_set_result;
            NoAction;
            drop;
        }
    }

    table t4_classify_exact {
        key = {
            meta.action_select1: range;
            meta.action_select2: range;
            meta.action_select3: range;
            meta.action_select4: range;
        }
        actions = {
            t4_set_result;
            NoAction;
            drop;
        }
    }

    table t5_classify_exact {
        key = {
            meta.action_select1: range;
            meta.action_select2: range;
            meta.action_select3: range;
            meta.action_select4: range;
        }
        actions = {
            t5_set_result;
            NoAction;
            drop;
        }
    }

    action extract_features() {
        
        meta.classify = 0;

        bit<4> num_frames_pkts;
        bit<16> value_to_write;
        frames_pkts_counter.read(num_frames_pkts, (bit<32>)meta.flowID);
        fid_reg.read(value_to_write, 0);

        // for average
        int_t ps = 0;
        int<32> diff_ps = 0;
        timestamp_t ipi = 0;
        int<48> diff_ts = 0;
        int_t fs = 0;
        timestamp_t ifi = 0;

        // for last collected
        int_t packet_size = 0;
        timestamp_t inter_packet_interval = 0;
        int_t frame_size = 0;
        timestamp_t inter_frame_interval = 0;

        // aux info
        timestamp_t current_time = standard_metadata.ingress_global_timestamp;
        timestamp_t last_packet_time = 0;
        timestamp_t last_frame_start_time = 0;
        bit<16> previous_seqNumber = 0;
        bit<16> current_seqNumber = 0;

        ps_register.read(ps, (bit<32>)meta.flowID);
        ipi_register.read(ipi, (bit<32>)meta.flowID);
        fs_register.read(fs, (bit<32>)meta.flowID);
        ifi_register.read(ifi, (bit<32>)meta.flowID);

        lpt_register.read(last_packet_time,(bit<32>) meta.flowID);
        lfst_register.read(last_frame_start_time, (bit<32>)meta.flowID);
        seqNumber_register.read(previous_seqNumber, (bit<32>)meta.flowID);

        if (last_packet_time == 0) { // 0 = first packet of that flow
            last_packet_time = current_time;

        } else {

            /* PS */
            packet_size = standard_metadata.packet_length;
            // check if it is not the first packet
            if (ps > 0 ) {
                diff_ps = ((int<32>) packet_size) - ((int<32>) ps);
                diff_ps = diff_ps >> 7;
                ps = ps + (bit<32>) diff_ps;
                //ps =  ps >> 1;
            } else {
                ps = packet_size;
            }

            /* IPI */
            inter_packet_interval = current_time - last_packet_time;
            last_packet_time = current_time;
            // check if it is not the first packet
            if (ipi > 0) {
                diff_ts = ((int<48>) inter_packet_interval ) - ((int<48>) ipi);
                diff_ts = diff_ts >> 7;
                ipi = ipi + (bit<48>) diff_ts;
                //ipi = inter_packet_interval;
            } else {
                ipi = inter_packet_interval;
            }
            /* check rtp frames */
            // try to check if the packet have rtp
            if (hdr.rtp.version == RTP_VERSION && hdr.rtp.padding == RTP_PADDING && hdr.rtp.extension == RTP_EXTENSION && hdr.rtp.csrcCounter == RTP_CSRC_COUNTER){ // hdr.udp.length_ >= 12
                //accumulated_frame_size = accumulated_frame_size + packet_size;

                if (hdr.rtp.marker == 1) {
                    //count rtp frames
                    num_frames_pkts = num_frames_pkts + 1;
                    if (num_frames_pkts >= 3){
                        value_to_write = meta.flowID;
                        num_frames_pkts = 0;

                        //classify.apply();
                        meta.classify = 1;
                    }
                    /* FS */
                    //frame_size = accumulated_frame_size;
                    current_seqNumber = hdr.rtp.seqNumber;
                    frame_size = ((bit<32>)(current_seqNumber - previous_seqNumber)) * packet_size;
                    //frame_size = (bit<32>) previous_seqNumber;

                    if (fs > 0) {
                        diff_ps = ((int<32>) frame_size) - ((int<32>) fs);
                        diff_ps = diff_ps >> 7;
                        fs = fs + (bit<32>) diff_ps;
                    } else {
                        fs = frame_size;
                    }
                    //accumulated_frame_size = 0;

                    /* IFI */
                    if (last_frame_start_time > 0) {
                        inter_frame_interval = current_time - last_frame_start_time;
                    } else {
                        inter_frame_interval = 0;
                    }
                    last_frame_start_time = current_time;

                    if (ifi > 0) {
                        diff_ts = ((int<48>) inter_frame_interval ) - ((int<48>) ifi);
                        diff_ts = diff_ts >> 7;
                        ifi = ifi + (bit<48>) diff_ts;
                    } else {
                        ifi = inter_frame_interval;
                    }

                }
            } else {
                // count pkts if is not rtp
                num_frames_pkts = num_frames_pkts + 1;
                    if (num_frames_pkts >= 10){
                        value_to_write = meta.flowID;
                        num_frames_pkts = 0;

                        //classify.apply();
                        meta.classify = 1;
                    }
            }
    

        }

        fid_reg.write(0, value_to_write);
        frames_pkts_counter.write((bit<32>)meta.flowID, num_frames_pkts);

        ps_register.write((bit<32>)meta.flowID, ps);
        ipi_register.write((bit<32>)meta.flowID, ipi);
        fs_register.write((bit<32>)meta.flowID, fs);
        ifi_register.write((bit<32>)meta.flowID, ifi);

        lpt_register.write((bit<32>)meta.flowID, last_packet_time);
        lfst_register.write((bit<32>)meta.flowID, last_frame_start_time);
        //a_fs_register.write((bit<32>)meta.flowID, accumulated_frame_size);
        if (current_seqNumber == 0) current_seqNumber = previous_seqNumber;
        seqNumber_register.write((bit<32>)meta.flowID, current_seqNumber);

        meta.ps = ps;
        meta.fs = fs;
        meta.ipi = ipi;

    }


    apply {
        bit<3> qid;
        bit<2> isUDP = 0;
        meta.flowID = 0;

        // forwarding to port
        if (hdr.nodeCount.isValid() && standard_metadata.instance_type == PKT_INSTANCE_TYPE_INGRESS_RECIRC) {
            send_back();
        } else {
            standard_metadata.egress_spec = (standard_metadata.ingress_port+1)%2;
        }

        

        // find flow id and extract features (ONLY DOWNLINK)
        if (standard_metadata.egress_spec == 0) {
            if (hdr.ipv4.isValid() && hdr.ipv4.protocol == PROTO_UDP) {
                isUDP = 1;
                find_flowID_ipv4();
                extract_features();
            } else if (hdr.ipv6.isValid() && hdr.ipv6.nextHdr == PROTO_UDP) {
                isUDP = 1;
                find_flowID_ipv6();
                extract_features();
            }

            // after every 10 pkts or 3 frames, classify the flow
            if (meta.classify == 1) {
                bit<3> major = 0;
                bit<3> max_count = 0;

                debug.count(0);

                // Run each tree and save their votes
                t1_feature1_exact.apply();
                t1_feature2_exact.apply();
                t1_feature3_exact.apply();
                t1_feature4_exact.apply();
                t1_classify_exact.apply();

                t2_feature1_exact.apply();
                t2_feature2_exact.apply();
                t2_feature3_exact.apply();
                t2_feature4_exact.apply();
                t2_classify_exact.apply();

                t3_feature1_exact.apply();
                t3_feature2_exact.apply();
                t3_feature3_exact.apply();
                t3_feature4_exact.apply();
                t3_classify_exact.apply();

                t4_feature1_exact.apply();
                t4_feature2_exact.apply();
                t4_feature3_exact.apply();
                t4_feature4_exact.apply();
                t4_classify_exact.apply();

                t5_feature1_exact.apply();
                t5_feature2_exact.apply();
                t5_feature3_exact.apply();
                t5_feature4_exact.apply();
                t5_classify_exact.apply();


                // Votes counting
                if (meta.count_other > max_count) {
                    max_count = meta.count_other;
                    major = 1;
                }

                if (meta.count_CG > max_count) {
                    max_count = meta.count_CG;
                    major = 2;
                }

                if (meta.count_AR > max_count) {
                    max_count = meta.count_AR;
                    major = 3;
                }

                // Use major result to assign queue
                if (major == 1) {
                    set_other();
                } else if (major == 2 || major == 3) { // for now CG and AR is going same queue
                    set_cg_ar();
                }

                // Only for debug and logging, can be removed 
                trees_result_reg.write(0, major);
                trees_result_reg.write(1, meta.result_t1);
                trees_result_reg.write(2, meta.result_t2);
                trees_result_reg.write(3, meta.result_t3);
                trees_result_reg.write(4, meta.result_t4);
                trees_result_reg.write(5, meta.result_t5);
                
            }
        } else {
            if (hdr.ipv4.isValid() && hdr.ipv4.protocol == PROTO_UDP) {
                isUDP = 1;
   
            } else if (hdr.ipv6.isValid() && hdr.ipv6.nextHdr == PROTO_UDP) {
                isUDP = 1;
            }
        }
        

        // setting queue of classified packets

        flow_queue.read(qid, (bit<32>)meta.flowID);
        if (qid == 0 && isUDP == 1) {
            qid = 1; // if classifier is off, assign queue 1 to UDP pkts manually
        }
        
        assign_q(qid);

        // setting queue of INT packets
        if (hdr.nodeCount.isValid()){
            if (hdr.ipv4.dstAddr == IP_INT_1) {
                ///int_pkts.count(1);
                qid = 1;
                assign_q(qid);
            } else if (hdr.ipv4.dstAddr == IP_INT_2) {
                //int_pkts.count(2);
                qid = 2;
                assign_q(qid);
            }
        }

        // forwarding ping test to each queue
        if (hdr.ipv4.isValid() && hdr.icmp.isValid()) {
            if (hdr.icmp.pattern == 0x6161) { // TCP
                qid = 0;
                icmp_pkts.count(0);
            } else if (hdr.icmp.pattern == 0x6262) { // UDP
                qid = 1;
                icmp_pkts.count(1);
            } else if (hdr.icmp.pattern == 0x6363) { // CG
                qid = 2;
                icmp_pkts.count(2);
            }
            //icmp_pattern_reg.write(0, hdr.icmp.pattern);
            //icmp_pkts.count(0);
            assign_q(qid);
        
        }



    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {

    counter(8, CounterType.packets) pqueues;

    register<enq_qdepth_v>(6) enq_qdepth_reg;
    register<deq_timedelta_v>(6) deq_timedelta_reg;
    register<deq_qdepth_v>(6) deq_qdepth_reg;
    register<deq_timedelta_v>(6) processing_time_reg;
    //register<bit<19>>(3) queue_length;
    register<bit<1>>(1) mark_ecn;

    action my_recirculate() {
        recirculate_preserving_field_list(0);
    }

    action save_telemetry_avg() {
        enq_qdepth_v enq_qdepth_avg;
        deq_timedelta_v deq_timedelta_avg;
        deq_qdepth_v deq_qdepth_avg;
        deq_timedelta_v processing_time_avg;
        deq_timedelta_v current_processing_time;

        int<19> diff_eq;
        int<32> diff_dt;
        int<19> diff_dq;
        int<32> diff_pt;

        bit<5> reg_index;
        if (standard_metadata.egress_port == 0){
            reg_index = standard_metadata.qid; 
        } else { //egress port == 1
            reg_index = standard_metadata.qid + 3;
        }

        enq_qdepth_reg.read(enq_qdepth_avg, (bit<32>)reg_index);
        deq_timedelta_reg.read(deq_timedelta_avg, (bit<32>)reg_index);
        deq_qdepth_reg.read(deq_qdepth_avg, (bit<32>)reg_index);
        processing_time_reg.read(processing_time_avg, (bit<32>)reg_index);

        if (deq_timedelta_avg == 0){ //if this is 0, the others are 0 too
            enq_qdepth_avg = standard_metadata.enq_qdepth;
            deq_timedelta_avg = standard_metadata.deq_timedelta;
            deq_qdepth_avg = standard_metadata.deq_qdepth;
            processing_time_avg = (standard_metadata.enq_timestamp - ((bit<32>)standard_metadata.ingress_global_timestamp)) + standard_metadata.deq_timedelta;
        } else {
            diff_eq = ((int<19>) standard_metadata.enq_qdepth) - ((int<19>) enq_qdepth_avg);
            diff_eq = diff_eq >> 7;
            enq_qdepth_avg = enq_qdepth_avg + (bit<19>) diff_eq;

            diff_dt = ((int<32>) standard_metadata.deq_timedelta) - ((int<32>) deq_timedelta_avg);
            diff_dt = diff_dt >> 7;
            deq_timedelta_avg = deq_timedelta_avg + (bit<32>) diff_dt;

            diff_dq = ((int<19>) standard_metadata.deq_qdepth) - ((int<19>) deq_qdepth_avg);
            diff_dq = diff_dq >> 7;
            deq_qdepth_avg = deq_qdepth_avg + (bit<19>) diff_dq;

            current_processing_time = (standard_metadata.enq_timestamp - ((bit<32>)standard_metadata.ingress_global_timestamp)) + standard_metadata.deq_timedelta;
            diff_pt = ((int<32>) current_processing_time) - ((int<32>) processing_time_avg);
            diff_pt = diff_pt >> 7;
            processing_time_avg = processing_time_avg + (bit<32>) diff_pt;
        }

        enq_qdepth_reg.write((bit<32>)reg_index, enq_qdepth_avg);
        deq_timedelta_reg.write((bit<32>)reg_index, deq_timedelta_avg);
        deq_qdepth_reg.write((bit<32>)reg_index, deq_qdepth_avg);
        processing_time_reg.write((bit<32>)reg_index, processing_time_avg);


    }

    action add_swtrace() {
        enq_qdepth_v enq_qdepth_avg;
        deq_timedelta_v deq_timedelta_avg;
        deq_qdepth_v deq_qdepth_avg;
        deq_timedelta_v processing_time_avg;

        bit<5> reg_index;
        if (standard_metadata.egress_port == 0){
            reg_index = standard_metadata.qid; 
        } else { //egress port == 1
            reg_index = standard_metadata.qid + 3;
        }

        enq_qdepth_reg.read(enq_qdepth_avg, (bit<32>)reg_index);
        deq_timedelta_reg.read(deq_timedelta_avg, (bit<32>)reg_index);
        deq_qdepth_reg.read(deq_qdepth_avg, (bit<32>)reg_index);
        processing_time_reg.read(processing_time_avg, (bit<32>)reg_index);

        hdr.nodeCount.count = hdr.nodeCount.count + 1;
        hdr.INT.push_front(1);
        hdr.INT[0].setValid();
        //1 para downlink, 2 para uplink
        if (hdr.nodeCount.count == 2){
            hdr.INT[0].swid = 1;
        } else {
            hdr.INT[0].swid = 2;
        }
        hdr.INT[0].ingress_port = (ingress_port_v)standard_metadata.ingress_port;
        hdr.INT[0].egress_port = (egress_port_v)standard_metadata.egress_port;
        hdr.INT[0].egress_spec = (egressSpec_v)standard_metadata.egress_spec;
        hdr.INT[0].priority = (priority_v)standard_metadata.priority;
        hdr.INT[0].qid = (qid_v)standard_metadata.qid;
        hdr.INT[0].ingress_global_timestamp = (ingress_global_timestamp_v)standard_metadata.ingress_global_timestamp;
        hdr.INT[0].egress_global_timestamp = (egress_global_timestamp_v)standard_metadata.egress_global_timestamp;
        hdr.INT[0].enq_timestamp = (enq_timestamp_v)standard_metadata.enq_timestamp;
        hdr.INT[0].enq_qdepth = (enq_qdepth_v)enq_qdepth_avg;
        hdr.INT[0].deq_timedelta = (deq_timedelta_v)deq_timedelta_avg;
        hdr.INT[0].deq_qdepth = (deq_qdepth_v)deq_qdepth_avg;
        hdr.INT[0].processing_time = (deq_timedelta_v)processing_time_avg;

        hdr.ipv4.totalLen = hdr.ipv4.totalLen + 72;

        enq_qdepth_avg = 0;
        deq_timedelta_avg = 0;
        deq_qdepth_avg = 0;
        processing_time_avg = 0;

        enq_qdepth_reg.write((bit<32>)reg_index, enq_qdepth_avg);
        deq_timedelta_reg.write((bit<32>)reg_index, deq_timedelta_avg);
        deq_qdepth_reg.write((bit<32>)reg_index, deq_qdepth_avg);
        processing_time_reg.write((bit<32>)reg_index, processing_time_avg);

     }

    apply {

        // counting number of pkts passed in each queue

        if (standard_metadata.qid == 0){
            pqueues.count(0);
        } else if (standard_metadata.qid == 1){
            pqueues.count(1);
        } else if (standard_metadata.qid == 2){
            pqueues.count(2);
        }

        // Mark ECN
        enq_qdepth_v occupancy = 0;
        bit<19> length = 0;
        bit<1> mark = 0;
        if (standard_metadata.qid == 1 && hdr.ipv4.ecn >= 0) {
            occupancy = standard_metadata.enq_qdepth;
            length = 64; //queue_length.read(length, 1);

            if (occupancy > ((length >> 1) + (length >> 2))) { // 75% of the queue
                mark = 1;
                hdr.ipv4.ecn = 3;

            } else if (occupancy > (length >> 1)) { // 50% of the queue
                mark_ecn.read(mark, 0);
                if (mark == 1) {
                    hdr.ipv4.ecn = 3;
                    mark = 0;
                } else {
                    mark = 1;
                }
                mark_ecn.write(0, mark);
            } 
        }
        //mark_ecn.write(0, mark);

        

        // saving queues metadata and recirculating
        if (hdr.nodeCount.isValid()) {
            add_swtrace();

            if (hdr.nodeCount.count < 2){
                my_recirculate();
            }

        } else {
            save_telemetry_avg();
        } 
    }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers hdr, inout metadata meta) {
     apply {
     }
}


/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.ipv6);
        packet.emit(hdr.udp);
        packet.emit(hdr.rtp);
        packet.emit(hdr.icmp);
        packet.emit(hdr.nodeCount);
        packet.emit(hdr.INT);
    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;