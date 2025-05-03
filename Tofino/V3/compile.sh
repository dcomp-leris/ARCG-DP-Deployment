#!/bin/bash

# ========= Step 0: Validate Input =========
if [ $# -ne 1 ]; then
    echo "Usage: $0 <P4 filename>"
    exit 1
fi

P4_FILE="$1"
WORK_DIR="/home/alireza/ARCG-DP-Deployment/Tofino/V3"
LOG_FILE="/tmp/p4_compile_output.log"

if [ ! -f "$WORK_DIR/$P4_FILE" ]; then
    echo "❌ Error: File '$P4_FILE' not found in $WORK_DIR"
    exit 1
fi

echo "🔧 Preparing environment..."

# ========= Step 1: Source environments =========
cd /home/leris || exit 1
source prepare_env-SDE.sh

cd /home/leris/sde/bf-sde-9.13.4 || exit 1
source ../tools/set_sde.bash

# ========= Step 2: Build the P4 program =========
cd "$WORK_DIR" || exit 1
echo "🚀 Compiling '$P4_FILE' now..."
echo "🔍 Build log will be saved to $LOG_FILE"

# Run build and log output
/home/leris/sde/tools/p4_build.sh -p "$P4_FILE" 2>&1 | tee "$LOG_FILE"

# ========= Step 3: Show result summary =========
echo -e "\n📄 Build Summary:"
if grep -q "FAILED" "$LOG_FILE"; then
    echo "❌ Build failed. Showing key issues:"
    echo "--------------------------------------------------"
    grep -Ei "error|warning|FAILED" "$LOG_FILE" | tail -n 20
    echo "--------------------------------------------------"
else
    echo "✅ Build completed successfully!"
fi
