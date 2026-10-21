import unittest

from triage_agent.classify import classify


class ClassifyTest(unittest.TestCase):
    def assertCategory(self, text, expected):
        result = classify(text)
        self.assertEqual(result.category, expected, result.scores)
        return result

    def test_billing_fr(self):
        self.assertCategory("La TVA de notre facture est fausse, merci de corriger le montant.", "billing")

    def test_billing_en(self):
        self.assertCategory("Please refund our last subscription payment.", "billing")

    def test_bug_beats_billing_when_app_errors(self):
        self.assertCategory("Erreur 500 quand je clique sur Générer la facture, l'application plante.", "bug")

    def test_bug_en(self):
        self.assertCategory("The PDF export crashes with an error.", "bug")

    def test_access_fr(self):
        self.assertCategory("Je ne peux plus me connecter, mot de passe refusé.", "access")

    def test_access_en(self):
        self.assertCategory("Locked out of my account after enabling 2FA.", "access")

    def test_other_feature_request(self):
        self.assertCategory("Suggestion : serait-il possible d'ajouter une intégration Sage ?", "other")

    def test_no_keywords_is_other_and_low_confidence(self):
        result = self.assertCategory("Can someone call me back?", "other")
        self.assertFalse(result.confident)

    def test_tie_is_low_confidence(self):
        result = classify("password invoice")  # access 3 vs billing 1 -> not a tie
        self.assertTrue(result.confident)
        result = classify("erreur paiement")  # bug 2 vs billing 2
        self.assertFalse(result.confident)
        self.assertIn("tie", result.low_confidence_reason)

    def test_weak_signal_is_low_confidence(self):
        result = classify("A quick question.")
        self.assertEqual(result.category, "other")
        self.assertFalse(result.confident)


if __name__ == "__main__":
    unittest.main()
