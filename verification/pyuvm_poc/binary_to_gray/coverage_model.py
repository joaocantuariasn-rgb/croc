class BinaryToGrayCoverage:
    def __init__(self, width=4):
        self.width = width
        self.total_values = 1 << width
        self.observed_values = set()

    def sample(self, value):
        self.observed_values.add(value)

    @property
    def percentage(self):
        return (
            len(self.observed_values)
            / self.total_values
        ) * 100

    def report(self):
        return (
            f"Functional coverage: "
            f"{len(self.observed_values)}/{self.total_values} "
            f"input values ({self.percentage:.1f}%)"
        )
