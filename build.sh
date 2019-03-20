SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
FLEX_LIB_DIR="${SCRIPT_DIR}/fx_plan_stack/FlexSEA-Stack-SharedLib"
ACT_PACK_DIR="${SCRIPT_DIR}"
PLAN_STACK_DIR="${SCRIPT_DIR}/fx_plan_stack"
ACPAC_DIR="${SCRIPT_DIR}/acpac_cscripts"
SERIAL_DIR="${SCRIPT_DIR}/fx_plan_stack/serial"

function build_from_scratch
{
    echo fresh build on $1
    cd $1
    rm -rf build
    mkdir -p build
    cd build
    cmake .. -G "Eclipse CDT4 - Ninja"
    ninja
    cd ${SCRIPT_DIR}
}

function build
{
    echo basic build on $1
    cd $1/build
    make
    cd ${SCRIPT_DIR}
}

function clean
{
    echo cleaning $1
    cd $1/build
    make clean
    cd ${SCRIPT_DIR}
}

function build_all
{
    build_from_scratch ${PLAN_STACK_DIR}
    build_from_scratch ${ACPAC_DIR}
    echo '/dev/ttyACM0' > ${ACPAC_DIR}/build/com.txt
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
            build_from_scratch ${ACPAC_DIR}
            echo '/dev/ttyACM0' > ${ACPAC_DIR}/build/com.txt
            ;;
        plan_stack)
            cd ${PLAN_STACK_DIR}
            ./stack_builder.sh
            ;;
        serial)
            build_from_scratch ${SERIAL_DIR}
            cp ${SERIAL_DIR}/build/libserialc.a ${PLAN_STACK_DIR}/libs
            ;;
        all)
            cd ${PLAN_STACK_DIR}
            ./stack_builder.sh
            build_from_scratch ${ACPAC_DIR}
            echo '/dev/ttyACM0' > ${ACPAC_DIR}/build/com.txt
            ;;
    esac

done

exit 0
