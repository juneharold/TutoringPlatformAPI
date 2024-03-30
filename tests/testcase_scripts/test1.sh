#!/bin/bash

# Adjust the following curl command based on your specific endpoint and data
echo "Test 1: Add available time slot for Tutor (id: 1)"

response=$(curl -s -X POST "http://127.0.0.1:5000/api/add_time" \
    -H "Content-Type: application/json" \
    -d '{"start_time": "2024-03-28 09:00:00", "end_time": "2024-03-28 12:00:00", "tutor_id": 1}' | jq .)

echo "$response" | jq . > ../actual/tc1_output.json

if [ $? -eq 0 ]; then
    echo "test case 1: PASSED!"
else
    echo "test case 1: FAILED! Check ./actual/tc1_output.json"
fi