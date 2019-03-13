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
    cmake ..
    make
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
    # build_from_scratch ${FLEX_LIB_DIR}
    # cp ${FLEX_LIB_DIR}/build/unix_64/libFlexSEA-Stack-Plan.a ${PLAN_STACK_DIR}/unix64
    build_from_scratch ${PLAN_STACK_DIR}
    build_from_scratch ${ACPAC_DIR}
    echo '/dev/ttyACM0' > ${ACPAC_DIR}/build/com.txt
}

function clean_all
{
    clean ${FLEX_LIB_DIR}
    clean ${PLAN_STACK_DIR}
    clean ${ACPAC_DIR}
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
    flexsea_lib
    all
    lib_check
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
            clean ${PLAN_STACK_DIR}
            build ${PLAN_STACK_DIR}
            ;;
        flexsea_lib)
            clean ${FLEX_LIB_DIR}
            build ${FLEX_LIB_DIR}
            cp ${FLEX_LIB_DIR}/build/unix_64/libFlexSEA-Stack-Plan.a ${PLAN_STACK_DIR}/unix64
            ;;
        serial)
            build_from_scratch ${SERIAL_DIR}
            cp ${SERIAL_DIR}/build/libserialc.a ${PLAN_STACK_DIR}/unix64
            ;;
        lib_check)
            sha1sum FlexSEA-Stack-SharedLib/build/unix_64/libFlexSEA-Stack-Plan.a
            sha1sum Actuator-Package/fx_plan_stack/unix64/libFlexSEA-Stack-Plan.a
            ;;
        clean)
            clean_all
            ;;
        all)
            build_all
            ;;
    esac

done

exit 0
