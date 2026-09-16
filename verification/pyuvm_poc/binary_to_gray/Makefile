SIM ?= verilator
TOPLEVEL_LANG = verilog

VERILOG_SOURCES = $(shell pwd)/../../../rtl/common_cells/binary_to_gray.sv

TOPLEVEL = binary_to_gray
COCOTB_TEST_MODULES = test_binary_to_gray

COMPILE_ARGS += -GN=4

include $(shell cocotb-config --makefiles)/Makefile.sim