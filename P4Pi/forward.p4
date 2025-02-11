/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_IPV6 = 0x86dd;
const bit<16> TYPE_IPV4  = 0x0800;

const bit<8> PROTO_INT = 253;
const bit<8> PROTO_TCP = 6;
const bit<8> PROTO_UDP = 17;
const bit<8> PROTO_ICMP = 1;

const bit<32> IP_INT_0 = 0x0a0a0a01; //10.10.10.1
const bit<32> IP_INT_1 = 0x0a0a0a02; //10.10.10.2
const bit<32> IP_INT_2 = 0x0a0a0a03; //10.10.10.3
const bit<32> IP_GATEWAY = 0xc8126601; //200.18.102.1
const bit<32> IP_ALIREZA = 0xc812661c; //200.18.102.28


const bit<2>  RTP_VERSION = 2;
const bit<1>  RTP_PADDING = 0;
const bit<1>  RTP_EXTENSION = 1;
const bit<4>  RTP_CSRC_COUNTER = 0;

const bit<1>  TRUE = 1;
const bit<1>  FALSE = 0;

#define PKT_INSTANCE_TYPE_NORMAL 0
#define PKT_INSTANCE_TYPE_INGRESS_CLONE 1
#define PKT_INSTANCE_TYPE_EGRESS_CLONE 2
#define PKT_INSTANCE_TYPE_COALESCED 3
#define PKT_INSTANCE_TYPE_INGRESS_RECIRC 4


#define MAX_HOPS 10

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

typedef bit<16> flowID_t;
typedef bit<32> int_t;
typedef bit<128> features_info_t;
typedef bit<160> features_t;
typedef bit<48> timestamp_t;

typedef bit<31> switchID_v;
typedef bit<9> ingress_port_v;
typedef bit<9> egress_port_v;
typedef bit<9>  egressSpec_v;
typedef bit<3>  priority_v;
typedef bit<5>  qid_v;
typedef bit<48>  ingress_global_timestamp_v;
typedef bit<48>  egress_global_timestamp_v;
typedef bit<32>  enq_timestamp_v;
typedef bit<19> enq_qdepth_v;
typedef bit<32> deq_timedelta_v;
typedef bit<19> deq_qdepth_v;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
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
    int_t ipi;

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
    //register<bit<16>>(1) fid_reg;
    //register<bit<4>>(0xffff) frames_pkts_counter;

    counter(3, CounterType.packets) icmp_pkts;
    register<bit<16>>(1) icmp_pattern_reg;

    action drop() {
        mark_to_drop(standard_metadata);
    }

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

    action assign_q(bit<3> qid) {
        standard_metadata.priority = qid;
    }


    apply {
        bit<3> qid;
        bit<2> isUDP = 0;
        meta.flowID = 0;

        // find flow id
        if (hdr.ipv4.isValid() && hdr.ipv4.protocol == PROTO_UDP) {
            isUDP = 1;
            find_flowID_ipv4();
        } else if (hdr.ipv6.isValid() && hdr.ipv6.nextHdr == PROTO_UDP) {
            isUDP = 1;
            find_flowID_ipv6();
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
            icmp_pattern_reg.write(0, hdr.icmp.pattern);
            //icmp_pkts.count(0);
            assign_q(qid);
        
        }

        // forwarding to port
        if (hdr.nodeCount.isValid() && standard_metadata.instance_type == PKT_INSTANCE_TYPE_INGRESS_RECIRC) {
            send_back();
        } else {
            standard_metadata.egress_spec = (standard_metadata.ingress_port+1)%2;
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