#!/bin/sh

# exit program if any command fails
set -e

FZF_OPTIONS='--reverse --margin 3% --cycle --header-first'

mkdir -p outlines

# URL endpoint return JSON array of object like:
# {
#     "text": "...",
#     "value": "..."
# }
# where .text is the uppercase version of .value

URL='http://www.sfu.ca/bin/wcm/course-outlines?'
YEAR=$(
curl -s "$URL" \
    | jq '.[].text' \
    | cut -d '"' -f2 \
    | fzf $FZF_OPTIONS \
          --header="Select year:" --tac 
)

URL="$URL$YEAR/"

TERM=$(
curl -s "$URL" \
    | jq '.[].text' \
    | cut -d '"' -f2 \
    | fzf $FZF_OPTIONS \
          --header="Select term:" --no-sort 
)

# convert term to lowercase, unnecessary since url is case-insensitive
# TERM=$(echo $TERM | tr "[:upper:]"  "[:lower:]")

URL="$URL$TERM/"
DEPT=$(
curl -s "$URL" \
    | jq '.[] | .text + " - " + .name' \
    | cut -d '"' -f2 \
    | fzf $FZF_OPTIONS \
          --header="Select department:" \
    | awk '{print $1}'
)

URL="$URL$DEPT/"
NUMBER=$(
curl -s "$URL" \
    | jq '.[] | .text + " - " + .title' \
    | cut -d '"' -f2 \
    | fzf $FZF_OPTIONS \
          --header="Select course number:" \
    | awk '{print $1}'
)

URL="$URL$NUMBER/"

# curl -s "$URL" \
#     | jq 
# exit
SECTION=$(
curl -s "$URL" \
    | jq '.[] | .sectionCode + " - " + .text' \
    | cut -d '"' -f2 \
    | fzf $FZF_OPTIONS \
          --header="Select course section:" \
    | awk '{print $3}'
)

URL="$URL$SECTION/"
FILENAME="outlines/${DEPT}_${NUMBER}_${SECTION}_${TERM}_${YEAR}.json"
curl -s "$URL" | jq > $FILENAME
python3 display.py $FILENAME
