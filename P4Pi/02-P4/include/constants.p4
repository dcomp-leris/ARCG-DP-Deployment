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