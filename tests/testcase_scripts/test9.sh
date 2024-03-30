#!/bin/bash

echo "Test 9: View registered classes for tutee (id: 4)"

response=$(curl -s -G -X GET "http://127.0.0.1:5000/api/view_registered_class" \
    -d "tutee_id=4" | jq .)

# Save the actual response to a file
echo "$response" | jq . > ../actual/tc9_output.json

if [ $? -eq 0 ]; then
    echo "test case 9: PASSED!"
else
    echo "test case 9: FAILED! Check ./actual/tc9_output.json"
fi
