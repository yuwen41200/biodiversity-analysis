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
# Usage: ./imageCCTagger.sh -i INPUT_FILE_NAME -c CC_TYPE -m CC_NOTICE -f [FONTSIZE] -b [BACKGROUND_COLOR] \
#                           -s [SIZE] -p [MESSAGE_POSITION] -o OUTPUT_FILE_NAME 
#    [required] INPUT_FILE_NAME: Name of input file
#    [required] CC_TYPE: required, Type of CC, can be: by, by-nc, by-nd, by-sa, by-nc-sa, by-nc-nd
#               icons from http://www.creativecommons.org.tw
#    [required] CC_NOTICE: a message to be attached, ex: "CC(3.0) by John Doe, 2016"
#    [optional] FONTSIZE (default: 12): font size of cc message
#    [optional] BACKGROUND_COLOR (default: black): if image is enlarged, fill background with this color
#    [optional] SIZE: (default: 1800x1350) resize image to width W, height H
#    [optional] MESSAGE_POSITION: (default: CENTER) the position of CC message/icon in the image, either CENTER or CORNER
#    [required] OUTPUT_FILE_NAME: if not provided, display the output directly
#
# Environment variables:
#
# Notice: MimeType of OUTPUT_FILE_NAME determines the resulting image format.
#         Thus, if OUTPUT_FILE_NAME=foo.jpg, output image will be in JPEG
#
# Example usage:
#   ./imageCCTagger.sh -i cat.jpg -f 12 -c by -m "CC by Tom" -o out.jpg
#

function print_help {
    echo " Usage: $0 -i INPUT_FILE_NAME -c CC_TYPE -m CC_NOTICE -f [FONTSIZE] -b [BACKGROUND_COLOR] "
    echo "                           -s [SIZE] -p [MESSAGE_POSITION] -o OUTPUT_FILE_NAME "
    echo "    [required] INPUT_FILE_NAME: Name of input file"
    echo "    [required] CC_TYPE: required, Type of CC, can be: by, by-nc, by-nd, by-sa, by-nc-sa, by-nc-nd"
    echo "               icons from http://www.creativecommons.org.tw"
    echo "    [required] CC_NOTICE: a message to be attached, ex: 'CC(3.0) by John Doe, 2016'"
    echo "    [optional] FONTSIZE (default: 12): font size of cc message"
    echo "    [optional] BACKGROUND_COLOR (default: black): if image is enlarged, fill background with this color"
    echo "    [optional] SIZE: (default: 1800x1350) resize image to width W, height H"
    echo "    [optional] MESSAGE_POSITION: (default: CENTER) the position of CC message/icon in the image, either CENTER or CORNER"
    echo "    [required] OUTPUT_FILE_NAME: if not provided, display the output directly"
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
    -m|--cc_notice)
    CC_NOTICE="$2"
    shift
    ;;
    -s|--size)
    SIZE="$2"
    shift
    ;;
    -p|--position)
    MESSAGE_POSITION="$2"
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

CC_ICON_DIR=$(dirname "$0")/icons
CC_ICON_FILE="$CC_ICON_DIR/cc-$CC_TYPE.png"

# Required arguments
[ "_$INPUT_FILE" = "_" ]  && argument_missing "INPUT_FILE"
[ "_$CC_TYPE" = "_" ]     && argument_missing "CC_TYPE"
[ "_$CC_NOTICE" = "_" ]   && argument_missing "CC_NOTICE"
[ "_$OUTPUT_FILE" = "_" ] && argument_missing "OUTPUT_FILE"

# Optional arguments
[ "_$SIZE" = "_" ]             && SIZE=1800x1350
[ "_$FONTSIZE" = "_" ]         && FONTSIZE="12"
[ "_$FILL_COLOR" = "_" ]       && FILL_COLOR=black
[ "_$MESSAGE_POSITION" = "_" ] && MESSAGE_POSITION=CORNER

# Verify output file mimetype
OUTPUT_FILE_MIMETYPE=$(echo "$OUTPUT_FILE" | sed 's/^.*\.//' | tr '[:upper:]' '[:lower:]')
IMAGE_MIMETYPE="jpg jpeg gif tif png gif"
for m in $IMAGE_MIMETYPE;
do
    if [ "x$m" = "x$OUTPUT_FILE_MIMETYPE" ];
    then
        OK=1
        break
    fi
done

[ "$OK" ] || die "Invalid output file mimetype, please specify a valid image mimetype"
[ -f $CC_ICON_FILE ] || die "Invalid CC type: $CC_TYPE"

iconw=$(identify -format %w ${CC_ICON_FILE})
iconh=$((6+${FONTSIZE}))

if [ "$MESSAGE_POSITION" = "CENTER" ]; then

TMP=$(mktemp --suffix=.png)
convert ${CC_ICON_FILE} -resize "${iconw}x${iconh}"\> jpg:- | \
convert - -background '#00000001' -pointsize ${FONTSIZE} -fill white label:"$CC_NOTICE" \
    -bordercolor '#00000070' -border 6x6 -gravity Center -geometry +5+5 +append $TMP
convert ${INPUT_FILE} -resize ${SIZE}\> jpg:- | \
convert - -gravity Center  -background ${FILL_COLOR} -extent ${SIZE} jpg:- | \
composite -gravity South -geometry +5+5 $TMP - "$OUTPUT_FILE"
rm $TMP

elif [ "$MESSAGE_POSITION" = "CORNER" ]; then

TMP=$(mktemp --suffix=.jpg)
convert ${CC_ICON_FILE} -resize "${iconw}x${iconh}"\> $TMP
convert ${INPUT_FILE} -resize ${SIZE}\> jpg:- | \
convert - -gravity Center  -background ${FILL_COLOR} -extent ${SIZE} jpg:- | \
convert -background '#00000005' -pointsize ${FONTSIZE} -fill white label:"$CC_NOTICE" \
    -bordercolor '#00000070' -border 6x6 - +swap -gravity SouthEast -geometry +5+5 -composite jpg:- | \
composite -gravity SouthWest -geometry +5+5 ${TMP} - "$OUTPUT_FILE"
rm $TMP

else

die "Unknown position: $MESSAGE_POSITION"

fi
