#!/usr/bin/env bash

# Type of font, use `convert -list font` to get all available fonts
#FONT_TYPE="TakaoPGothic"
#FONT_TYPE="Droid-Sans-Fallback"
FONT_PATH="$(dirname $0)/fonts/NotoSansCJKtc-DemiLight.otf"

# Size of output image
SIZE=950x600

# Default type of copyright
CC_DEFAULT=by

# Field number of ID in csv
ID_FIELD=1

# Field number of author in csv
AUTHOR_FIELD=13

# Field number of copyright in csv
CC_FIELD=16

IMAGE_NOT_AVAILABLE="本紀錄屬敏感受威脅物種，不對外開放！"

# Script to tag the image
TAGGER_SCRIPT="$(dirname $0)/../image-tagger/imageCCTagger.sh"

while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    -i|--input_file)
    SOURCE_CSV="$2"
    shift
    ;;
    -d|--directory)
    TARGET_DIR="$2"
    shift
    ;;
    -fp|--fontpath)
    FONT_PATH="$2"
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

function die {
    echo "$1"
    exit 1
}

function argument_missing {
    die "Missing required argument: $1"
}

# Required arguments
[ "_$SOURCE_CSV" = "_" ] && argument_missing "INPUT_FILE"
[ "_$TARGET_DIR" = "_" ] && argument_missing "TARGET_DIR"

# Optional arguments
[ "_$FONT_PATH" = "_" ] && \
    FONT_PATH=`convert -list font  | grep -A5 "$FONT_TYPE" | head -6 | tail -1 | cut -f2 -d':'`

[ -f $SOURCE_CSV ]    || die "Source CSV not found: $SOURCE_CSV"
[ -f $TAGGER_SCRIPT ] || die "Tagger script not found: $TAGGER_SCRIPT"
[ -f $FONT_PATH ]     || die "Font not found: $FONT_TYPE"
mkdir -p "$TARGET_DIR"

PY_SCRIPT=$(mktemp)
cat > $PY_SCRIPT << EOF
import sys,re
pattern=r'<a.*href=(.*)>\s*<.*img.*img-responsive.*src=\".*\"'
print(re.findall(pattern,sys.stdin.read())[0])
EOF

CC_TYPES=`"$TAGGER_SCRIPT" -h | sed 1d | grep CC_TYPE | cut -d':' -f3  | sed 's/ *//g' | tr ',' '\n'`

cat "$SOURCE_CSV" | sed 1d | while read line;
do 
    ID=$(echo $line | cut -f$ID_FIELD -d',')

    # Retrieving image from roadkill.tw
    OUT="$TARGET_DIR/$ID.jpg"


    if [ ! -f "$OUT" ]; then
        echo "Processing $ID ..."
        IMG=`curl -s "https://roadkill.tw/occurrence/$ID" | python "$PY_SCRIPT" 2> /dev/null | sed "s/[\'\"]//g"`

        if [ "_" = "_$IMG" ]; then
            echo "Image not available for id $ID, using a placeholder image";
            convert -pointsize 28 -size $SIZE  -gravity Center \
                -font $FONT_PATH caption:"$IMAGE_NOT_AVAILABLE" "$OUT"
        else
            # Extracting author
            AUTHOR=$(echo $line | cut -f$AUTHOR_FIELD -d',')
            [ "_" = "_$AUTHOR" ] && AUTHOR=Unknown

            # Extracting CC info
            CC=$(echo $line | cut -f$CC_FIELD -d',' | sed 's/cc-//g')
            FOUND=0
            for t in $(echo -n "$CC_TYPES");
            do
                if [ "_$t" = "_$CC" ];
                then
                    FOUND=1
                    break
                fi
            done
            if [ "$FOUND" = "0" ]; then
                CC=$CC_DEFAULT
            fi

            wget $IMG -qO "$OUT" &> /dev/null || echo "Cannot download $ID.jpg";
            "$TAGGER_SCRIPT" -i "$OUT" -s $SIZE -c $CC -m "by $AUTHOR" -fp "$FONT_PATH" -o "$OUT"
        fi
    else
        echo "Found $OUT, not generating it again ..."
    fi
done
rm $PY_SCRIPT
