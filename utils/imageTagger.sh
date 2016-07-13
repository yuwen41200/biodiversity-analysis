#!/bin/bash -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 INPUT_FILE_NAME IMAGE_OWNER [OUTPUT_FILE_NAME]"
    exit
fi

INPUT_FILE=$1
OWNER=$2
OUTPUT_FILE=$3
CONVERT=/usr/bin/convert
COMPOSITE=/usr/bin/composite
DISPLAY_BIN=/usr/bin/display
SIZE=1800x1350
NO_OUTPUT=0

if [ ! -x "$CONVERT" ] || [ ! -x "$COMPOSITE" ] || [ ! -x "$DISPLAY_BIN" ]; then
    echo "Please ensure ImageMagick is installed"
    exit
fi
if [ ! "$OUTPUT_FILE" ]; then
    OUTPUT_FILE=$(mktemp)
    NO_OUTPUT=1
fi

$CONVERT $INPUT_FILE -resize $SIZE\> jpg:- | \
$CONVERT - -gravity Center -extent $SIZE -fill black jpg:- | \
$CONVERT -background '#00000005' -pointsize 12 -fill white label:"CC by $OWNER" \
    -bordercolor '#00000070' -border 6x6 - +swap -gravity SouthEast -geometry +5+5 -composite jpg:- | \
$COMPOSITE -gravity SouthWest -geometry +5+5 cc.png - "$OUTPUT_FILE"

if [ "$DISPLAY" = 1 ]; then
    echo $OUTPUT_FILE
    $DISPLAY_BIN $OUTPUT_FILE
fi

if [ "$NO_OUTPUT" = 1 ]; then
    rm $OUTPUT_FILE
fi
