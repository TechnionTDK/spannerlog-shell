#!/bin/bash

function print_help {
    echo
    echo "Available commands are:"
    echo "splog compile     #      Compiles Spannerlog source code into executables under target/"
    echo "splog run         #      Runs the current Spannerlog app end-to-end"
    echo "splog sql         #      Runs an SQL query against the database for the Spannerlog application"
}

function print_error {
    tput setaf 1
    echo "$1" >&2
    tput sgr0
}

# print help if no arguments were given
if [ $# -eq 0 ]; then
    print_help
    exit
fi

# parse arguments
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
DB="db.url"
INPUT_DIR="input"
UDF_DIR="udf"

# compile
if [ -n "$COMPILE" ]; then
    if [ ! -f "$APP" ] || [ ! -f "$DB" ]; then
        print_error "Not inside a Spannerlog application: $APP and db.url should be all present in a parent directory"
        exit
    fi

    # delete old target directory and create a new one
    rm -rf target
    mkdir target

    # create soft links
    if [ -d "$INPUT_DIR" ]; then
        ln -s "../$INPUT_DIR" "target/$INPUT_DIR"
    fi
    if [ -d "$UDF_DIR" ]; then
        ln -s "../$UDF_DIR" "target/$UDF_DIR"
    fi
    ln -s "../$DB" "target/$DB"

    # compile spannerlog program
    if eval "${EXEC} -compile app.splog" > target/app.ddlog; then
	   eval "cd target; deepdive compile; cd .."
    fi
fi

# run
if [ -n "$RUN" ]; then
	eval "cd target; deepdive do all; cd .."
fi

# execute an SQL query
if [ -n "$SQL" ]; then
	eval "cd target; deepdive sql \"${SQL}\"; cd .."
fi
