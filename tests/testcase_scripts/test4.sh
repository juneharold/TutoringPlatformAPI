#!/bin/bash

echo "Test 4:  Find possible time-slots for classes for Tutee (id: 3)"

response=$(curl -s -G -X GET "http://127.0.0.1:5000/api/find_classes" \
    --data-urlencode "start_time=2024-03-28 06:00:00" \
    --data-urlencode "end_time=2024-03-28 13:00:00" \
    --data-urlencode "duration=30" | jq .)

echo "$response" | jq . > ../actual/tc4_output.json

if [ $? -eq 0 ]; then
    echo "test case 4: PASSED!"
else
    echo "test case 4: FAILED! Check ./actual/tc4_output.json"
fi