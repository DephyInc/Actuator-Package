SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"

PLAN_STACK_DIR="${SCRIPT_DIR}/fx_plan_stack"
ACPAC_DIR="${SCRIPT_DIR}/C"

# guest host OS
if [[ $1 = "-pi" ]]; then
    HOST_OS="raspberryPi"
elif [[ "$OSTYPE" == "linux-gnu" ]]; then
    HOST_OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    HOST_OS="mac"
elif [[ "$OSTYPE" == "cygwin" ]]; then
    HOST_OS="windows"
elif [[ "$OSTYPE" == "msys" ]]; then
    HOST_OS="windows"
else
    HOST_OS="linux"
fi

function build_from_scratch
{
    echo fresh build on $1
    cd $1
    rm -rf build
    mkdir -p build
    cd build
    if [[ "$HOST_OS" == "linux" ]]; then
        cmake -G Ninja -D CMAKE_C_COMPILER=gcc-7 -D CMAKE_CXX_COMPILER=g++-7 ..
    else
        cmake .. -G Ninja
    fi

    ninja
    cd ${SCRIPT_DIR}
}

function acpac
{
    cd ${ACPAC_DIR}
    ./cscripts_builder.sh
    cd ${SCRIPT_DIR}
    #echo '/dev/ttyACM0' > ${ACPAC_DIR}/build/com.txt
}

function cscripts_proto
{
    cd ${ACPAC_DIR}
    ./cscripts_builder.sh proto
    cd ${SCRIPT_DIR}
    #echo '/dev/ttyACM0' > ${ACPAC_DIR}/build/com.txt
}

function plan_stack
{
    cd ${PLAN_STACK_DIR}
    ./stack_builder.sh
    cd ${SCRIPT_DIR}
}

function stack_proto
{
    cd ${PLAN_STACK_DIR}
    ./stack_builder.sh proto
    cd ${SCRIPT_DIR}
}

#
# Argument Processing
#

# This script always requires a build target.
if [ $# -eq 0 ]; then
    cat<<EOF
Build plan software.
Usage: $(basename $0) [options] [target-board] ...
Options:

Targets:
    acpac
    plan_stack
    all
Examples:
    ./build.sh acpac
    ./build.sh all
EOF
    exit 0
fi

# Process command line arguments.
for ARGUMENT in "$@"; do

    case "$ARGUMENT" in
        acpac)
            acpac
            ;;
        plan_stack)
            plan_stack
            ;;
        proto)
            stack_proto
            cscripts_proto
            ;;
        doit)
            cd ${ACPAC_DIR}/build
            ./protobuf
            cd ${SCRIPT_DIR}
            ;;
        run)
            cd ${ACPAC_DIR}/build
            ./main
            cd ${SCRIPT_DIR}
            ;;
        all)
            plan_stack
            acpac
            ;;
    esac

done

exit 0
