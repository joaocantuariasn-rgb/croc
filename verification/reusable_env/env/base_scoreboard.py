from pyuvm import uvm_subscriber


class BaseScoreboard(uvm_subscriber):

    def compare(self, actual, expected, context=""):
        if actual != expected:
            raise AssertionError(
                f"Scoreboard mismatch: "
                f"actual={actual}, expected={expected}"
                + (f", {context}" if context else "")
            )

        self.logger.info(
            f"Scoreboard match: "
            f"actual={actual}, expected={expected}"
            + (f", {context}" if context else "")
        )
