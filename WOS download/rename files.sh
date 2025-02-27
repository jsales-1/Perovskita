#!/usr/bin/env bash

# Set the folder you want to rename files in. 
# If you want to use the current directory, you can leave it as "."
TARGET_DIR="./perovskites_2020_2025"

# The prefix you want to add to each file
PREFIX="3_"

# Change to the target directory
cd "$TARGET_DIR" || exit 1

# Loop through all files in the directory
for FILE in *; do
  # Skip directories or hidden files as needed, adjust accordingly
  if [ -f "$FILE" ]; then
    # Construct new name
    NEW_NAME="${PREFIX}${FILE}"

    # Rename (mv) the file
    mv "$FILE" "$NEW_NAME"
    echo "Renamed '$FILE' to '$NEW_NAME'"
  fi
done
