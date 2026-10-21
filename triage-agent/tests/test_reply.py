import re
import unittest

from triage_agent.classify import CATEGORIES
from triage_agent.models import Ticket
from triage_agent.reply import draft_reply

TICKET = Ticket("T-999", "Claire Martin", "c@example.fr", "Sujet", "Corps")
INFORMAL_FR = re.compile(r"\b(tu|toi|ton|ta|tes|te)\b", re.IGNORECASE)


class DraftReplyTest(unittest.TestCase):
    def test_french_replies_use_vous_and_never_tu(self):
        for category in CATEGORIES:
            for urgency in ("P1", "P2", "P3"):
                reply = draft_reply(TICKET, "fr", category, urgency)
                self.assertRegex(reply, r"\bvous\b|\bvotre\b")
                self.assertIsNone(INFORMAL_FR.search(reply), reply)
                self.assertTrue(reply.startswith("Bonjour Claire Martin,"))
                self.assertIn("T-999", reply)

    def test_english_reply(self):
        reply = draft_reply(TICKET, "en", "billing", "P1")
        self.assertTrue(reply.startswith("Hello Claire Martin,"))
        self.assertIn("billing team", reply)
        self.assertIn("top priority", reply)

    def test_missing_name_falls_back(self):
        ticket = Ticket("T-1", "", "", "", "")
        self.assertTrue(draft_reply(ticket, "fr", "bug", "P2").startswith("Bonjour Madame, Monsieur,"))


if __name__ == "__main__":
    unittest.main()
