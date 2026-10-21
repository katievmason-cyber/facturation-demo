import unittest

from triage_agent.language import detect_language


class DetectLanguageTest(unittest.TestCase):
    def test_french(self):
        r = detect_language("Bonjour, nous n'arrivons plus à télécharger notre facture depuis hier.")
        self.assertEqual(r.language, "fr")
        self.assertFalse(r.ambiguous)

    def test_english(self):
        r = detect_language("Hello, we can't download our invoice since yesterday. Thanks for your help.")
        self.assertEqual(r.language, "en")
        self.assertFalse(r.ambiguous)

    def test_accents_alone_point_to_french(self):
        self.assertEqual(detect_language("Facture erronée, échéance dépassée").language, "fr")

    def test_no_evidence_is_ambiguous(self):
        r = detect_language("SSO 2FA ???")
        self.assertTrue(r.ambiguous)

    def test_mixed_text_is_ambiguous(self):
        r = detect_language("Bonjour, the invoice is wrong merci")
        self.assertTrue(r.ambiguous)


if __name__ == "__main__":
    unittest.main()
