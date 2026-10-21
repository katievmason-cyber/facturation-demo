from dataclasses import dataclass, field

VAT_RATES = {
    "normal": 0.20,
    "intermediaire": 0.10,
    "reduit": 0.055,
    "super_reduit": 0.021,
}


def to_cents(amount):
    return int(amount * 100) / 100


@dataclass
class LineItem:
    description: str
    unit_price: float
    quantity: int
    vat_rate: float

    @property
    def total_excl_vat(self):
        return self.unit_price * self.quantity

    @property
    def vat(self):
        return self.total_excl_vat * self.vat_rate


@dataclass
class Invoice:
    number: str
    customer: str
    lines: list = field(default_factory=list)

    def add_line(self, description, unit_price, quantity, vat_rate):
        if vat_rate not in VAT_RATES.values():
            raise ValueError(f"Unsupported VAT rate: {vat_rate}")
        self.lines.append(LineItem(description, unit_price, quantity, vat_rate))

    def total_excl_vat(self):
        return to_cents(sum(line.total_excl_vat for line in self.lines))

    def total_vat(self):
        return to_cents(sum(line.vat for line in self.lines))

    def total_incl_vat(self):
        return to_cents(self.total_excl_vat() + self.total_vat())
