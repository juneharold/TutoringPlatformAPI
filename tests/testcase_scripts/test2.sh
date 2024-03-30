#!/bin/bash

# Adjust the following curl command based on your specific endpoint and data
echo "Test 2: Remove available time slot for Tutor (id: 1)"

response=$(curl -s -X DELETE "http://127.0.0.1:5000/api/delete_time" \
    -H "Content-Type: application/json" \
    -d '{"start_time": "2024-03-28 10:00:00", "end_time": "2024-03-28 11:00:00", "tutor_id": 1}' | jq .)

echo "$response" | jq . > ../actual/tc2_output.json

if [ $? -eq 0 ]; then
    echo "test case 2: PASSED!"
else
    echo "test case 2: FAILED! Check ./actual/tc2_output.json"
fi