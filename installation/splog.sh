#!/bin/bash

function print_help {
    echo
    echo "Available commands are:"
    echo "splog compile     #      Compiles Spannerlog source code into executables under run/"
    echo "splog run         #      Runs the current Spannerlog app end-to-end"
    echo "splog sql         #      Runs a SQL query against the database for the Spannerlog application"
}

function print_error {
    tput setaf 1
    echo "$1" >&2
    tput sgr0
}

if [ $# -eq 0 ]; then
    print_help
    exit
fi

key="$1"

case $key in
    compile)
    COMPILE=true
    ;;
    run)
    RUN=true
    ;;
    sql)
	SQL="$2"
	;;
    *)
    print_error "$1: invalid command"
    print_help
    exit
    ;;
esac


EXEC="java -jar ~/Workspace/Projects/spannerlog-shell/installation/spannerlog-1.0-SNAPSHOT.jar"
APP="app.splog"

if [ -n "$COMPILE" ]; then
    if [ ! -f "$APP" ]; then
        print_error "Not inside a Spannerlog application: $APP and db.url should be all present in a parent directory"
        exit
    fi
    rm -rf run
    if eval "${EXEC} -compile app.splog" > app.ddlog; then
	   eval "deepdive compile"
    fi
fi

if [ -n "$RUN" ]; then
	eval "deepdive do all"
fi

if [ -n "$SQL" ]; then
	eval "deepdive sql \"${SQL}\""
fi
