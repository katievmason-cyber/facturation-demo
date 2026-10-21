import unittest

from triage_agent.urgency import assess_urgency, payment_problem


class PaymentRuleTest(unittest.TestCase):
    """A blocked payment or a double charge is always P1."""

    def assertP1(self, text):
        self.assertEqual(assess_urgency(text).level, "P1", text)
        self.assertTrue(assess_urgency(text).reasons[0].startswith("always P1"), text)

    def test_payment_blocked_fr(self):
        self.assertP1("Notre paiement a été refusé ce mois-ci.")
        self.assertP1("Paiement bloqué depuis hier.")
        self.assertP1("Le paiement par carte a échoué.")

    def test_payment_blocked_en(self):
        self.assertP1("Our payment was declined.")
        self.assertP1("The payment keeps failing at checkout.")
        self.assertP1("Payment blocked, please help.")

    def test_double_charge_fr(self):
        self.assertP1("Notre abonnement a été débité deux fois.")
        self.assertP1("Nous constatons un double prélèvement sur notre compte.")
        self.assertP1("Le paiement apparaît en double sur notre relevé.")

    def test_double_charge_en(self):
        self.assertP1("We were charged twice for October.")
        self.assertP1("There is a duplicate payment on our card.")

    def test_payment_mention_without_problem_is_not_forced(self):
        self.assertEqual(payment_problem("Which payment methods do you accept?"), "")
        self.assertEqual(assess_urgency("Quels moyens de paiement acceptez-vous ?").level, "P3")

    def test_blocked_far_from_payment_is_not_forced(self):
        text = "Question sur le paiement annuel. Par ailleurs, un de nos stagiaires est bloqué sur la formation."
        self.assertEqual(payment_problem(text), "")

    def test_retrying_twice_is_not_a_double_charge(self):
        self.assertEqual(payment_problem("J'ai réinitialisé mon mot de passe deux fois."), "")


class UrgencyLevelsTest(unittest.TestCase):
    def test_p1_outage_or_whole_team(self):
        self.assertEqual(assess_urgency("Toute l'équipe est bloquée, erreur 500.").level, "P1")
        self.assertEqual(assess_urgency("The platform is down for all users.").level, "P1")

    def test_p1_security(self):
        self.assertEqual(assess_urgency("Nous craignons un piratage de notre compte.").level, "P1")

    def test_p2_single_user_blocked_or_wrong_amount(self):
        self.assertEqual(assess_urgency("Impossible de me connecter.").level, "P2")
        self.assertEqual(assess_urgency("The VAT on my invoice is wrong.").level, "P2")

    def test_p3_question(self):
        self.assertEqual(assess_urgency("How does pricing work for 20 users?").level, "P3")

    def test_escalation_keyword_raises_one_level(self):
        self.assertEqual(assess_urgency("Question sur l'export, c'est urgent.").level, "P2")
        self.assertEqual(assess_urgency("Invoice total is wrong, please fix ASAP.").level, "P1")


if __name__ == "__main__":
    unittest.main()
