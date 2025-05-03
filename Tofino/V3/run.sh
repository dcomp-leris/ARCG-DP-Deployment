#!/bin/bash

# Usage: ./run_switch.sh RF

if [ -z "$1" ]; then
  echo "Usage: $0 <program_name>"
  exit 1
fi

PROGRAM_NAME="$1"
LOG_FILE="switchd_output_$PROGRAM_NAME.log"

echo "🚀 Running switchd with program: $PROGRAM_NAME"
echo "📝 Output will also be logged to $LOG_FILE"
echo "---------------------------------------------"

# Run the command and show + save output
/home/leris/sde/bf-sde-9.13.4/run_switchd.sh -p "$PROGRAM_NAME" --arch tft2 | tee "$LOG_FILE"

EXIT_CODE=${PIPESTATUS[0]}
echo "---------------------------------------------"
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ switchd ran successfully for $PROGRAM_NAME"
else
    echo "❌ switchd exited with code $EXIT_CODE. Check $LOG_FILE for details."
fi

