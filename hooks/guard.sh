#!/bin/sh
# my-tech-team guard (Claude Code PreToolUse hook for Bash).
# Asks the PM before risky commands. It never denies and fails open:
# if anything goes wrong it prints nothing, so normal permissions apply.
input=$(cat 2>/dev/null) || exit 0
# Read only the command: drop the description field, then make every line
# of the command its own command (JSON "\n" becomes ";", "\r" and "\t" spaces).
input=$(printf '%s' "$input" \
  | sed -E 's/"description":[[:space:]]*"([^"\\]|\\.)*"//' \
  | sed 's/\\n/;/g; s/\\[rt]/ /g') || exit 0

has() { printf '%s' "$input" | grep -Eq -- "$1"; }
hasi() { printf '%s' "$input" | grep -Eiq -- "$1"; }

W='(^|[^A-Za-z0-9_./-])'   # start of a command word
reason=""

# Recursive delete of an absolute, home or parent path. Temp paths are
# removed first, so they never excuse another target in the same command.
notmp=$input
if ! has "(/tmp|/var/folders)/[^[:space:]\"]*\\.\\."; then
  notmp=$(printf '%s' "$input" | sed -E 's#(\\")?(/private)?(/tmp|/var/folders)/[^[:space:]"\\]+##g') || notmp=$input
fi
if has "${W}rm[[:space:]]+(-[^[:space:]]+[[:space:]]+)*(-[A-Za-z]*[rR][A-Za-z]*|--recursive)" \
  && printf '%s' "$notmp" | grep -Eq -- "${W}rm[[:space:]][^|;&]*[[:space:]](\\\\\"|')?(/|~|\\\$\\{?HOME|\\.\\.(/|[[:space:]\\'\"]|\$))"; then
  reason="recursive delete outside the project"
elif has "${W}git[[:space:]]+reset[[:space:]][^|;&]*--hard"; then
  reason="git reset --hard discards uncommitted work"
elif has "${W}git[[:space:]]+clean[[:space:]]+-[A-Za-z]*f"; then
  reason="git clean deletes untracked files"
elif has "${W}git[[:space:]]+push[^|;&]*[[:space:]](-f|--force|--force-with-lease)([^A-Za-z-]|$)" \
  || has "${W}git[[:space:]]+push[^|;&]*[[:space:]]\\+[^[:space:]\"]"; then
  reason="force-push rewrites remote history"
elif has "${W}git[[:space:]]+push[^|;&]*[[:space:]](--delete|:[A-Za-z0-9])"; then
  reason="deletes a remote branch or tag"
elif has "${W}git[[:space:]]+(branch[[:space:]]+(-d|-D|--delete)|tag[[:space:]]+(-d|--delete))"; then
  reason="deletes a branch or tag"
elif has "${W}git[[:space:]]+config[[:space:]]+--global"; then
  reason="changes global git config"
elif has "${W}(pkill|killall)[[:space:]]" || has "${W}kill[[:space:]]+-(9|KILL)" || has "xargs[[:space:]]+kill"; then
  reason="kills processes that may not belong to this task"
elif has "simctl[[:space:]]+(erase|delete)" || has "(-wipe-data|emulator[^|;&]*-wipe)" \
  || has "${W}adb[[:space:]][^|;&]*(uninstall|pm[[:space:]]+clear)"; then
  reason="erases a simulator, emulator or app data"
elif hasi "(psql|mysql|mariadb|sqlite3|duckdb|sqlcmd|mongosh)[^|;&]*(drop|truncate)[[:space:]]+(database|schema|table)"; then
  reason="drops or truncates database data"
elif has "${W}sudo[[:space:]]"; then
  reason="runs a command as administrator (sudo)"
elif has "(curl|wget)[^|]*\\|[[:space:]]*(sudo[[:space:]]+)?(ba|z|da)?sh([^A-Za-z]|$)"; then
  reason="pipes a download into a shell"
elif has "${W}brew[[:space:]]+(install|uninstall|reinstall|upgrade|tap)" \
  || has "${W}(npm|pnpm|yarn)[[:space:]][^|;&]*(-g|--global|global[[:space:]]+add)([^A-Za-z-]|$)" \
  || has "playwright[[:space:]]+install" || has "get\\.maestro\\.mobile\\.dev" \
  || has "${W}flutter[[:space:]]+upgrade" || has "${W}sdkmanager[[:space:]]"; then
  reason="installs or upgrades software on this machine"
elif has ">>?[[:space:]]*(\\\\\")?(~|\\\$\\{?HOME\\}?)/\\.(zshrc|bashrc|bash_profile|profile|zprofile|claude/)" \
  || has "${W}defaults[[:space:]]+write" || has "${W}(chsh|launchctl)[[:space:]]"; then
  reason="changes shell, system or Claude Code settings"
elif has "${W}(mkfs|shutdown|reboot)([[:space:]]|$)" || has "diskutil[[:space:]]+(erase|partition)" || has "${W}dd[[:space:]]+if="; then
  reason="can damage disks or stop this machine"
elif has "${W}(chmod|chown)[[:space:]]+-R[[:space:]][^|;&]*[[:space:]](\\\\\"|')?(/|~|\\\$\\{?HOME)"; then
  reason="changes permissions recursively outside the project"
fi

[ -z "$reason" ] && exit 0
printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"my-tech-team guard: %s. Approve only if you expected this command."}}\n' "$reason"
exit 0
