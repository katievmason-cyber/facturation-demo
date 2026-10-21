import unittest
from decimal import Decimal

from facturation import Invoice
from facturation.invoice import ROUNDING_PER_INVOICE, ROUNDING_PER_LINE


def invoice_with(rounding, *lines):
    invoice = Invoice(number="TEST", customer="Client test", rounding=rounding)
    for unit_price, quantity, vat_rate in lines:
        invoice.add_line("Ligne", unit_price, quantity, vat_rate)
    return invoice


class ModeArrondiTest(unittest.TestCase):
    LINES = [(0.10, 1, 0.055)] * 3  # 3 x 0,0055 EUR de TVA

    def test_par_defaut_arrondi_par_facture(self):
        self.assertEqual(Invoice("T", "C").rounding, ROUNDING_PER_INVOICE)

    def test_arrondi_par_facture(self):
        # 0,30 x 5,5 % = 0,0165 -> 0,02
        self.assertEqual(invoice_with(ROUNDING_PER_INVOICE, *self.LINES).total_vat(), Decimal("0.02"))

    def test_arrondi_par_ligne(self):
        # 3 x arrondi(0,0055) = 3 x 0,01 = 0,03
        self.assertEqual(invoice_with(ROUNDING_PER_LINE, *self.LINES).total_vat(), Decimal("0.03"))

    def test_arrondi_par_facture_separe_les_taux(self):
        invoice = invoice_with(ROUNDING_PER_INVOICE, (12.90, 3, 0.055), (4.35, 7, 0.20), (1.15, 9, 0.021))
        self.assertEqual(
            invoice.vat_by_rate(),
            {Decimal("0.055"): Decimal("2.13"), Decimal("0.20"): Decimal("6.09"), Decimal("0.021"): Decimal("0.22")},
        )
        self.assertEqual(invoice.total_vat(), Decimal("8.44"))

    def test_demi_centime_arrondi_au_superieur(self):
        # 0,05 x 10 % = 0,005 -> 0,01 (arrondi "au plus proche, 0,5 vers le haut")
        self.assertEqual(invoice_with(ROUNDING_PER_INVOICE, (0.05, 1, 0.10)).total_vat(), Decimal("0.01"))

    def test_mode_inconnu_refuse(self):
        with self.assertRaises(ValueError):
            Invoice("T", "C", rounding="autre")

    def test_taux_inconnu_refuse(self):
        with self.assertRaises(ValueError):
            Invoice("T", "C").add_line("Ligne", 10, 1, 0.07)


if __name__ == "__main__":
    unittest.main()
