import unittest
from decimal import Decimal

from facturation import Invoice


def invoice_with(*lines):
    invoice = Invoice(number="TEST", customer="Client test")
    for unit_price, quantity, vat_rate in lines:
        invoice.add_line("Ligne", unit_price, quantity, vat_rate)
    return invoice


class TvaParTauxTest(unittest.TestCase):
    """TVA attendue = HT x taux, arrondie au centime le plus proche."""

    def assertVat(self, invoice, expected):
        self.assertEqual(Decimal(str(invoice.total_vat())), Decimal(expected))

    def test_taux_normal_20(self):
        # FACT-142 : facture_01.json, 20 % de 169,00 EUR
        self.assertVat(invoice_with((49.00, 1, 0.20), (60.00, 2, 0.20)), "33.80")
        self.assertVat(invoice_with((1.14, 1, 0.20)), "0.23")

    def test_taux_intermediaire_10(self):
        self.assertVat(invoice_with((1.07, 1, 0.10)), "0.11")
        self.assertVat(invoice_with((1.49, 1, 0.10)), "0.15")

    def test_taux_reduit_5_5(self):
        self.assertVat(invoice_with((12.90, 3, 0.055)), "2.13")
        self.assertVat(invoice_with((1.21, 1, 0.055)), "0.07")

    def test_taux_super_reduit_2_1(self):
        self.assertVat(invoice_with((1.15, 9, 0.021)), "0.22")
        self.assertVat(invoice_with((1.21, 1, 0.021)), "0.03")

    def test_total_ttc_egal_ht_plus_tva(self):
        invoice = invoice_with((49.00, 1, 0.20), (60.00, 2, 0.20))
        self.assertEqual(Decimal(str(invoice.total_excl_vat())), Decimal("169.00"))
        self.assertEqual(Decimal(str(invoice.total_incl_vat())), Decimal("202.80"))


if __name__ == "__main__":
    unittest.main()
