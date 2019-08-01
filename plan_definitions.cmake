# declare this as ActPack so that we don't try pulling in flexsea-dephy submodule
set(PLAN_TYPE "PLAN_ACTPACK")

add_definitions(
	-DBOARD_TYPE_FLEXSEA_PLAN
	-DBUILD_SHARED_LIB_DLL
	-DNOT_TEST_PC
	-DINCLUDE_UPROJ_ACTPACK
)