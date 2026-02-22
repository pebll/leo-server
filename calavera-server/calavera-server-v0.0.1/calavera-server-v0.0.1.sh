#!/bin/sh
printf '\033c\033]0;%s\a' Calavera-Server
base_path="$(dirname "$(realpath "$0")")"
"$base_path/calavera-server-v0.0.1.x86_64" "$@"
