"""Reply templates. French replies always use the formal "vous"."""

from .models import Ticket

TEMPLATES = {
    "fr": {
        "greeting": "Bonjour {name},",
        "intro": "Merci de nous avoir contactés. Nous avons bien reçu votre demande ({ticket_id}).",
        "category": {
            "billing": "Notre équipe facturation examine votre dossier "
                       "et reviendra vers vous avec une réponse précise.",
            "bug": "Nous avons transmis le problème à notre équipe technique afin qu'elle le reproduise et le corrige. "
                   "Si vous en avez une, n'hésitez pas à nous envoyer une capture d'écran.",
            "access": "Pour votre sécurité, nous allons vérifier votre compte avant de rétablir votre accès. "
                      "Nous ne vous demanderons jamais votre mot de passe.",
            "other": "Nous transmettons votre message à l'équipe concernée.",
        },
        "urgency": {
            "P1": "Votre demande est traitée en priorité absolue.",
            "P2": "Nous revenons vers vous dans les meilleurs délais.",
            "P3": "Nous vous répondrons dans les prochains jours.",
        },
        "closing": "Cordialement,\nL'équipe Support",
    },
    "en": {
        "greeting": "Hello {name},",
        "intro": "Thank you for getting in touch. We have received your request ({ticket_id}).",
        "category": {
            "billing": "Our billing team is reviewing your account and will come back to you with a clear answer.",
            "bug": "We have passed the issue to our technical team so they can reproduce and fix it. "
                   "If you have a screenshot, please feel free to send it to us.",
            "access": "For your security, we will verify your account before restoring access. "
                      "We will never ask you for your password.",
            "other": "We are forwarding your message to the right team.",
        },
        "urgency": {
            "P1": "Your request is being handled as a top priority.",
            "P2": "We will get back to you as soon as possible.",
            "P3": "We will reply within the next few days.",
        },
        "closing": "Kind regards,\nThe Support Team",
    },
}


def draft_reply(ticket: Ticket, language: str, category: str, urgency: str) -> str:
    t = TEMPLATES.get(language, TEMPLATES["en"])
    name = ticket.customer_name.strip() or ("Madame, Monsieur" if language == "fr" else "there")
    body = " ".join([
        t["intro"].format(ticket_id=ticket.ticket_id),
        t["category"][category],
        t["urgency"][urgency],
    ])
    return "\n\n".join([t["greeting"].format(name=name), body, t["closing"]])
