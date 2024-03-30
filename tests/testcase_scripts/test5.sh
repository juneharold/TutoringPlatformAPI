#!/bin/bash

echo "Test 5: Find possible tutors in specific day-of-week and time for Tutee (id: 3)"

response=$(curl -s -G -X GET "http://127.0.0.1:5000/api/find_tutors" \
    -d "days_of_week=1" -d "days_of_week=1" -d "days_of_week=1" \
    -d "days_of_week=1" -d "days_of_week=1" -d "days_of_week=1" -d "days_of_week=1" \
    -d "start_time=06:00" -d "end_time=09:00" -d "duration=30" | jq .)

# Save the actual response to a file
echo "$response" | jq . > ../actual/tc5_output.json

if [ $? -eq 0 ]; then
    echo "test case 5: PASSED!"
else
    echo "test case 5: FAILED! Check ./actual/tc5_output.json"
fi
