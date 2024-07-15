#!/bin/bash

# Listen for slinktool -Q :18000 command
if [[ "$1" == "slinktool" && "$2" == "-Q" && "$3" == ":18000" ]]; then
    echo "Running slinktool -Q :18000..."

    # Run your Python script to process the output
    python3 /path/to/slinktool_output.py  # Replace with the actual path to your Python script
else
    # Print usage or handle other commands
    echo "Usage: $0 slinktool -Q :18000"
fi
