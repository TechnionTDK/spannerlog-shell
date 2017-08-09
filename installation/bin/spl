#!/usr/bin/env bash
set -eu

print_help() {
    echo
    echo "Available commands are:"
    echo "spl compile     #      Compiles Spannerlog source code into executables under target/"
    echo "spl run         #      Runs the current Spannerlog app end-to-end"
    echo "spl sql         #      Runs an SQL query against the database for the Spannerlog application"
}

# print help if no arguments were given
[ $# -gt 0 ] || {
    print_help
    exit
}

cmd=$1; shift

export SPL_HOME=$(dirname "$(dirname -- $0)")
export PATH="$SPL_HOME/bin:$SPLOG_HOME/shell:$PATH"

# Check if command is valid
exe=spl-"$cmd"
if type "$exe" &>/dev/null; then
    set -- "$exe" "$@"
else
    print-error "$cmd: invalid command"
    exit
fi

# Run given command under this environment
exec "$@"
