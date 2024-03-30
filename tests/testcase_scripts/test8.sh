#!/bin/bash

echo "Test 8: View registered classes for tutee (id: 3)"

response=$(curl -s -G -X GET "http://127.0.0.1:5000/api/view_registered_class" \
    -d "tutee_id=3" | jq .)

# Save the actual response to a file
echo "$response" | jq . > ../actual/tc8_output.json

if [ $? -eq 0 ]; then
    echo "test case 8: PASSED!"
else
    echo "test case 8: FAILED! Check ./actual/tc8_output.json"
fi
