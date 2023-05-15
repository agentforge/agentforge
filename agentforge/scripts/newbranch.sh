#!/bin/bash

# Check for correct number of arguments
if [ $# -ne 2 ]
then
    echo "Usage: $0 <upstream_branch> <new_branch>"
    exit 1
fi

# Assign arguments to variables
upstream_branch=$1
new_branch=$2

# Stash any changes
git stash

# Create a new branch and switch to it
git checkout -b $new_branch

# Set the upstream
git branch --set-upstream-to=$upstream_branch $new_branch

# Pop the stash
git stash pop

echo "Operation completed successfully."
