SIM ?= verilator
TOPLEVEL_LANG = verilog

TOPLEVEL = tb_croc_soc
COCOTB_TEST_MODULES = test_croc_soc

COMPILE_ARGS += -Wno-fatal
COMPILE_ARGS += -Wno-style
COMPILE_ARGS += -Wno-BLKANDNBLK
COMPILE_ARGS += -Wno-WIDTHEXPAND
COMPILE_ARGS += -Wno-WIDTHTRUNC
COMPILE_ARGS += -Wno-WIDTHCONCAT
COMPILE_ARGS += -Wno-ASCRANGE
COMPILE_ARGS += --timing
COMPILE_ARGS += --autoflush
COMPILE_ARGS += --x-assign fast
COMPILE_ARGS += --x-initial fast

COMPILE_ARGS += -f croc_cocotb.f

SIM_ARGS += +binary=../../sw/bin/helloworld.hex

include $(shell cocotb-config --makefiles)/Makefile.sim