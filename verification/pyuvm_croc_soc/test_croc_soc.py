import cocotb
from cocotb.triggers import RisingEdge
from pyuvm import uvm_monitor, uvm_env, uvm_test, test

class CrocMonitor(uvm_monitor):

    async def run_phase(self):
        cocotb.log.info("CrocMonitor iniciado")

        for ciclo in range(10):
            await RisingEdge(cocotb.top.sys_clk)

            cocotb.log.info(
                f"Ciclo {ciclo + 1}: "
                f"rst_n={cocotb.top.rst_n.value}, "
                f"uart_tx={cocotb.top.uart_tx.value}, "
                f"gpio_out={cocotb.top.gpio_out.value}"
            )
class CrocEnv(uvm_env):

    def build_phase(self):
        super().build_phase()

        self.monitor = CrocMonitor("monitor", self)

@test()
class CrocTest(uvm_test):

    def build_phase(self):
        super().build_phase()

        self.env = CrocEnv("env", self)

    async def run_phase(self):
        self.raise_objection()

        cocotb.log.info("CrocTest executando")

        for _ in range(12):
            await RisingEdge(cocotb.top.sys_clk)

        self.drop_objection()