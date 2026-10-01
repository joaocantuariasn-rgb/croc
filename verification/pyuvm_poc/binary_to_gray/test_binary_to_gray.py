import cocotb
from cocotb.triggers import Timer

from pyuvm import (
    uvm_test,
    uvm_env,
    uvm_driver,
    uvm_monitor,
    uvm_sequence,
    uvm_sequence_item,
    uvm_sequencer,
    uvm_analysis_port,
    test,
)

from reference_model import binary_to_gray_reference
from coverage_model import BinaryToGrayCoverage
from reusable_env.env.base_scoreboard import BaseScoreboard

class BinaryToGrayItem(uvm_sequence_item):
    def __init__(self, name, value=0):
        super().__init__(name)
        self.value = value


class BinaryToGrayBasicSequence(uvm_sequence):
    async def body(self):
        values = [
            0b0000,
            0b0001,
            0b0010,
            0b0011,
            0b0100,
            0b0111,
            0b1000,
            0b1111,
        ]

        for value in values:
            item = BinaryToGrayItem("item", value)

            await self.start_item(item)
            await self.finish_item(item)


class BinaryToGrayFullSequence(uvm_sequence):
    async def body(self):
        for value in range(16):
            item = BinaryToGrayItem("item", value)

            await self.start_item(item)
            await self.finish_item(item)


class BinaryToGrayDriver(uvm_driver):
    async def run_phase(self):
        while True:
            item = await self.seq_item_port.get_next_item()

            cocotb.top.A.value = item.value

            await Timer(1, unit="ns")

            self.seq_item_port.item_done()


class BinaryToGrayMonitor(uvm_monitor):
    def build_phase(self):
        super().build_phase()

        self.ap = uvm_analysis_port("ap", self)
        self.coverage = BinaryToGrayCoverage(width=4)

    async def run_phase(self):
        while True:
            await Timer(1, unit="ns")

            value = int(cocotb.top.A.value)
            result = int(cocotb.top.Z.value)

            self.coverage.sample(value)

            self.ap.write((value, result))

    def report_phase(self):
        super().report_phase()

        self.logger.info(
            self.coverage.report()
        )

class BinaryToGrayScoreboard(BaseScoreboard):
    def write(self, data):
        value, result = data

        expected = binary_to_gray_reference(value)

        self.compare(
            actual=result,
            expected=expected,
            context=f"A={value:04b}"
        )


class BinaryToGrayEnv(uvm_env):
    def build_phase(self):
        super().build_phase()

        self.sequencer = uvm_sequencer("sequencer", self)
        self.driver = BinaryToGrayDriver("driver", self)
        self.monitor = BinaryToGrayMonitor("monitor", self)
        self.scoreboard = BinaryToGrayScoreboard("scoreboard", self)

    def connect_phase(self):
        super().connect_phase()

        self.driver.seq_item_port.connect(
            self.sequencer.seq_item_export
        )

        self.monitor.ap.connect(
            self.scoreboard.analysis_export
        )


@test()
class BinaryToGrayTest(uvm_test):
    def build_phase(self):
        super().build_phase()
        self.env = BinaryToGrayEnv("env", self)

    async def run_phase(self):
        self.raise_objection()

        sequence = BinaryToGrayFullSequence("full_sequence")
        await sequence.start(self.env.sequencer)

        await Timer(1, unit="ns")

        self.drop_objection()