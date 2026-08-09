# Ketenpunt-tool — maturitymodel voor derde diensten

**Live demo: [uvascript26.streamlit.app](https://uvascript26.streamlit.app)**

Proof-of-concept bij een afstudeeronderzoek (UvA, Executive Programme of
Digital Auditing) naar het beheersen van risico's van derde diensten op
het *ketenpunt*: het raakvlak waar een organisatie afhankelijk wordt van
externe IT-dienstverleners.

De tool operationaliseert een maturitymodel met tien beheersdomeinen in
drie lagen, verbonden via een getypeerde gewogen dwarsverbandenmatrix.
Op basis van ingevoerde volwassenheidsscores (1–5) berekent de tool
verbeterprioriteiten (hefboomwaarde × maturity-gap) en een gefaseerd
verbeterpad volgens de gelaagde structuur: fundament eerst.

## Zes tabbladen

1. **Uitvraag** — maturityscoring per domein met operationele niveaubeschrijvingen
2. **Maturityprofiel** — radardiagram van het ingevoerde profiel
3. **Dwarsverbandenmatrix** — heatmap met relatietypen (M/A/F/S/E/C)
4. **Prioritering** — hefboom × gap, met signalering van zwakke Laag 1-modifiers
5. **Getypeerde graaf** — de drie lagen met gekleurde relatiepijlen
6. **Advies & stappenplan** — interactief verbeterpad met cascade-afhankelijkheden

## Zelf draaien

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Bestanden

| Bestand | Inhoud |
|---|---|
| `app.py` | Streamlit-applicatie (zes tabbladen) |
| `model_data.json` | dwarsverbandenmatrix, relatietypen, hefboomwaarden, laagindeling |
| `kennisbasis.py` | niveaubeschrijvingen en maatregelen per domein |
| `afhankelijkheden.py` | cascade-afhankelijkheden (type M/A, score ≥ 5) |
| `stap_uitleg.py` | uitlegteksten per verbeterstap |

## Status en licentie

Dit is een demonstratie-artefact ter ondersteuning van het onderzoek,
geen productierijp adviesinstrument; de scoring en prioritering volgen
de methodiek uit de bijbehorende scriptie. Licentie: BSD-3-Clause.
