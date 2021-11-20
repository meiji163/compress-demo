#!/usr/bin/env bash

# script to view the leaderboard

get_submissions(){
    gh api -X GET /organizations/65834464/team/5124884/discussions/55/comments \
        --paginate --template '
        {{- range . -}}
            {{- printf "%s\t%s\n" .author.login .body -}}
        {{- end -}}'
}

regex="([0-9]+) bytes"

fmt_submissions(){
    local bytes user body 
    get_submissions | while IFS=$'\t' read -r user body; do
        if [[ $body =~ $regex ]]
        then
            printf "%s\t%s\n" "$user" "${BASH_REMATCH[1]}"
        fi
    done | column -t -s$'\t'
}

leaderboard(){
    printf "========LEADERBOARD========\n"
    fmt_submissions | sort -k2 -n 
    printf "\n\nUpdated at: %s\n" "$(date)"
}

leaderboard
