#!/bin/bash
set -o errexit -o nounset -o pipefail
function -h {
cat <<USAGE
 USAGE: tsv.bash

  Calculates population density for major cities of Brazil.

USAGE
}; function --help { -h ;}                 # A nice way to handle -h and --help
export LC_ALL=en_US.UTF-8                    # A locale that works consistently

function main {
  while read_tsv state city population area
  do
    unset location density
    local location="$city ($state)"
    if [[ ${population+isset} && ${area+isset} ]]
    then local density="$(bc <<<"scale=4 ; $population/$area")"
    fi
    write_tsv_variables location density
  done
}

function read_tsv {
  local __tsv_trailing_stuff__  # Shadowing, to protect other vars of this name
  IFS=$'\t' read -r "$@" __tsv_trailing_stuff__ && reassign_tsv_variables "$@"
}

# Interprets escape sequences in variable values and re-assigns them. Unsets
# variables that consist of `\N`.
function reassign_tsv_variables {
  for var in "$@"
  do
    local rest="${!var}" head="${!var%%\\*}" result=""
    unset "$var"
    [[ $rest != '\N' ]] || continue                      # Let nulls stay unset
    while [[ $rest != $head ]]
    do
      result+="$head"
      rest="${rest#*\\}"
      case "$rest" in
        n*)  result+=$'\n' ; rest="${rest:1}" ;;
        r*)  result+=$'\r' ; rest="${rest:1}" ;;
        t*)  result+=$'\t' ; rest="${rest:1}" ;;
        \\*) result+=$'\\' ; rest="${rest:1}" ;;
        '')  err "Trailing backslash in $var=${!var}"
      esac
      head="${rest%%\\*}"     # NB: Always skip backslash, so \<char> -> <char>
    done
    result+="$rest"
    eval "$var"'="$result"' # NB: We *reference* and do not *substitute* result
  done
}

function write_tsv_variables {
  local __tsv_internal_accum__              # Hope this doesn't shadow anything
  [[ $# -gt 0 ]] || return 0
  while true
  do
    if [[ ${!1+isset} ]]
    then
      __tsv_internal_accum__="${!1}"
      __tsv_internal_accum__="${__tsv_internal_accum__//'\'/\\\\}"
      __tsv_internal_accum__="${__tsv_internal_accum__//$'\t'/\t}"
      __tsv_internal_accum__="${__tsv_internal_accum__//$'\n'/\n}"
      __tsv_internal_accum__="${__tsv_internal_accum__//$'\r'/\r}"
    else
      __tsv_internal_accum__='\N'
    fi
    printf '%s' "$__tsv_internal_accum__"
    shift
    [[ $# -gt 0 ]] || break
    printf $'\t'
  done
  printf $'\n'
}

function write_tsv {
  local esc
  [[ $# -gt 0 ]] || return 0
  while true
  do
    esc="$1"
    esc="${esc//'\'/\\\\}"
    esc="${esc//$'\t'/\t}"
    esc="${esc//$'\n'/\n}"
    esc="${esc//$'\r'/\r}"
    printf '%s' "$esc"
    shift
    [[ $# -gt 0 ]] || break
    printf $'\t'
  done
  printf $'\n'
}

function msg { out "$*" >&2 ;}
function err { local x=$? ; msg "$*" ; return $(( $x == 0 ? 1 : $x )) ;}
function out { printf '%s\n' "$*" ;}

if [[ ${1:-} ]] && declare -F | cut -d' ' -f3 | fgrep -qx -- "${1:-}"
then "$@"
else main "$@"
fi
