#!/bin/bash
FIRMWARES_PATH="builds"
SIZE_FILE="sizes.csv"

echo "firmware,size" > "$SIZE_FILE"
for FIRMWARE in "builds"/*
do
	FIRMWARE_NAME="$(basename $FIRMWARE)"
	# getting the firmware dimesion
	FIRMWARE_SIZE=$(du -k "$FIRMWARE" | cut -f1)
	echo "$FIRMWARE_NAME,$FIRMWARE_SIZE" >> "$SIZE_FILE"
	# run the same test with all the firmwares
	./$FIRMWARE -X heapsize=100M performance.py "$FIRMWARE_NAME"
done