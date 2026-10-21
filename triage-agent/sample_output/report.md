# Rapport de triage / Triage report

Source : `tickets.csv`

- **Tickets :** 15
- **P1 :** 7
- **À revoir par un humain / Needs human review :** 5

## Par catégorie / By category

| Catégorie / Category | Tickets | % |
|---|---|---|
| billing | 6 | 40 % |
| bug | 2 | 13 % |
| access | 4 | 27 % |
| other | 3 | 20 % |

## Par urgence / By urgency

| Urgence / Urgency | Tickets | % |
|---|---|---|
| P1 | 7 | 47 % |
| P2 | 3 | 20 % |
| P3 | 5 | 33 % |

## Par langue / By language

| Langue / Language | Tickets | % |
|---|---|---|
| fr | 8 | 53 % |
| en | 7 | 47 % |

## Catégorie × urgence / Category × urgency

|  | P1 | P2 | P3 | Total |
|---|---|---|---|---|
| billing | 4 | 1 | 1 | 6 |
| bug | 1 | 1 | 0 | 2 |
| access | 2 | 1 | 1 | 4 |
| other | 0 | 0 | 3 | 3 |
| **Total** | 7 | 3 | 5 | 15 |

## Tickets P1

| ID | Catégorie | Sujet / Subject | Raison / Reason |
|---|---|---|---|
| T-002 | billing | Paiement débité deux fois | always P1: payment charged twice ('debite deux fois') |
| T-003 | bug | Plus aucune facture ne se génère - URGENT | critical impact ('toute l equipe') |
| T-005 | access | Compte administrateur verrouillé | critical impact ('personne ne peut') |
| T-008 | billing | Paiement refusé, abonnement suspendu | always P1: payment blocked ('paiement' ... 'refuse') |
| T-009 | billing | Charged twice for October | always P1: payment charged twice ('charged twice') |
| T-011 | access | Can't log in with SSO | critical impact ('whole team') |
| T-013 | billing | Payment blocked at checkout | always P1: payment blocked ('payment' ... 'blocked') |

## À revoir par un humain / Needs human review

| ID | Catégorie | Urgence | Raison / Reason |
|---|---|---|---|
| T-002 | billing | P1 | refund requested |
| T-005 | access | P1 | possible security incident |
| T-007 | other | P3 | personal data request (GDPR) |
| T-009 | billing | P1 | refund requested |
| T-014 | other | P3 | no category keywords matched |

## Détail par ticket / Per-ticket detail

| ID | Langue | Catégorie | Urgence | Revue | Sujet / Subject | Réponse proposée / Draft reply |
|---|---|---|---|---|---|---|
| T-001 | fr | billing | P2 | non | TVA incorrecte sur la facture F-2026-0412 | Bonjour Claire Martin,<br><br>Merci de nous avoir contactés. Nous avons bien reçu votre demande (T-001). Notre équipe facturation examine votre dossier et reviendra vers vous avec une réponse précise. Nous revenons vers vous dans les meilleurs délais.<br><br>Cordialement,<br>L'équipe Support |
| T-002 | fr | billing | P1 | oui | Paiement débité deux fois | Bonjour Julien Moreau,<br><br>Merci de nous avoir contactés. Nous avons bien reçu votre demande (T-002). Notre équipe facturation examine votre dossier et reviendra vers vous avec une réponse précise. Votre demande est traitée en priorité absolue.<br><br>Cordialement,<br>L'équipe Support |
| T-003 | fr | bug | P1 | non | Plus aucune facture ne se génère - URGENT | Bonjour Sophie Lefèvre,<br><br>Merci de nous avoir contactés. Nous avons bien reçu votre demande (T-003). Nous avons transmis le problème à notre équipe technique afin qu'elle le reproduise et le corrige. Si vous en avez une, n'hésitez pas à nous envoyer une capture d'écran. Votre demande est traitée en priorité absolue.<br><br>Cordialement,<br>L'équipe Support |
| T-004 | fr | access | P2 | non | Impossible de me connecter | Bonjour Thomas Bernard,<br><br>Merci de nous avoir contactés. Nous avons bien reçu votre demande (T-004). Pour votre sécurité, nous allons vérifier votre compte avant de rétablir votre accès. Nous ne vous demanderons jamais votre mot de passe. Nous revenons vers vous dans les meilleurs délais.<br><br>Cordialement,<br>L'équipe Support |
| T-005 | fr | access | P1 | oui | Compte administrateur verrouillé | Bonjour Camille Dubois,<br><br>Merci de nous avoir contactés. Nous avons bien reçu votre demande (T-005). Pour votre sécurité, nous allons vérifier votre compte avant de rétablir votre accès. Nous ne vous demanderons jamais votre mot de passe. Votre demande est traitée en priorité absolue.<br><br>Cordialement,<br>L'équipe Support |
| T-006 | fr | other | P3 | non | Suggestion : export vers Sage | Bonjour Nicolas Petit,<br><br>Merci de nous avoir contactés. Nous avons bien reçu votre demande (T-006). Nous transmettons votre message à l'équipe concernée. Nous vous répondrons dans les prochains jours.<br><br>Cordialement,<br>L'équipe Support |
| T-007 | fr | other | P3 | oui | Demande de suppression de données (RGPD) | Bonjour Émilie Roux,<br><br>Merci de nous avoir contactés. Nous avons bien reçu votre demande (T-007). Nous transmettons votre message à l'équipe concernée. Nous vous répondrons dans les prochains jours.<br><br>Cordialement,<br>L'équipe Support |
| T-008 | fr | billing | P1 | non | Paiement refusé, abonnement suspendu | Bonjour Antoine Girard,<br><br>Merci de nous avoir contactés. Nous avons bien reçu votre demande (T-008). Notre équipe facturation examine votre dossier et reviendra vers vous avec une réponse précise. Votre demande est traitée en priorité absolue.<br><br>Cordialement,<br>L'équipe Support |
| T-009 | en | billing | P1 | oui | Charged twice for October | Hello Sarah Thompson,<br><br>Thank you for getting in touch. We have received your request (T-009). Our billing team is reviewing your account and will come back to you with a clear answer. Your request is being handled as a top priority.<br><br>Kind regards,<br>The Support Team |
| T-010 | en | bug | P2 | non | PDF export crashes | Hello James Wilson,<br><br>Thank you for getting in touch. We have received your request (T-010). We have passed the issue to our technical team so they can reproduce and fix it. If you have a screenshot, please feel free to send it to us. We will get back to you as soon as possible.<br><br>Kind regards,<br>The Support Team |
| T-011 | en | access | P1 | non | Can't log in with SSO | Hello Emma Clarke,<br><br>Thank you for getting in touch. We have received your request (T-011). For your security, we will verify your account before restoring access. We will never ask you for your password. Your request is being handled as a top priority.<br><br>Kind regards,<br>The Support Team |
| T-012 | en | billing | P3 | non | Question about pricing for 20 users | Hello Oliver Brown,<br><br>Thank you for getting in touch. We have received your request (T-012). Our billing team is reviewing your account and will come back to you with a clear answer. We will reply within the next few days.<br><br>Kind regards,<br>The Support Team |
| T-013 | en | billing | P1 | non | Payment blocked at checkout | Hello Priya Patel,<br><br>Thank you for getting in touch. We have received your request (T-013). Our billing team is reviewing your account and will come back to you with a clear answer. Your request is being handled as a top priority.<br><br>Kind regards,<br>The Support Team |
| T-014 | en | other | P3 | oui | Hello | Hello Daniel Hughes,<br><br>Thank you for getting in touch. We have received your request (T-014). We are forwarding your message to the right team. We will reply within the next few days.<br><br>Kind regards,<br>The Support Team |
| T-015 | en | access | P3 | non | Invitation link expired | Hello Laura Mitchell,<br><br>Thank you for getting in touch. We have received your request (T-015). For your security, we will verify your account before restoring access. We will never ask you for your password. We will reply within the next few days.<br><br>Kind regards,<br>The Support Team |
