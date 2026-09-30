from reusable_env.env.base_coverage import BaseValueCoverage


class BinaryToGrayCoverage(BaseValueCoverage):
    def __init__(self, width=4):
        self.width = width
        super().__init__(total_values=1 << width)

    def report(self):
        return (
            f"Functional coverage: "
            f"{self.covered_values}/{self.total_values} "
            f"input values ({self.percentage:.1f}%)"
        )
