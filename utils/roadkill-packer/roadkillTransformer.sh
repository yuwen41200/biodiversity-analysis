#! /usr/bin/env bash 

# Try to use the trick here to encode Chinese text:
# http://www.imagemagick.org/Usage/text/
# but it did not work

ID_FIELD=1
AUTHOR_FIELD=13
CC_FIELD=16
CC_DEFAULT=by
TAGGER="../image-tagger/imageCCTagger.sh"

cat sample.csv | sed 1d | while read line;
do 
    ID=$(echo $line | cut -f$ID_FIELD -d',')
    echo "Processing $ID ..."

    # Extracting author
    AUTHOR=$(echo $line | cut -f$AUTHOR_FIELD -d',')
    [ "_" = "_$AUTHOR" ] && AUTHOR=Unknown

    # Extracting CC info
    CC=$(echo $line | cut -f$CC_FIELD -d',')
    FOUND=0
    for t in `"$TAGGER" -h | sed 1d | grep CC_TYPE | cut -d':' -f3  | sed 's/ *//g' | tr ',' '\n'`;
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
        [ -f "$OUT" ] || wget $IMG -qO "$OUT" &> /dev/null || echo "Cannot download $ID.jpg";
        "$TAGGER" -i "$OUT" -s 800x600 -c $CC -m "by $AUTHOR" -o "$OUT"
    fi
done
