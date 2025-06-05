#!/bin/bash

# === Prompt for interface name ===
read -p "Enter the interface name to capture from (e.g., enp2s0np0): " IFACE

# === Prompt for PCAP file name and location ===
read -e -p "Enter output PCAP file path (default: ./my.pcap): " PCAP_FILE
PCAP_FILE=${PCAP_FILE:-./my.pcap}  # Use default if empty

echo "Capturing on interface: $IFACE"
echo "Saving to file: $PCAP_FILE"

# === Start full packet capture ===
sudo tshark -i "$IFACE" -f "ip" -w "$PCAP_FILE" &
PID1=$!

# === Start live IP/DSCP/ECN monitoring ===
sudo tshark -i "$IFACE" -f "ip" -T fields -e ip.src -e ip.dst -e ip.dsfield.dscp -e ip.dsfield.ecn &
PID2=$!

# === Wait for both tshark processes ===
wait $PID1 $PID2