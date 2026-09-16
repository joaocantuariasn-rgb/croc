import cocotb
from cocotb.triggers import RisingEdge


@cocotb.test()
async def test_croc_soc_access(dut):

    cocotb.log.info("Cocotb conectado ao Croc SoC")

    cocotb.log.info(f"rst_n    = {dut.rst_n.value}")
    cocotb.log.info(f"sys_clk  = {dut.sys_clk.value}")
    cocotb.log.info(f"uart_tx  = {dut.uart_tx.value}")
    cocotb.log.info(f"gpio_out = {dut.gpio_out.value}")

    # Aguarda alguns ciclos do clock real gerado pelo croc_vip
    for _ in range(10):
        await RisingEdge(dut.sys_clk)

    cocotb.log.info("10 ciclos do clock do Croc observados com sucesso")

    cocotb.log.info(f"rst_n após 10 ciclos = {dut.rst_n.value}")