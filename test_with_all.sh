#!/bin/bash
FIRMWARES_PATH="builds"
SIZE_FILE="sizes.csv"

echo "firmware,size,SLOC" > "$SIZE_FILE"
for FIRMWARE in "builds"/*
do
	if [ -L "$FIRMWARE" ]; then
		FIRMWARE_PATH=$(readlink -f "$FIRMWARE")
	else
		FIRMWARE_PATH="$FIRMWARE"
	fi

	echo $FIRMWARE_PATH
	FIRMWARE_NAME="$(basename $FIRMWARE)"
	# getting the firmware dimesion
	FIRMWARE_SIZE=$(du -k "$FIRMWARE_PATH" | cut -f1)
	SLOC=$(objdump -d "$FIRMWARE_PATH" | wc -l)
	echo $SLOC
	echo "$FIRMWARE_NAME,$FIRMWARE_SIZE,$SLOC" >> "$SIZE_FILE"
	# run the same test with all the firmwares
	# ./$FIRMWARE -X heapsize=4096M performance.py "$FIRMWARE_NAME"
done