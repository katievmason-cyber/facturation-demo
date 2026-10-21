import json
import sys
from decimal import Decimal

from .invoice import Invoice


def load_invoice(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f, parse_float=Decimal)
    invoice = Invoice(number=data["number"], customer=data["customer"])
    for line in data["lines"]:
        invoice.add_line(line["description"], line["unit_price"], line["quantity"], line["vat_rate"])
    return invoice


def format_rate(rate):
    return f"{float(rate * 100):g}"


def render(invoice):
    out = [f"Facture {invoice.number} - {invoice.customer}", "-" * 60]
    for line in invoice.lines:
        out.append(
            f"{line.description:<30} {line.quantity:>3} x {line.unit_price:>8.2f} EUR  TVA {format_rate(line.vat_rate)}%"
        )
    out.append("-" * 60)
    out.append(f"Total HT  : {invoice.total_excl_vat():>10.2f} EUR")
    out.append(f"Total TVA : {invoice.total_vat():>10.2f} EUR")
    out.append(f"Total TTC : {invoice.total_incl_vat():>10.2f} EUR")
    return "\n".join(out)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python -m facturation <invoice.json>")
        return 1
    print(render(load_invoice(argv[0])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
