#!/bin/bash

# Define the base path for test scripts and output directories
SCRIPT_DIR="./testcase_scripts"
ACTUAL_DIR="./actual"
OUTPUT_DIR="./testcase_output"

echo "Starting all tests..."

# Ensure the actual and output directories exist
mkdir -p "$ACTUAL_DIR"
mkdir -p "$OUTPUT_DIR"

# Navigate to the script directory to run tests
cd "$SCRIPT_DIR" || exit

# Make all .sh files executable
chmod +x *.sh

# Find and run each test script in the testcase_scripts directory
for test_script in *.sh; do
    if [[ -f "$test_script" && -x "$test_script" ]]; then
        echo "Running $test_script..."
        ./"$test_script"
    else
        echo "Skipping $test_script: not executable or not found"
    fi
done

# Navigate back to the original tests directory
cd - > /dev/null

echo "All tests completed."
