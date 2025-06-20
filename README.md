# In-Network AR/CG Traffic Classification Entirely Deployed in the Programmable Data Plane: Unlocking RTP Features and L4S Integration

[![Conference](https://img.shields.io/badge/submitted-Netsoft2025-blue)](https://netsoft2025.ieee-netsoft.org)
[![Conference](https://img.shields.io/badge/Acceptance-Netsoft2025-yellow)](https://netsoft2025.ieee-netsoft.org)
[![paper](https://img.shields.io/badge/Paper-Netsoft2025-red)](Netsoft2025_Paper.pdf)
[![Presentation](https://img.shields.io/badge/Presentation-Netsoft2025-green)](https://docs.google.com/presentation/d/17G_gH58o-Is9wHY_llHknBOVOjm30t07b-QE5o4wmqM/edit?usp=sharing)



### **Note:**
This paper has been submitted to the Netsoft 2025 Conference and was accepted!

## AR/CG Flow classification + Packets Marking + L4S
This repository is going to run the Random Forest (RF) model in tofino 2 to identify the AR/CG **_flows_** & mark AR/CG **_packets_** with ECT(1) as shown in Fig.1. It paves the way for AR/CG to be routed through L4S Queue.  

<p align="center">
  <img src="https://github.com/user-attachments/assets/9f14e123-1f02-438b-8fdf-82282033ff8e" alt="Descriptive Alt Text" width="500" height="auto" style="display: block; margin: 0 auto; max-width: 100%;">
</p>

## Repository Navigation

![image](https://github.com/user-attachments/assets/b9dcc6b3-aa36-4020-af0e-c62e204c524e)






## Topology & Setup
To do the experiment, we use the below topology and setup to evaluate the model as shown in Fig.4. 

<p align="center">
  <img src="https://github.com/user-attachments/assets/bfbbd937-484f-4e5c-97ab-f0a8b168bc75" alt="Descriptive Alt Text" width="500" height="auto" style="display: block; margin: 0 auto; max-width: 100%;">
</p>

In this topology, we have three componenets: (A) Tofino Switch, (B) Server 1, and (C) Server 2. 
To run the topology to reproduce the results, we must follow the order as below:
1. Compile and Run Tofino Switch (Section A)
2. Run Server 2 (Section C)
3. Run Server 1 (Section B)

## (A) Compiling & Running P4 Code on Tofino 2 Switch 

### (A-1) **Connect Tofino & Clone P4 Code**
      ssh [username]@[IP]    # Replace your username & Tofino IP
      pass: xxxx             # Tofino password

      # Clone the Repository on your Tofino
      git clone https://github.com/dcomp-leris/ARCG-DP-Deployment.git
      cd ARCG-DP-Deployment/Tofino/V3

**Output:**

> Cloning into 'ARCG-DP-Deployment'...
> remote: Enumerating objects: 308, done.
> remote: Counting objects: 100% (76/76), done.
> remote: Compressing objects: 100% (61/61), done.
> remote: Total 308 (delta 22), reused 39 (delta 9), pack-reused 232 (from 1)
> Receiving objects: 100% (308/308), 6.04 MiB | 10.65 MiB/s, done.
> Resolving deltas: 100% (105/105), done.





#### (A-2) Compile the P4 Code in Tofino
      # Ensure you are in "~/ARCG-DP-Deployment/Tofino/V3" then
      ~/../p4_build.sh -p RF.p4

**Output:**

> Using SDE          /home/leris/sde/bf-sde-9.13.4
> Using SDE_INSTALL /home/leris/sde/bf-sde-9.13.4/install
> Using SDE version bf-sde-9.13.4

> OS Name: Ubuntu 20.04.6 LTS
> This system has 8GB of RAM and 8 CPU(s)
> Parallelization:  Recommended: -j4   Actual: -j4

> Compiling for p4_16/t2na
> P4 compiler path:    /home/leris/sde/bf-sde-9.13.4/install/bin/bf-p4c
> P4 compiler version: 9.13.4 (SHA: 3b52315) (p4c-based)
> Build Dir: /home/leris/sde/bf-sde-9.13.4/build/p4-build/tofino2/RF
> Logs Dir: /home/leris/sde/bf-sde-9.13.4/logs/p4-build/tofino2/RF

>  Building RF        CLEAR CMAKE MAKE INSTALL ... DONE


#### (A-3) Run the P4 code

      # Run compiled P4 code (RF) on Tofino2 (tf2)
      ~/../run_switchd.sh  -p RF --arch tf2

**Output:**

> Using SDE /home/leris/sde/bf-sde-9.13.4
> Using SDE_INSTALL /home/leris/sde/bf-sde-9.13.4/install
> Setting up DMA Memory Pool
> Using TARGET_CONFIG_FILE /home/leris/sde/bf-sde-9.13.4/install/share/p4/targets/tofino2/RF.conf
> Using SDE_DEPENDENCIES /home/leris/sde/bf-sde-9.13.4/install
> Using PATH /home/leris/sde/bf-sde-9.13.4/install/bin:/home/leris/sde/bf-sde-9.13.4/install/bin:/home/leris/sde/bf-sde-9.13.4/install/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
> Using LD_LIBRARY_PATH /home/leris/sde/bf-sde-9.13.4/install/lib:/home/leris/sde/bf-sde-9.13.4/install/lib:/usr/local/lib:/home/leris/sde/bf-sde-9.13.4/install/lib:/usr/local/lib
> kernel mode packet driver present, forcing kernel_pkt option!
> 2025-06-03 18:44:55.312205 BF_SWITCHD DEBUG - bf_switchd: system services initialized
> 2025-06-03 18:44:55.312291 BF_SWITCHD DEBUG - bf_switchd: loading conf_file /home/leris/sde/bf-sde-9.13.4/install/share/p4/targets/tofino2/RF.conf...
> 2025-06-03 18:44:55.312348 BF_SWITCHD DEBUG - bf_switchd: processing device configuration...
> 2025-06-03 18:44:55.312450 BF_SWITCHD DEBUG - Configuration for dev_id 0
> 2025-06-03 18:44:55.312482 BF_SWITCHD DEBUG -   Family        : tofino2
> 2025-06-03 18:44:55.312510 BF_SWITCHD DEBUG -   pci_sysfs_str : /sys/devices/pci0000:00/0000:00:03.0/0000:05:00.0
> 2025-06-03 18:44:55.312537 BF_SWITCHD DEBUG -   pci_int_mode  : 0
> 2025-06-03 18:44:55.312564 BF_SWITCHD DEBUG -   sds_fw_path   : share/tofino_sds_fw/avago/firmware
> 2025-06-03 18:44:55.312592 BF_SWITCHD DEBUG - bf_switchd: processing P4 configuration...
> 2025-06-03 18:44:55.312660 BF_SWITCHD DEBUG - coal_mirror_enable=0 coal_min=0 sessions_num=0
> 2025-06-03 18:44:55.312697 BF_SWITCHD DEBUG - P4 profile for dev_id 0
> 2025-06-03 18:44:55.312724 BF_SWITCHD DEBUG - num P4 programs 1
> 2025-06-03 18:44:55.312751 BF_SWITCHD DEBUG -   p4_name: RF
> 2025-06-03 18:44:55.312779 BF_SWITCHD DEBUG -   p4_pipeline_name: pipe
> 2025-06-03 18:44:55.312806 BF_SWITCHD DEBUG -     libpd: 
> 2025-06-03 18:44:55.312833 BF_SWITCHD DEBUG -     libpdthrift: 
> 2025-06-03 18:44:55.312860 BF_SWITCHD DEBUG -     context: /home/leris/sde/bf-sde-9.13.4/install/share/tofino2pd/RF/pipe/context.json
> 2025-06-03 18:44:55.312888 BF_SWITCHD DEBUG -     config: /home/leris/sde/bf-sde-9.13.4/install/share/tofino2pd/RF/pipe/tofino2.bin
> 2025-06-03 18:44:55.312916 BF_SWITCHD DEBUG -   Pipes in scope [
> 2025-06-03 18:44:55.312943 BF_SWITCHD DEBUG - 0 
> 2025-06-03 18:44:55.312970 BF_SWITCHD DEBUG - 1 
> 2025-06-03 18:44:55.312997 BF_SWITCHD DEBUG - 2 
> 2025-06-03 18:44:55.313023 BF_SWITCHD DEBUG - 3 
> 2025-06-03 18:44:55.313049 BF_SWITCHD DEBUG - ]
> 2025-06-03 18:44:55.313076 BF_SWITCHD DEBUG -   diag: 
> 2025-06-03 18:44:55.313103 BF_SWITCHD DEBUG -   accton diag: 
> 2025-06-03 18:44:55.313130 BF_SWITCHD DEBUG -   Agent[0]: /home/leris/sde/bf-sde-9.13.4/install/lib/libpltfm_mgr.so
> 2025-06-03 18:44:55.335540 BF_SWITCHD DEBUG - bf_switchd: library /home/leris/sde/bf-sde-9.13.4/install/lib/libpltfm_mgr.so loaded
> 2025-06-03 18:44:55.336830 BF_SWITCHD DEBUG - bf_switchd: agent[0] initialized
> Health monitor started 
> 2025-06-03 18:44:58.303403 BF_SWITCHD DEBUG - Device 0: Operational mode set to ASIC
> 2025-06-03 18:44:58.303506 BF_SWITCHD DEBUG - Initialized the device types using platforms infra API
> 2025-06-03 18:44:58.303544 BF_SWITCHD DEBUG - ASIC detected at PCI /sys/class/bf/bf0/device
> 2025-06-03 18:44:58.303637 BF_SWITCHD DEBUG - ASIC pci device id is 272 (0x0110)
> 2025-06-03 18:44:58.392037 BF_SWITCHD DEBUG - Skipped pkt-mgr init
> Starting PD-API RPC server on port 9090
> 2025-06-03 18:44:58.392927 BF_SWITCHD DEBUG - bf_switchd: drivers initialized
> /2025-06-03 18:45:17.790945 BF_PLTFM ERROR - ChkSum not matched for 15
> 
> 2025-06-03 18:45:19.272961 BF_SWITCHD DEBUG - bf_switchd: dev_id 0 initialized
> 2025-06-03 18:45:19.273029 BF_SWITCHD DEBUG - bf_switchd: initialized 1 devices
> Adding Thrift service for bf-platforms to server
> 2025-06-03 18:45:19.273286 BF_SWITCHD DEBUG - bf_switchd: thrift initialized for agent : 0
> 2025-06-03 18:45:19.273323 BF_SWITCHD DEBUG - bf_switchd: spawning cli server thread
> 2025-06-03 18:45:19.273597 BF_SWITCHD DEBUG - bf_switchd: spawning driver shell
> 2025-06-03 18:45:19.273756 BF_SWITCHD DEBUG - bf_switchd: server started - listening on port 9999
> bfruntime gRPC server started on 0.0.0.0:50052
> 
>         ********************************************
>         *      WARNING: Authorised Access Only     *
>         ********************************************
>     



#### (A-4) Run the Controllr code
      
      bfshell> bfrt_python

      # Set the CP.py file address
      bfrt_python> %load /home/alireza/ARCG-DP-Deployment/Tofino/V3/CP.py

**Output:**

> bfrt_python> %load /home/alireza/ARCG-DP-Deployment/Tofino/CP.py
> 
>         ...:             votes[key.strip()] = int(value.strip())
>         ...: 
>         ...:         # Use the BFRT API to add the entry
>         ...:         bfrt.RF.pipe.Ingress.table_majority.add_with_trees_aggregation(
>         ...:             metadata_classT1 = votes['t1'],
>         ...:             metadata_classT2 = votes['t2'],
>         ...:             metadata_classT3 = votes['t3'],
>         ...:             metadata_classT4 = votes['t4'],
>         ...:             metadata_classT5 = votes['t5'],
>         ...:             majority        = votes['m']
>         ...:         )

    
#### (A-5) Run Monitoring
To monitor the values, we can monitor the *FlowID*, *PS*, *IPG*, *FS*, *IFG* *t1*, *t2*, *t3*, *t4*, *t5*, *host_ifg*. run the *monitoring.py*. Open another terminal in Tofino2 and run:

    python3 monitoring.py
     
**Output:**
```
Subscribe attempt #1
Subscribe response received 0
Connected to BF Runtime Server as client 0
Received RF on GetForwarding on client 0, device 0
The target runs the program  RF
Binding with p4_name RF
Binding with p4_name RF successful!!
FlowID, PS, IPG, FS, IFG t1, t2, t3, t4, t5, host_ifg
0, 3, 497673774, 0, 0, 3, 3, 3, 3, 3,0.0
```


#### (A-6) Results
RF AR/CG Classifier + Automatic ECT Marking + Forwarding (L4S + Classic) Queues are running!

### (B) Server 1
#### (B-1) Installation:

* Operating System (OS) Ubuntu 20.04.6 LTS or later.
* [Tcpreplay Installation](https://tcpreplay.appneta.com)
* [Download AR/CG PCAPs](https://github.com/dcomp-leris/VR-AR-CG-network-telemetry.git)
#### (B-2) Server1 Functions

* Check the *Tcpreplay* installation.
* Read the PCAPs
* Replay the PCAPs through the Interface connected to the Tofino 2

#### (B-4) Run the *replay.sh*
```
cd ./ARCG-DP-Deployment/server1
./replay.sh 
```


**Output:**

> tcpreplay is already installed.
> Q1. Enter the name of the interface connected to Tofino2 (e.g., eth0)? [eth0]
> Q2. Enter the path to the PCAP folder (e.g., ./pcap_pool)? [./pcap_pools]
> Replaying ./pcap_pools/ar.pcap on interface eth0...

**Note:** This script asks two questions Q1 [interface] and Q2 [PCAP address] then starts to replaying the traffic.


### (C)Server 2
#### (C-1) Installation 
* Tshark
    ```
        sudo apt update
        sudo apt install -y tshark
    ```
* Python3
    ```
        sudo apt update
        sudo apt install python3
    ``` 
#### (C-2) Capturing the Received PCAPs
* Get the Interface to listen to it!
* Get the address and pcap file name to store in the local storage.    
* Run the *capturing.sh* script
    ```
        cd ./ARCG-DP-Deployment/server2
        ./capturing.sh
    ```
    **Output:**
> Q1. Enter the interface name to capture from (e.g., enp2s0np0)? [enp2s0np0]
> Q2. Enter output PCAP file path (default: ./my.pcap)? [./ar.pcap]
> Capturing on interface: enp2s0np0
> Saving to file: ./ar.pcap
> Capturing on 'enp2s0np0'
> tshark: The file to which the capture would be saved ("./ar.pcap")
> 172.16.0.1	224.0.0.251	0	0
> 172.16.0.1	224.0.0.251	0	0

        
#### (C-3) INT

There is a prob INT packet to collect the queues (Classic & L4S) logs:
* Queue Latency(ns)
* Queue Occupancy (number of packets)
* Nodal Processing Time (ns) (Egress - Ingress)

This INT has *sender.py* & *Receiver.py* which should be run respectively.
##### (C-3-1) Run the *receiver.py* packets (Terminal 1)
```
    cd ./ARCG-DP-Deployment/INT 
    python3 receiver.py 0 300 # ID = 0 & Duration is 5 min = 300 s
```
Note: Received data is stored in the folder called *data*.

##### (C-3-2) Run the *sender.py* packets (Open other new Terminal 2)

```
cd ./ARCG-DP-Deployment/INT
python sender.py
```

