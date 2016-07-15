#!/bin/bash -e

# 
# Goal: watermark CC notice to a photograph.
# Functionalities:
#   1. Resize the image to a fixed size (default to w = 1800, h = 1350)
#        If input image is larger, resize to a fitting size without distortion
#        If input image is smaller, only extend it to given size by white background
#   2. Overlay a given CC icon to bottom-left
#   3. Overlay a CC notice to bottom-right
# Requirement: ImageMagick 
# Usage: ./imageCCTagger.sh INPUT_FILE_NAME CC_TYPE CC_NOTICE [OUTPUT_FILE_NAME]
#    INPUT_FILE_NAME: Name of input file
#    CC_TYPE: Type of CC, can be: by, by-nc, by-nd, by-sa, by-nc-sa, by-nc-nd
#             icons from http://www.creativecommons.org.tw
#    CC_NOTICE: a message to be attached, ex: "CC(3.0) by John Doe, 2016"
#    OUTPUT_FILE_NAME: optional, if not provided, display the output directly
# Environment variables:
#   DISPLAY=1: display the result image
#   SIZE=WxH: resize image to width W, height H
#
# Notice: MimeType of OUTPUT_FILE_NAME determines the resulting image format.
#         Thus, if OUTPUT_FILE_NAME=foo.jpg, output image will be in JPEG
#

if [ $# -lt 2 ]; then
    echo "Usage: $0 INPUT_FILE_NAME CC_TYPE CC_NOTICE [OUTPUT_FILE_NAME]"
    exit
fi

INPUT_FILE=$1
CC_TYPE=$2
CC_NOTICE=$3
OUTPUT_FILE=$4
CC_ICON_DIR=icons
CC_ICON_FILE="$CC_ICON_DIR/cc-$CC_TYPE.png"

if [ ! -f $CC_ICON_FILE ]; then
    echo "Invalid CC type: $CC_TYPE"
    exit
fi
if [ ! "$SIZE" ]; then
    SIZE=1800x1350
fi
if [ ! "$OUTPUT_FILE" ]; then
    OUTPUT_FILE=$(mktemp)
    NO_OUTPUT=1
fi

convert $INPUT_FILE -resize $SIZE\> jpg:- | \
convert - -gravity Center -extent $SIZE -fill black jpg:- | \
convert -background '#00000005' -pointsize 12 -fill white label:"$CC_NOTICE" \
    -bordercolor '#00000070' -border 6x6 - +swap -gravity SouthEast -geometry +5+5 -composite jpg:- | \
composite -gravity SouthWest -geometry +5+5 $CC_ICON_FILE - "$OUTPUT_FILE"

if [ "$DISPLAY" = 1 ] || [ "$NO_OUTPUT" = 1 ]; then
    display $OUTPUT_FILE
    if [ "$NO_OUTPUT" = 1 ]; then
        rm $OUTPUT_FILE
    else
        echo $OUTPUT_FILE
    fi
fi
