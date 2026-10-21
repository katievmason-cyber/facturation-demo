# triage-agent

A rule-based support-ticket triage agent for French and English tickets. It uses only the Python standard library: no API keys, no network calls and no dependencies.

*Un agent de triage de tickets support, en français et en anglais, fondé uniquement sur des règles. Il n'utilise que la bibliothèque standard Python : aucune clé d'API, aucun appel réseau, aucune dépendance.*

## What it does / Ce qu'il fait

For each ticket in a CSV file, the agent:

1. **Detects the language** (`fr` / `en`). It scores common French and English words and counts French accents.
2. **Classifies the ticket** as `billing`, `bug`, `access` or `other`, using weighted keywords in both languages. If no keyword matches, the ticket goes to `other`.
3. **Assigns an urgency** (`P1`–`P3`):

   | Level | Rule |
   |---|---|
   | **P1** | Outage, a whole team blocked, data loss or a security issue. **Any blocked, refused or failed payment, or any double charge, is always P1.** |
   | **P2** | One user blocked, an error or crash, a wrong amount, or a refund request. |
   | **P3** | A question or a feature request. |

   Words like "urgent", "ASAP" or "au plus vite" raise the urgency by one level.
4. **Drafts a short, polite reply** in the ticket's language. French replies always use "vous".
5. **Flags the ticket for human review** in these cases:
   - the language is unclear;
   - the category is a tie or the keyword signal is weak;
   - the ticket touches a sensitive topic: GDPR/RGPD, a possible security incident, a refund, or legal wording.

*Pour chaque ticket : détection de la langue, catégorie, urgence, brouillon de réponse (toujours avec « vous » en français) et, si besoin, un indicateur « à revoir par un humain ». Un paiement bloqué ou débité deux fois est toujours classé P1.*

## Usage / Utilisation

```bash
cd triage-agent
python -m triage_agent data/tickets.csv --out out
```

This writes two files:

- `out/triaged.csv`: one row per ticket, with the language, category, urgency, review flag, the reasons, and the draft reply.
- `out/report.md`: counts per category, urgency and language, a category × urgency table, the P1 tickets, the tickets that need review, and a per-ticket table with the draft replies.

For an example, see [`sample_output/report.md`](sample_output/report.md), which was generated from the 15 sample tickets in [`data/tickets.csv`](data/tickets.csv).

### Input format / Format d'entrée

The input is a UTF-8 CSV with these columns: `ticket_id, customer_name, email, subject, body, created_at` (`created_at` is optional).

## Tests

```bash
cd triage-agent
python -m unittest -v
```

The tests also check that `sample_output/` is up to date. If you change a rule, regenerate it with:

`python -m triage_agent data/tickets.csv --out sample_output`

## Layout / Structure

| File | Role |
|---|---|
| `triage_agent/language.py` | Language detection |
| `triage_agent/classify.py` | Category keywords and scoring |
| `triage_agent/urgency.py` | P1–P3 rules, including the payment rule |
| `triage_agent/reply.py` | Reply templates (FR / EN) |
| `triage_agent/pipeline.py` | CSV input and output, human-review flags |
| `triage_agent/report.py` | Markdown report |

To tune the agent, edit the keyword lists. The patterns are regular expressions matched against lowercase text with the accents removed.

## Limits / Limites

This is keyword matching, not language understanding. Sarcasm, negations ("ce n'est pas urgent") and tickets that mix several topics can be misclassified. The review flag exists for those cases, so a person checks the draft before it is sent.

Requires Python 3.9+.
