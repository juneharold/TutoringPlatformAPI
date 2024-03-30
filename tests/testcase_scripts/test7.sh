#!/bin/bash

# Adjust the following curl command based on your specific endpoint and data
echo "Test 7:  Register for class in existing time for tutee (id: 3)"

response=$(curl -s -X PUT "http://127.0.0.1:5000/api/register_class" \
    -H "Content-Type: application/json" \
    -d '{"start_time": "2024-03-28 09:00:00", "duration": 30, "tutor_id": 1, "tutee_id": 3}' | jq .)

echo "$response" | jq . > ../actual/tc7_output.json

if [ $? -eq 0 ]; then
    echo "test case 7: PASSED!"
else
    echo "test case 7: FAILED! Check ./actual/tc7_output.json"
fi
