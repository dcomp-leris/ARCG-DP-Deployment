
#!/bin/bash

PROGRAM="$1"

if [ -z "$PROGRAM" ]; then
  echo "Usage: $0 <p4-program-name>"
  exit 1
fi

echo "🔍 Killing any process using port 9090..."
sudo fuser -k 9090/tcp

echo "🔁 Loading kernel drivers..."
sudo /home/leris/sde/bf-sde-9.13.4/install/libexec/bf_kdrv_mod_load

echo "🌍 Sourcing environment..."
cd /home/leris
source prepare_env-SDE.sh
cd /home/leris/sde/bf-sde-9.13.4
source ../tools/set_sde.bash

echo "🚀 Running switchd for $PROGRAM"
cd /home/alireza/ARCG-DP-Deployment/Tofino/V3
/home/leris/sde/bf-sde-9.13.4/run_switchd.sh -p "$PROGRAM" --arch tf2
