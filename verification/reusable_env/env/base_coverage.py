class BaseValueCoverage:
    def __init__(self, total_values):
        self.total_values = total_values
        self.observed_values = set()

    def sample(self, value):
        self.observed_values.add(value)

    @property
    def covered_values(self):
        return len(self.observed_values)

    @property
    def percentage(self):
        if self.total_values == 0:
            return 0.0

        return (
            self.covered_values /
            self.total_values
        ) * 100

    def report(self):
        return (
            f"Functional coverage: "
            f"{self.covered_values}/{self.total_values} "
            f"values ({self.percentage:.1f}%)"
        )
