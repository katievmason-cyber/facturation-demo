import contextlib
import io
import os
import tempfile
import unittest

from triage_agent.cli import main
from triage_agent.models import Ticket
from triage_agent.pipeline import read_tickets, triage_all, triage_ticket
from triage_agent.report import render_report

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_CSV = os.path.join(ROOT, "data", "tickets.csv")
SAMPLE_OUTPUT = os.path.join(ROOT, "sample_output")

# ticket_id: (language, category, urgency, needs_review)
EXPECTED = {
    "T-001": ("fr", "billing", "P2", False),
    "T-002": ("fr", "billing", "P1", True),
    "T-003": ("fr", "bug", "P1", False),
    "T-004": ("fr", "access", "P2", False),
    "T-005": ("fr", "access", "P1", True),
    "T-006": ("fr", "other", "P3", False),
    "T-007": ("fr", "other", "P3", True),
    "T-008": ("fr", "billing", "P1", False),
    "T-009": ("en", "billing", "P1", True),
    "T-010": ("en", "bug", "P2", False),
    "T-011": ("en", "access", "P1", False),
    "T-012": ("en", "billing", "P3", False),
    "T-013": ("en", "billing", "P1", False),
    "T-014": ("en", "other", "P3", True),
    "T-015": ("en", "access", "P3", False),
}


class SampleTicketsTest(unittest.TestCase):
    def setUp(self):
        self.results = triage_all(read_tickets(SAMPLE_CSV))

    def test_every_sample_ticket(self):
        self.assertEqual(len(self.results), 15)
        for r in self.results:
            with self.subTest(ticket=r.ticket.ticket_id):
                got = (r.language, r.category, r.urgency, r.needs_review)
                self.assertEqual(got, EXPECTED[r.ticket.ticket_id], r.review_reasons + r.urgency_reasons)

    def test_report_counts(self):
        report = render_report(self.results)
        self.assertIn("| billing | 6 | 40 % |", report)
        self.assertIn("| P1 | 7 | 47 % |", report)
        self.assertIn("| **Total** | 7 | 3 | 5 | 15 |", report)
        self.assertIn("## Détail par ticket / Per-ticket detail", report)
        self.assertIn("Bonjour Claire Martin,<br>", report)

    def test_committed_sample_output_is_up_to_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            with contextlib.redirect_stdout(io.StringIO()):
                main([SAMPLE_CSV, "--out", tmp])
            for name in ("report.md", "triaged.csv"):
                with open(os.path.join(tmp, name), encoding="utf-8") as fresh, \
                        open(os.path.join(SAMPLE_OUTPUT, name), encoding="utf-8") as committed:
                    self.assertEqual(fresh.read(), committed.read(), f"regenerate sample_output/{name}")


class ReviewFlagTest(unittest.TestCase):
    def test_sensitive_topics_are_flagged(self):
        r = triage_ticket(Ticket("T-1", "A", "", "Remboursement", "Merci de nous rembourser la facture."))
        self.assertTrue(r.needs_review)
        self.assertIn("refund requested", r.review_reasons)

    def test_clear_ticket_is_not_flagged(self):
        body = "Bonjour, je n'arrive plus à me connecter à mon compte depuis ce matin."
        r = triage_ticket(Ticket("T-2", "A", "", "Mot de passe", body))
        self.assertFalse(r.needs_review)

    def test_report_pipes_and_newlines_are_escaped(self):
        r = triage_ticket(Ticket("T-3", "A", "", "a | b", "Bonjour"))
        self.assertIn("a \\| b", render_report([r]))


if __name__ == "__main__":
    unittest.main()
