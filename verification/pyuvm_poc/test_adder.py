import cocotb
from cocotb.triggers import Timer

from pyuvm import (
    uvm_test,
    uvm_env,
    uvm_driver,
    uvm_monitor,
    uvm_scoreboard,
    uvm_sequence,
    uvm_sequence_item,
    uvm_sequencer,
    uvm_analysis_port,
    uvm_subscriber,
    test
)
class AdderItem(uvm_sequence_item):
    def __init__(self, name, a=0, b=0):
        super().__init__(name)
        self.a = a
        self.b = b
class AdderSequence(uvm_sequence):
    async def body(self):
        values = [
            (10, 20),
            (5, 7),
            (100, 50),
            (255, 255),
        ]

        for a, b in values:
            item = AdderItem("item", a, b)

            await self.start_item(item)
            await self.finish_item(item)
class AdderDriver(uvm_driver):
    async def run_phase(self):
        while True:
            item = await self.seq_item_port.get_next_item()

            cocotb.top.a.value = item.a
            cocotb.top.b.value = item.b

            await Timer(1, units="ns")

            self.seq_item_port.item_done()
class AdderMonitor(uvm_monitor):
    def build_phase(self):
        super().build_phase()
        self.ap = uvm_analysis_port("ap", self)

    async def run_phase(self):
        while True:
            await Timer(1, units="ns")

            a = int(cocotb.top.a.value)
            b = int(cocotb.top.b.value)
            result = int(cocotb.top.sum.value)

            self.ap.write((a, b, result))
class AdderScoreboard(uvm_subscriber):
    def write(self, data):
        a, b, result = data
        expected = a + b

        assert result == expected, (
            f"ERRO: {a} + {b} = {result}, esperado {expected}"
        )

        self.logger.info(
            f"PASSOU: {a} + {b} = {result}"
        )

class AdderEnv(uvm_env):
    def build_phase(self):
        super().build_phase()

        self.sequencer = uvm_sequencer("sequencer", self)
        self.driver = AdderDriver("driver", self)
        self.monitor = AdderMonitor("monitor", self)
        self.scoreboard = AdderScoreboard("scoreboard", self)

    def connect_phase(self):
        super().connect_phase()

        self.driver.seq_item_port.connect(
            self.sequencer.seq_item_export
        )

        self.monitor.ap.connect(
            self.scoreboard.analysis_export
        )
@test()
class AdderTest(uvm_test):
    def build_phase(self):
        super().build_phase()
        self.env = AdderEnv("env", self)

    async def run_phase(self):
        self.raise_objection()

        sequence = AdderSequence("sequence")
        await sequence.start(self.env.sequencer)

        await Timer(2, units="ns")

        self.drop_objection()
