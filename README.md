# In-Network AR/CG Traffic Classification Entirely Deployed in the Programmable Data Plane: Unlocking RTP Features and L4S Integration

[![netsoft2025](https://img.shields.io/badge/Click%20Me-Visit%20Now-blue)](https://netsoft2025.ieee-netsoft.org)


[The repository is related to the paper submitted to the Netsoft' 2025 conference and it is under construction!]


## (1) Connect & Clone P4 Code
      ssh [username]@[IP]    # Replace your username & Tofino IP
      pass: xxxx             # Tofino password

      # Clone the Repository on your Tofino
      git clone https://github.com/dcomp-leris/ARCG-DP-Deployment.git
      cd ARCG-DP-Deployment/Tofino/V2

**Output:**

   ![image](https://github.com/user-attachments/assets/59d0e906-fa76-41dd-93be-78a22efd0c05)


## (2) Compile the P4 Code in Tofino
      # Check to be in the froject folder
      ~/../p4_build.sh -p RF.p4

**Output:**

![image](https://github.com/user-attachments/assets/b742f937-c749-403c-82c4-92a3012e472a)

## (3) Run the P4 code

      # Run compiled P4 code (RF) on Tofino2
      ~/../run_switchd.sh  -p RF --arch tf2

**Output:**

![image](https://github.com/user-attachments/assets/2651dab0-8e8a-47c6-8e00-0a4416f0f0e0)

## (4) Run the Controllr code
      
      bfshell> bfrt_python

      # Set the CP.py file address
      bfrt_python> %load /home/alireza/ARCG-DP-Deployment/Tofino/V2/CP.py

**Output:**

![image](https://github.com/user-attachments/assets/3ad83274-003f-4869-a809-5250379c8058)


## (5) Results
RF AR/CG Classifier + Automatic ECT Marking + Forwarding (L4S + Classic) Queues are running!


![image](https://github.com/user-attachments/assets/cde365e7-f644-4c57-8498-8d291aa1a392)





 
