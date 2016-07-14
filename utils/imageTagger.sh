#!/bin/bash -e

# 
# Goal: watermark the owner's name to a photograph.
# Functionalities:
#   1. Resize the image to a fixed size (default to w = 1800, h = 1350)
#        If input image is larger, resize to a fitting size without distortion
#        If input image is smaller, only extend it to given size by white background
#   2. Overlay a "CC BY" icon to bottom-left
#   3. Overlay the owner's name to bottom-right
# Requirement: ImageMagick 
# Usage: ./cc.sh INPUT_FILE_NAME IMAGE_OWNER [OUTPUT_FILE_NAME]
# Environment variables:
#   DISPLAY=1: display the result image
#   SIZE=WxH: resize image to width W, height H
#
# Notice: MimeType of OUTPUT_FILE_NAME determines the resulting image format.
#         Thus, if OUTPUT_FILE_NAME=foo.jpg, output image will be in JPEG
#

if [ $# -lt 2 ]; then
    echo "Usage: $0 INPUT_FILE_NAME IMAGE_OWNER [OUTPUT_FILE_NAME]"
    exit
fi

INPUT_FILE=$1
OWNER=$2
OUTPUT_FILE=$3
NO_OUTPUT=0

if [ ! "$SIZE" ]; then
    SIZE=1800x1350
fi
if [ ! "$OUTPUT_FILE" ]; then
    OUTPUT_FILE=$(mktemp)
    NO_OUTPUT=1
fi

convert $INPUT_FILE -resize $SIZE\> jpg:- | \
convert - -gravity Center -extent $SIZE -fill black jpg:- | \
convert -background '#00000005' -pointsize 12 -fill white label:"CC by $OWNER" \
    -bordercolor '#00000070' -border 6x6 - +swap -gravity SouthEast -geometry +5+5 -composite jpg:- | \
composite -gravity SouthWest -geometry +5+5 cc.png - "$OUTPUT_FILE"

if [ "$DISPLAY" = 1 ]; then
    echo $OUTPUT_FILE
    display $OUTPUT_FILE
fi
if [ "$NO_OUTPUT" = 1 ]; then
    rm $OUTPUT_FILE
fi
