#!/usr/bin/env bash

help() {
    cat <<EOF
Usage: $0 [-p]

Display leaderboard from GitHub discussion 

Flags:
    -p      post to discord channel (set WEBHOOK_URL environment variable)
EOF
}

regex="([0-9]+) bytes"

p_flag=false
while getopts 'p' flag; do
    case "${flag}" in
        p) p_flag=true 
            ;;
        *) help
            exit 1 ;;
    esac
done

get_submissions(){
    gh api -X GET /organizations/65834464/team/5124884/discussions/55/comments \
        --paginate --cache=4m \
        --template '
        {{- range . -}}
            {{- printf "%s\t%s\n" .author.login .body -}}
        {{- end -}}'
}

fmt_submissions(){
    local bytes user body 
    get_submissions | while IFS=$'\t' read -r user body; do
        if [[ $body =~ $regex ]]; then
            printf "%s\t%s\n" "$user" "${BASH_REMATCH[1]}"
        fi
    done | sort -k2 -n | column -t -s$'\t'
}


leaderboard(){
    printf '=========[LEADERBOARD]=========

%s

Updated at: %s
https://github.com/orgs/MLH-Fellowship/teams/pod-4-2-0/discussions/55
' "$(fmt_submissions)" "$(date)"

}

to_discord(){
    local url
    url="$WEBHOOK_URL"
    if [[ -z "$url" ]]; then
        echo "Error: WEBHOOK_URL not set"
        return 1
    fi

    curl -s -X POST "$url" -d content="$1"
}

if [ "$p_flag" = true ]; then
    msg="$(leaderboard)"
    msg="\`\`\`css
${msg}
\`\`\`"
    to_discord "$msg"
else
    leaderboard
fi
