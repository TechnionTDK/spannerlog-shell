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

TARGET_DIR="target"
TARGET="app.ddlog"
UDF_TARGET_DIR="${TARGET_DIR}/udf"

# compile
if [ -n "${COMPILE}" ]; then
    if [ ! -f "${APP}" ] || [ ! -f "${DB}" ]; then
        print_error "Not inside a Spannerlog application: ${APP} and ${DB} should be all present in a parent directory"
        exit
    fi

    # delete old target directory and create a new one
    rm -rf ${TARGET_DIR}
    mkdir ${TARGET_DIR}
    mkdir ${UDF_TARGET_DIR}

    # create soft links
    if [ -d "${INPUT_DIR}" ]; then
        ln -s "../${INPUT_DIR}" "${TARGET_DIR}/${INPUT_DIR}"
    fi
    ln -s "../${DB}" "${TARGET_DIR}/${DB}"

    # compile spannerlog program
    if eval "${EXEC} -compile ${APP} ${UDF_DIR} ${UDF_TARGET_DIR}" > ${TARGET_DIR}/${TARGET}; then
       # eval "cd target; deepdive compile; cd .."
       echo pass
    fi
fi

# run
if [ -n "${RUN}" ]; then
    eval "cd ${TARGET_DIR}; deepdive do all; cd .."
fi

# execute an SQL query
if [ -n "${SQL}" ]; then
    eval "cd ${TARGET_DIR}; deepdive sql \"${SQL}\"; cd .."
fi
