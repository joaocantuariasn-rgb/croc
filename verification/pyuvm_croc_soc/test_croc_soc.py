import cocotb
from cocotb.triggers import RisingEdge
from pyuvm import uvm_monitor, uvm_env, uvm_test, uvm_analysis_port, uvm_subscriber, test

class CrocMonitor(uvm_monitor):

    def build_phase(self):
        super().build_phase()
        self.ap = uvm_analysis_port("ap", self)

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

            self.ap.write({
                "ciclo": ciclo + 1,
                "rst_n": int(cocotb.top.rst_n.value),
                "uart_tx": int(cocotb.top.uart_tx.value),
                "gpio_out": int(cocotb.top.gpio_out.value)
            })

class CrocScoreboard(uvm_subscriber):

    def write(self, dados):

        if dados["rst_n"] == 0:
            self.viu_reset_ativo = True

        if dados["rst_n"] == 1:
            self.viu_reset_liberado = True

        cocotb.log.info(
            f"Scoreboard recebeu: "
            f"ciclo={dados['ciclo']}, "
            f"rst_n={dados['rst_n']}, "
            f"uart_tx={dados['uart_tx']}, "
            f"gpio_out={dados['gpio_out']}"
        )

    def check_phase(self):
        super().check_phase()

        assert self.viu_reset_ativo, \
            "ERRO: rst_n nunca ficou em 0"

        assert self.viu_reset_liberado, \
            "ERRO: rst_n nunca foi liberado para 1"

        cocotb.log.info(
            "PASSOU: reset do Croc foi ativado e depois liberado"
        )

    def build_phase(self):
        super().build_phase()

        self.viu_reset_ativo = False
        self.viu_reset_liberado = False

class CrocEnv(uvm_env):

    def build_phase(self):
        super().build_phase()

        self.monitor = CrocMonitor("monitor", self)
        self.scoreboard = CrocScoreboard("scoreboard", self)

    def connect_phase(self):
        super().connect_phase()

        self.monitor.ap.connect(self.scoreboard.analysis_export)

@test()
class CrocTest(uvm_test):

    def build_phase(self):
        super().build_phase()

        self.env = CrocEnv("env", self)

    async def run_phase(self):
        self.raise_objection()

        cocotb.log.info("CrocTest executando")

        for ciclo in range(12):
            await RisingEdge(cocotb.top.sys_clk)

        self.drop_objection()

