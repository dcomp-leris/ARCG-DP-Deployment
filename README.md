# In-Network AR/CG Traffic Classification Entirely Deployed in the Programmable Data Plane: Unlocking RTP Features and L4S Integration

[![Conference](https://img.shields.io/badge/submitted-Netsoft2025-blue)](https://netsoft2025.ieee-netsoft.org)
[![Conference](https://img.shields.io/badge/Acceptance-Netsoft2025-yellow)](https://netsoft2025.ieee-netsoft.org)
[![Event](https://img.shields.io/badge/Event-Netsoft2025-red)](https://netsoft2025.ieee-netsoft.org/program)


### **Note:**
This paper has been submitted to the Netsoft 2025 Conference and was accepted!

## General View 
This repository is going to run the Random Forest (RF) model in tofino 2 to identify the AR/CG **_flows_** & mark AR/CG **_packets_** with ECT(1) as shown in Fig.1. It paves the way for AR/CG to be routed through L4S Queue.  

<p align="center">
  <img src="https://github.com/user-attachments/assets/9f14e123-1f02-438b-8fdf-82282033ff8e" alt="Descriptive Alt Text" width="500" height="auto" style="display: block; margin: 0 auto; max-width: 100%;">
</p>

## Topology & Setup
To do the experiment, we use the below topology and setup to evaluate the model as shown in Fig.4. 

<p align="center">
  <img src="https://github.com/user-attachments/assets/bfbbd937-484f-4e5c-97ab-f0a8b168bc75" alt="Descriptive Alt Text" width="500" height="auto" style="display: block; margin: 0 auto; max-width: 100%;">
</p>



### (A) P4 Code Copiling & Running on Tofino 2 

  #### (1) Connect to Tofino & Clone P4 Code from the repository
      ssh [username]@[IP]    # Replace your username & Tofino IP
      pass: xxxx             # Tofino password

      # Clone the Repository on your Tofino
      git clone https://github.com/dcomp-leris/ARCG-DP-Deployment.git
      cd ARCG-DP-Deployment/Tofino/V3

**Output:**

   ![image](https://github.com/user-attachments/assets/59d0e906-fa76-41dd-93be-78a22efd0c05)


  ##### (2) Compile the P4 Code in Tofino
      # Ensure you are in "~/ARCG-DP-Deployment/Tofino/V3" then
      ~/../p4_build.sh -p RF.p4

**Output:**

![image](https://github.com/user-attachments/assets/b742f937-c749-403c-82c4-92a3012e472a)

  ####   (3) Run the P4 code

      # Run compiled P4 code (RF) on Tofino2 (tf2)
      ~/../run_switchd.sh  -p RF --arch tf2

**Output:**

![image](https://github.com/user-attachments/assets/2651dab0-8e8a-47c6-8e00-0a4416f0f0e0)

####     (4) Run the Controllr code
      
      bfshell> bfrt_python

      # Set the CP.py file address
      bfrt_python> %load /home/alireza/ARCG-DP-Deployment/Tofino/V3/CP.py

**Output:**

![image](https://github.com/user-attachments/assets/3ad83274-003f-4869-a809-5250379c8058)


####     (5) Results
RF AR/CG Classifier + Automatic ECT Marking + Forwarding (L4S + Classic) Queues are running!

### (B) Server 1 Configuration 




 
