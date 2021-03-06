#!/bin/bash -e

# 
# Goal: watermark CC notice to a list of photographs, as cataloged by a CSV file.
#
# Functionalities:
#      Given a CSV file with fields (in exactly this order):
#        input_file, author, license
#      backup and transform photograph indicated in each row by imageCCTager.sh script
#      Note: license corresponds to CC_TYPE argument in imageCCTagger script, please see its comment
#
# Requirement: ImageMagick, imageCCTagger.sh
#
# Usage: ./batchImageTagger.sh -i INPUT_FILE_NAME [-v] -d [INPUT_IMAGE_DIRECTORY] -o OUTPUT_IMAGE_DIRECTORY -f [FONTSIZE] -b [BACKGROUND_COLOR] \
#                           -s [SIZE] -p [MESSAGE_POSITION]
#    [required] INPUT_FILE_NAME: Name of input file (only .csv supported)
#    [optional] INPUT_IMAGE_DIRECTORY: directory of input images; if left empty, the script will
#               assume `input_file` field in the INPUT_FILE is in absolute path
#    [required] OUTPUT_IMAGE_DIRECTORY: directory of output images
#    [optional] FONTSIZE (default: 12): font size of cc message
#    [optional] BACKGROUND_COLOR (default: black): if image is enlarged, fill background with this color
#    [optional] SIZE: (default: 1800x1350) resize image to width W, height H
#    [optional] MESSAGE_POSITION: (default: CENTER) the position of CC message/icon in the image, either CENTER or CORNER
#    [optional] -v, VERBOSE: print verbose messages
#
# Example usage:
#   ./batchImageTagger.sh -i list.csv -d /home/foo/images
#

function print_help {
    echo " Usage: ./batchImageTagger.sh -i INPUT_FILE_NAME [-v] -d [INPUT_IMAGE_DIRECTORY] -o OUTPUT_IMAGE_DIRECTORY -f [FONTSIZE] -b [BACKGROUND_COLOR] \ "
    echo "                           -s [SIZE] -p [MESSAGE_POSITION]"
    echo "    [required] INPUT_FILE_NAME: Name of input file (only .csv supported)"
    echo "    [optional] INPUT_IMAGE_DIRECTORY: directory of input images; if left empty, the script will"
    echo "               assume `input_file` field in the INPUT_FILE is in absolute path"
    echo "    [required] OUTPUT_IMAGE_DIRECTORY: directory of output images"
    echo "    [optional] FONTSIZE (default: 12): font size of cc message"
    echo "    [optional] BACKGROUND_COLOR (default: black): if image is enlarged, fill background with this color"
    echo "    [optional] SIZE: (default: 1800x1350) resize image to width W, height H"
    echo "    [optional] MESSAGE_POSITION: (default: CENTER) the position of CC message/icon in the image, either CENTER or CORNER"
    echo "    [optional] -v, VERBOSE: print verbose messages"
    echo ""
    echo " Example usage:"
    echo "   ./batchImageTagger.sh -i list.csv -d /home/foo/images"
}
function die {
    echo "$1"
    exit 1
}
function argument_missing {
    print_help
    echo ""
    die "Missing required argument: $1"
}

while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    -i|--input_file)
    INPUT_FILE="$2"
    shift
    ;;
    -d|--directory)
    INPUT_DIR="$2"
    shift
    ;;
    -o|--output)
    OUTPUT_DIR="$2"
    shift
    ;;
    -h|--help)
    print_help
    exit 1
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
    -v)
    _info=echo
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

# Required arguments
[ "_$INPUT_FILE" = "_" ] && argument_missing "INPUT_FILE"
[ "_$OUTPUT_DIR" = "_" ] && argument_missing "OUTPUT_DIR"

# Optional arguments
[ "_$SIZE" = "_" ]                || SIZE="-s $SIZE"
[ "_$FONTSIZE" = "_" ]            || FONTSIZE="-f $FONTSIZE"
[ "_$FILL_COLOR" = "_" ]          || FILL_COLOR="-b $FILL_COLOR"
[ "_$MESSAGE_POSITION" = "_" ]    || MESSAGE_POSITION"=-p $MESSAGE_POSITION"
[ "_$IMAGE_TAGGER_SCRIPT" = "_" ] && IMAGE_TAGGER_SCRIPT="./imageCCTagger.sh"
[ "_$_info" = "_" ]               && _info=: # If not VERBOSE, ignore printing any string

[ -f "$INPUT_FILE"  ]  || die "${INPUT_FILE}: file not found"
[ -x "$IMAGE_TAGGER_SCRIPT" ] || die "imageTagger script \"$IMAGE_TAGGER_SCRIPT\" not found or is not executable"

if [ "_$INPUT_DIR" != "_" ]; then
    [ -d "$INPUT_DIR" ]  || \
        die "$INPUT_DIR: directory not found"
    ABS_PATH=0
fi

mkdir -p "$OUTPUT_DIR"

# Determine delimiter of csv, either tab or comma
IFS="	"
head "$INPUT_FILE" -n1 | grep "	" &> /dev/null || IFS=","
CNT=0

while read input_file author license
do
    # skip the first row
    if [ "$FLAG" ];
    then
        CC_NOTICE="CC($license) by $author"

        IN="$input_file"
        if [ "$ABS_PATH" = "0" ]; then
            IN="${INPUT_DIR}/${input_file}"
        fi

        OUT="${OUTPUT_DIR}/$(basename "$input_file")"

        if [ -f "$IN" ]; then
            CMD="bash $IMAGE_TAGGER_SCRIPT -i \"$IN\" -o \"$OUT\" \
                -c $license -m \"$CC_NOTICE\" \
                $FONTSIZE $BACKGROUND_COLOR $SIZE $MESSAGE_POSITION"
            $_info "Processing input file $IN"
            eval $CMD
            $_info "Result written to $OUT"
            CNT=$(($CNT + 1))
        else
            die "$IN: file not found"
        fi
    fi
    FLAG=1
done < "$INPUT_FILE"

$_info "Done, $CNT images converted"
