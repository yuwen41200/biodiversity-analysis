#! /usr/bin/env bash 

# The source csv file to be parsed
SOURCE_CSV=sample.csv

# The directory to put the generated images
TARGET_DIR=by

# Type of font, use `convert -list font` to get all available fonts
#FONT_TYPE="TakaoPGothic"
FONT_TYPE="Droid-Sans-Fallback"

# Default type of copyright
CC_DEFAULT=by

# Field number of ID in csv
ID_FIELD=1

# Field number of author in csv
AUTHOR_FIELD=13

# Field number of copyright in csv
CC_FIELD=16

# Script to tag the image
TAGGER_SCRIPT="../image-tagger/imageCCTagger.sh"

function die {
    echo "$1"
    exit 1
}


FONT_PATH=`convert -list font  | grep -A5 "$FONT_TYPE" | head -6 | tail -1 | cut -f2 -d':'`
[ -f $SOURCE_CSV ]    || die "Source CSV not found: $SOURCE_CSV"
[ -f $TAGGER_SCRIPT ] || die "Tagger script not found: $TAGGER_SCRIPT"
[ -f $FONT_PATH ]     || die "Font not found: $FONT_TYPE"
mkdir -p "$TARGET_DIR"

cat "$SOURCE_CSV" | sed 1d | while read line;
do 
    ID=$(echo $line | cut -f$ID_FIELD -d',')
    echo "Processing $ID ..."

    # Extracting author
    AUTHOR=$(echo $line | cut -f$AUTHOR_FIELD -d',')
    [ "_" = "_$AUTHOR" ] && AUTHOR=Unknown

    # Extracting CC info
    CC=$(echo $line | cut -f$CC_FIELD -d',')
    FOUND=0
    for t in `"$TAGGER_SCRIPT" -h | sed 1d | grep CC_TYPE | cut -d':' -f3  | sed 's/ *//g' | tr ',' '\n'`;
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

    # Retrieving image from roadkill.tw
    OUT="imgs/$ID.jpg"
    IMG=`curl -s "https://roadkill.tw/occurrence/$ID" | \
    python -c 'import sys, re;print(re.findall(r"<.*img.*img-responsive.*src=\"(.*)\"",sys.stdin.read())[0])' 2>/dev/null \
    | cut -f1 -d'"'`; 

    if [ "_" = "_$IMG" ]; then
        echo "Image not available for id $ID";
    else
        if [ ! -f "$OUT" ]; then
            wget $IMG -qO "$OUT" &> /dev/null || echo "Cannot download $ID.jpg";
            "$TAGGER_SCRIPT" -i "$OUT" -s 800x600 -c $CC -m "by $AUTHOR" -fp "$FONT_PATH" -o "$OUT"
        fi
    fi
done
