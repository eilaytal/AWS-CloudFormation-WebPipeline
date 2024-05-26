#!/bin/bash

# Check if argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <new_version>"
    exit 1
fi

# Assign the new version from the argument
new_version="$1"

# Replace the value of "Version" parameter in the JSON file
sed -E -i "s/\"Version\" : \"V[0-9]\.[0-9]+\"/\"Version\" : \"V1.$new_version\"/" ./AWS/cloudformation-config.json

# Replace the value of "Version" in the HTML
sed -E -i "s/V[0-9]\.[0-9]+/V1.$new_version/" ./Frontend/labcom.html
