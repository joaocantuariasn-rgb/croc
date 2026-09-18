import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from pyuvm import uvm_monitor, uvm_env, uvm_test, uvm_analysis_port, uvm_subscriber, test


async def uart_read_byte():
    uart_tx = cocotb.top.uart_tx

    # Aguarda o início do start bit
    await FallingEdge(uart_tx)

    # Vai para o centro do start bit
    await Timer(4, unit="us")

    valor = 0

    # Lê os 8 bits, LSB primeiro
    for bit in range(8):
        await Timer(8, unit="us")

        if int(uart_tx.value):
            valor |= (1 << bit)

    # Aguarda o stop bit
    await Timer(8, unit="us")

    return valor

class CrocMonitor(uvm_monitor):

    def build_phase(self):
        super().build_phase()
        self.ap = uvm_analysis_port("ap", self)
        self.uart_ap = uvm_analysis_port("uart_ap", self)

    async def run_phase(self):
        cocotb.log.info("CrocMonitor iniciado")

        cocotb.start_soon(self.monitor_uart())

        ciclo = 0

        while True:
            await RisingEdge(cocotb.top.sys_clk)
            ciclo += 1

            core_status = int(
                cocotb.top.i_croc_soc.i_croc.i_soc_ctrl.core_status_q.value
            )

            if ciclo <= 10 or core_status != 0:
                cocotb.log.info(
                    f"Ciclo {ciclo}: "
                    f"rst_n={cocotb.top.rst_n.value}, "
                    f"uart_tx={cocotb.top.uart_tx.value}, "
                    f"gpio_out={cocotb.top.gpio_out.value}"
                )

            self.ap.write({
                "ciclo": ciclo,
                "rst_n": int(cocotb.top.rst_n.value),
                "uart_tx": int(cocotb.top.uart_tx.value),
                "gpio_out": int(cocotb.top.gpio_out.value),
                "core_status": core_status
            })

            if core_status != 0:
                cocotb.log.info(
                    f"EOC detectado: core_status=0x{core_status:08X}"
                )
                break

    async def monitor_uart(self):
        mensagem = []

        while True:
            byte = await uart_read_byte()

            if byte == 0x0A:  # '\n'
                texto = bytes(mensagem).decode("ascii", errors="replace")

                cocotb.log.info(
                    f"pyUVM UART recebeu: {texto}"
                )

                self.uart_ap.write(texto)

                mensagem.clear()
            else:
                mensagem.append(byte)

class UartScoreboard(uvm_subscriber):

    def build_phase(self):
        super().build_phase()
        self.mensagem_recebida = None

    def write(self, mensagem):
        self.mensagem_recebida = mensagem

        cocotb.log.info(
            f"UART Scoreboard recebeu: {mensagem}"
        )

class CrocScoreboard(uvm_subscriber):

    def write(self, dados):

        if dados["rst_n"] == 0:
            self.viu_reset_ativo = True

        if dados["rst_n"] == 1:
            self.viu_reset_liberado = True

        if dados["ciclo"] <= 10 or dados["core_status"] != 0:
            cocotb.log.info(
                f"Scoreboard recebeu: "
                f"ciclo={dados['ciclo']}, "
                f"rst_n={dados['rst_n']}, "
                f"uart_tx={dados['uart_tx']}, "
                f"gpio_out={dados['gpio_out']}"
            )

        if dados["core_status"] != 0:
            self.core_status_final = dados["core_status"]

    def check_phase(self):
        super().check_phase()

        assert self.viu_reset_ativo, \
            "ERRO: rst_n nunca ficou em 0"

        assert self.viu_reset_liberado, \
            "ERRO: rst_n nunca foi liberado para 1"

        assert self.core_status_final == 0x00000001, \
            f"ERRO: programa terminou com core_status=0x{self.core_status_final:08X}"
        
        cocotb.log.info(
            "PASSOU: reset validado e programa finalizado com sucesso "
            f"(core_status=0x{self.core_status_final:08X})"
        )

    def build_phase(self):
        super().build_phase()

        self.viu_reset_ativo = False
        self.viu_reset_liberado = False
        self.core_status_final = 0

class CrocEnv(uvm_env):

    def build_phase(self):
        super().build_phase()

        self.monitor = CrocMonitor("monitor", self)
        self.scoreboard = CrocScoreboard("scoreboard", self)
        self.uart_scoreboard = UartScoreboard("uart_scoreboard", self)

    def connect_phase(self):
        super().connect_phase()

        self.monitor.ap.connect(self.scoreboard.analysis_export)
        self.monitor.uart_ap.connect(
            self.uart_scoreboard.analysis_export
        )

@test()
class CrocTest(uvm_test):

    def build_phase(self):
        super().build_phase()

        self.env = CrocEnv("env", self)

    async def run_phase(self):
        self.raise_objection()

        cocotb.log.info("CrocTest executando")


        core_status = cocotb.top.i_croc_soc.i_croc.i_soc_ctrl.core_status_q

        cocotb.log.info(
            f"core_status_q encontrado: {core_status.value}"
        )

        while True:
            await RisingEdge(cocotb.top.sys_clk)

            core_status = int(
                cocotb.top.i_croc_soc.i_croc.i_soc_ctrl.core_status_q.value
            )

            if core_status != 0:
                break

        self.drop_objection()

