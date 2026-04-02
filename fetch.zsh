#!/usr/bin/env zsh

# colors
c0="%f"
c1="%F{blue}"
c2="%F{magenta}"
c3="%F{cyan}"

# info
os=$(grep "^NAME" /etc/os-release | cut -d= -f2 | tr -d '"')
kernel=$(uname -r)
wm="${XDG_CURRENT_DESKTOP:-${DESKTOP_SESSION:-niri}}"
terminal="${TERM:-kitty}"
uptime=$(uptime -p | sed 's/up //')
ram=$(free -m | awk '/Mem:/ {printf "%dMB / %dMB", $3, $2}')

# os age
os_install=$(date -r /etc/machine-id '+%s')
now=$(date '+%s')
diff=$(( now - os_install ))
years=$(( diff / 31536000 ))
days=$(( (diff % 31536000) / 86400 ))
hours=$(( (diff % 86400) / 3600 ))
os_age="${years}y ${days}d ${hours}h"

# cool wms
cool_wms=("bspwm" "niri" "river" "hyprland" "dwm" "awesome" "xmonad")
wm_lower="${wm:l}"
btw_wm=""
for w in $cool_wms; do
  [[ "$wm_lower" == *"$w"* ]] && btw_wm=" btw" && break
done

# info array
info=(
  "${c1}os      ${c0}${os} btw"
  "${c1}kernel  ${c0}${kernel}"
  "${c1}wm      ${c0}${wm}${btw_wm}"
  "${c1}term    ${c0}${terminal}${btw_wm}"
  "${c1}ram     ${c0}${ram}"
  "${c1}uptime  ${c0}${uptime}"
  "${c1}os age  ${c0}${os_age}"
)

# logo array
logo=(
  $'    /\\'
  $'   /  \\'
  $'  /    \\'
  $' /  /\\  \\'
  $'/__/  \\__\\'
  $'          '
  $'          '
)

# print side by side
print ""
for i in {1..7}; do
  printf '\033[34m%-14s\033[0m' "${logo[$i]}"
  print -P "   ${info[$i]}"
done
print ""

# color blocks
print -P "%F{blue}██%F{magenta}██%F{cyan}██%F{yellow}██%F{green}██%F{red}██%F{white}██${c0}"
print ""
