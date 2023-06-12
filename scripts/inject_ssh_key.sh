#!/bin/bash

# This script copies a provided SSH private key to a specified Docker container
# and sets the file permissions to 600.

# Ensure the script is run with two arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <container_name> <id_rsa_file_path>"
    exit 1
fi

# Assign variables from the command line arguments
container_name="$1"
id_rsa_file_path="$2"

# Check if the provided file exists
if [ ! -f "$id_rsa_file_path" ]; then
    echo "Error: The provided SSH key file does not exist at the specified path: $id_rsa_file_path"
    exit 1
fi

# Generate a random string for temporary file name
temp_file="temp_id_rsa_$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)"

# Copy the id_rsa file to the Docker container's root directory with a temp name
docker cp "$id_rsa_file_path" "$container_name:/$temp_file"

# Check if the copy operation was successful
if [ "$?" -ne 0 ]; then
    echo "Error: Failed to copy the SSH key file to the Docker container"
    exit 1
fi

# Set the file permissions to 600 inside the Docker container
docker exec "$container_name" sh -c "chmod 600 /$temp_file"

# Check if the chmod operation was successful
if [ "$?" -ne 0 ]; then
    echo "Error: Failed to set the file permissions to 600 in the Docker container"
    exit 1
fi

# Rename the temporary file to .ssh/id_rsa inside the Docker container
docker exec "$container_name" sh -c "mv /$temp_file /root/.ssh/id_rsa"

# Check if the rename operation was successful
if [ "$?" -ne 0 ]; then
    echo "Error: Failed to move the SSH key file to its final location in the Docker container"
    exit 1
fi

echo "SSH key file successfully transferred to the Docker container and permissions set to 600"

exit 0
