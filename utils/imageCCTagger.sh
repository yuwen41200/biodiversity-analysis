#!/bin/bash -e

# 
# Goal: watermark CC notice to a photograph.
#
# Functionalities:
#   1. Resize the image to a fixed size (default to w = 1800, h = 1350)
#        If input image is larger, resize to a fitting size without distortion
#        If input image is smaller, only extend it to given size by white background
#   2. Overlay a given CC icon to bottom-left
#   3. Overlay a CC notice to bottom-right
#
# Requirement: ImageMagick 
#
# Usage: ./imageCCTagger.sh -i [INPUT_FILE_NAME] -c [CC_TYPE] -f [FONTSIZE] -n [CC_NOTICE] -b [BACKGROUND_COLOR] -o [OUTPUT_FILE_NAME]
#    [required] INPUT_FILE_NAME: Name of input file
#    [required] CC_TYPE: required, Type of CC, can be: by, by-nc, by-nd, by-sa, by-nc-sa, by-nc-nd
#               icons from http://www.creativecommons.org.tw
#    [required] CC_NOTICE: a message to be attached, ex: "CC(3.0) by John Doe, 2016"
#    [optional] FONTSIZE: font size of cc message
#    [optional] BACKGROUND_COLOR: if image is enlarged, fill background with this color
#    [optional] OUTPUT_FILE_NAME: if not provided, display the output directly
#
# Environment variables:
#   DISPLAY=1: display the result image
#   SIZE=WxH: resize image to width W, height H
#
# Notice: MimeType of OUTPUT_FILE_NAME determines the resulting image format.
#         Thus, if OUTPUT_FILE_NAME=foo.jpg, output image will be in JPEG
#
# Example usage:
#   SIZE=1200x1600 ./imageCCTagger.sh -i cat.jpg -f 12 -c by -n "CC by Tom" -b black -o out.jpg
#
function print_help {
    echo "Usage: $0 -i INPUT_FILE_NAME -c CC_TYPE -n CC_NOTICE -b [BACKGROUND_COLOR] -o [OUTPUT_FILE_NAME]"
}

function die {
    echo "$1"
    exit 1
}
function argument_missing {
    print_help
    die "Missing required argument: $1"
}

while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    -i|--inputfile)
    INPUT_FILE="$2"
    shift
    ;;
    -o|--outputfile)
    OUTPUT_FILE="$2"
    shift
    ;;
    -b|--backgroundcolor)
    FILL_COLOR="$2"
    shift
    ;;
    -f|--fontsize)
    FONTSIZE="$2"
    shift
    ;;
    -c|--cc_type)
    CC_TYPE="$2"
    shift
    ;;
    -n|--cc_notice)
    CC_NOTICE="$2"
    shift
    ;;
    -h|--help)
    print_help
    exit 1
    CC_NOTICE="$2"
    shift
    ;;
    *)
    # unknown option
    echo "Invalid option specified: $key"
    print_help
    exit 1
    ;;
esac
shift
done

CC_ICON_DIR=icons
CC_ICON_FILE="$CC_ICON_DIR/cc-$CC_TYPE.png"

# Required arguments
[ "_$INPUT_FILE" = "_" ]  && argument_missing "INPUT_FILE"
[ "_$CC_TYPE" = "_" ]     && argument_missing "CC_TYPE"
[ "_$CC_NOTICE" = "_" ]   && argument_missing "CC_NOTICE"

# Optional arguments
[ "_$SIZE" = "_" ]        && SIZE=1800x1350
[ "_$FONTSIZE" = "_" ]    && FONTSIZE="12"
[ "_$FILL_COLOR" = "_" ]  && FILL_COLOR=black
[ "_$OUTPUT_FILE" = "_" ] && NO_OUTPUT=1 && OUTPUT_FILE=$(mktemp)

# Verify output file mimetype
OUTPUT_FILE_MIMETYPE=$(echo "$OUTPUT_FILE" | cut -f2 -d'.')
IMAGE_MIMETYPE="jpg jpeg gif tif png gif"
for m in $IMAGE_MIMETYPE;
do
    if [ "x$m" = "x$IMAGE_MIMETYPE" ];
    then
        OK=1
    fi
done

[ "$OK" ] || die "Invalid output file mimetype, please specify a valid image mimetype"
[ -f $CC_ICON_FILE ] || die "Invalid CC type: $CC_TYPE"

convert ${INPUT_FILE} -resize ${SIZE}\> jpg:- | \
convert - -gravity Center  -background ${FILL_COLOR} -extent ${SIZE} jpg:- | \
convert -background '#00000005' -pointsize ${FONTSIZE} -fill white label:"$CC_NOTICE" \
    -bordercolor '#00000070' -border 6x6 - +swap -gravity SouthEast -geometry +5+5 -composite jpg:- | \
composite -gravity SouthWest -geometry +5+5 ${CC_ICON_FILE} - "$OUTPUT_FILE"

if [ "$DISPLAY" = 1 ] || [ "$NO_OUTPUT" = 1 ]; then
    display $OUTPUT_FILE
    if [ "$NO_OUTPUT" = 1 ]; then
        rm $OUTPUT_FILE
    else
        echo $OUTPUT_FILE
    fi
fi
