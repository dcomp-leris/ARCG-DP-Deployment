#!/bin/bash

# === Check and install tcpreplay if not installed ===
if ! command -v tcpreplay &> /dev/null; then
    echo "tcpreplay not found. Installing..."
    sudo apt update && sudo apt install -y tcpreplay
else
    echo "tcpreplay is already installed."
fi

# === Prompt for interface ===
read -p "Q1. Enter the name of the interface connected to Tofino2 (e.g., eth0)? " INTERFACE

# === Prompt for PCAP directory (with auto-complete) ===
read -e -p "Q2. Enter the path to the PCAP folder (e.g., ./pcap_pool)? " PCAP_DIR

# === Replay each PCAP/PCAPNG file ===
for pcap in "$PCAP_DIR"/*.pcap "$PCAP_DIR"/*.pcapng; do
    [ -e "$pcap" ] || continue
    echo "Replaying $pcap on interface $INTERFACE..."
    sudo tcpreplay --intf1="$INTERFACE" "$pcap"
done