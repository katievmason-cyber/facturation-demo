from collections import defaultdict
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal

VAT_RATES = {
    "normal": Decimal("0.20"),
    "intermediaire": Decimal("0.10"),
    "reduit": Decimal("0.055"),
    "super_reduit": Decimal("0.021"),
}

CENT = Decimal("0.01")

# Arrondi de la TVA : par facture (par taux, sur le total HT) ou par ligne.
ROUNDING_PER_INVOICE = "facture"
ROUNDING_PER_LINE = "ligne"
ROUNDING_MODES = (ROUNDING_PER_INVOICE, ROUNDING_PER_LINE)


def to_decimal(value):
    return value if isinstance(value, Decimal) else Decimal(str(value))


def to_cents(amount):
    return to_decimal(amount).quantize(CENT, rounding=ROUND_HALF_UP)


@dataclass
class LineItem:
    description: str
    unit_price: Decimal
    quantity: int
    vat_rate: Decimal

    def __post_init__(self):
        self.unit_price = to_decimal(self.unit_price)
        self.vat_rate = to_decimal(self.vat_rate)

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
    rounding: str = ROUNDING_PER_INVOICE

    def __post_init__(self):
        if self.rounding not in ROUNDING_MODES:
            raise ValueError(f"Unsupported rounding mode: {self.rounding}")

    def add_line(self, description, unit_price, quantity, vat_rate):
        if to_decimal(vat_rate) not in VAT_RATES.values():
            raise ValueError(f"Unsupported VAT rate: {vat_rate}")
        self.lines.append(LineItem(description, unit_price, quantity, vat_rate))

    def total_excl_vat(self):
        return to_cents(sum((line.total_excl_vat for line in self.lines), Decimal(0)))

    def vat_by_rate(self):
        if self.rounding == ROUNDING_PER_LINE:
            vat = defaultdict(Decimal)
            for line in self.lines:
                vat[line.vat_rate] += to_cents(line.vat)
            return dict(vat)
        base = defaultdict(Decimal)
        for line in self.lines:
            base[line.vat_rate] += line.total_excl_vat
        return {rate: to_cents(amount * rate) for rate, amount in base.items()}

    def total_vat(self):
        return sum(self.vat_by_rate().values(), Decimal("0.00"))

    def total_incl_vat(self):
        return self.total_excl_vat() + self.total_vat()
