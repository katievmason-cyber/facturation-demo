# facturation-demo

A small invoicing service that supports French VAT (TVA) rates.

*Un petit service de facturation qui gère les taux de TVA français.*

## VAT rates / Taux de TVA

| Key | Rate |
|-----|------|
| `normal` | 20 % |
| `intermediaire` | 10 % |
| `reduit` | 5,5 % |
| `super_reduit` | 2,1 % |

## Usage / Utilisation

```bash
python -m facturation examples/facture_01.json
python -m facturation examples/facture_02.json
```

Requires Python 3.9+ and no external dependencies.

*Nécessite Python 3.9+ et aucune dépendance externe.*
