"""
Ketenpunt Maturitymodel — Interactieve proof-of-concept
Afstudeerscriptie Daan Musulin (UvA Executive Programme of Digital Auditing)

Beheersen van risico's derde diensten op het ketenpunt.

Start met:  streamlit run app.py
Vereist:    pip install streamlit plotly networkx
"""

import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import json
import os

from kennisbasis import NIVEAUS, MAATREGELEN
from afhankelijkheden import AFHANKELIJK_VAN
from stap_uitleg import STAP_UITLEG

# ──────────────────────────────────────────────────────────────
# Data laden
# ──────────────────────────────────────────────────────────────
HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "model_data.json")) as f:
    DATA = json.load(f)

DOMAINS = DATA["domains"]
MATRIX = DATA["matrix"]
HEFBOOM = DATA["hefboom"]
LAGEN = DATA["lagen"]

# Relatietype-kleuren
TYPE_COLORS = {
    "M": "#1f4e8c",   # Modificerend - donkerblauw
    "A": "#2e8b57",   # Activerend - groen
    "F": "#e8861e",   # Feedback - oranje
    "E": "#8e44ad",   # Emergent - paars
    "C": "#95a5a6",   # Complementair - grijs
    "S": "#c0392b",   # Supportief - rood
}
TYPE_NAMES = {
    "M": "Modificerend (Laag 1→2/3)",
    "A": "Activerend (Laag 2→3)",
    "F": "Feedback (Laag 3→2)",
    "E": "Emergent (Laag 2/3→1)",
    "C": "Complementair (binnen laag)",
    "S": "Supportief (binnen laag, asymmetrisch)",
}

# Type-plafonds
PLAFONDS = {"M": 10, "A": 8, "F": 7, "S": 6, "E": 6, "C": 5}


def keten_omhoog(domein):
    """Transitieve sluiting van AFHANKELIJK_VAN.

    Geeft alle directe én indirecte onderliggende domeinen die moeten
    meegroeien om `domein` bestendig te verhogen. Doorloopt dus niet
    alleen de directe afhankelijkheden, maar ook de afhankelijkheden
    daarvan, tot aan de Laag 1-fundamenten (Governance, Cultuur), die
    zelf geen onderliggende domeinen meer hebben.

    Retourneert een set domeinnamen (exclusief `domein` zelf).
    """
    gezien = set()
    stack = list(AFHANKELIJK_VAN.get(domein, []))
    while stack:
        d = stack.pop()
        if d in gezien:
            continue
        gezien.add(d)
        for onder in AFHANKELIJK_VAN.get(d, []):
            if onder not in gezien:
                stack.append(onder)
    gezien.discard(domein)
    return gezien


def render_stappen(domein):
    """Toon de concrete maatregel en stappen voor een domein (inline,
    zonder geneste expanders zodat dit ook binnen een expander veilig is)."""
    m = MAATREGELEN[domein]
    st.info(m["maatregel"])
    st.caption(f"⏱ {m['doorlooptijd']}  |  📋 {m['norm']}  |  Effect: {m['effect']}")
    st.markdown("**Stappen:**")
    for i, stap in enumerate(m["stappen"]):
        st.markdown(f"{i + 1}. {stap}")
        u = STAP_UITLEG.get(domein, {}).get(i)
        if u:
            st.markdown(f"&nbsp;&nbsp;&nbsp;_Aanpak:_ {u['hoe']}",
                        unsafe_allow_html=True)
            for da in u["deelacties"]:
                st.markdown(f"&nbsp;&nbsp;&nbsp;&bull; {da}",
                            unsafe_allow_html=True)
            st.caption(
                f"Wie: {u['wie']} · Valkuil: {u['valkuil']} · "
                f"Klaar als: {u['resultaat']} · 📋 {u['norm']}")

# Voorbeeld-scenario's uit hoofdstuk 5 (maturityscores 1-5 per domein).
# De scores volgen de maturityprofielen uit de scriptie:
#   Scenario 1 → tabel 5.1, Scenario 2 → tabel 5.4, Scenario 3 → tabel 5.7,
#   Scenario 4 → tabel 5.10, Scenario 5 → tabel 5.13, Scenario 6 → tabel 5.16.
SCENARIOS = {
    "Scenario 1 — Consultancy (governance-dominant)": {
        "SLA": 1, "Beveiliging": 2, "Monitoring": 1, "Documentatie": 1, "BCM": 1,
        "Governance": 1, "Awareness": 1, "Cultuur": 2, "Externe borging": 1, "Normenkoppeling": 2,
    },
    "Scenario 2 — Verzekeraar (compliance-paradox)": {
        "SLA": 4, "Beveiliging": 4, "Monitoring": 3, "Documentatie": 4, "BCM": 3,
        "Governance": 3, "Awareness": 1, "Cultuur": 1, "Externe borging": 3, "Normenkoppeling": 4,
    },
    "Scenario 3 — CISO-vacature MKB (degradatie)": {
        "SLA": 3, "Beveiliging": 3, "Monitoring": 2, "Documentatie": 3, "BCM": 3,
        "Governance": 3, "Awareness": 2, "Cultuur": 3, "Externe borging": 3, "Normenkoppeling": 3,
    },
    "Scenario 4 — Installatiebedrijf 110fte (drie-ordes)": {
        "SLA": 2, "Beveiliging": 2, "Monitoring": 1, "Documentatie": 2, "BCM": 2,
        "Governance": 2, "Awareness": 2, "Cultuur": 3, "Externe borging": 1, "Normenkoppeling": 1,
    },
    "Scenario 5 — TSC 2022 (externe-borging-dominant)": {
        "SLA": 3, "Beveiliging": 3, "Monitoring": 3, "Documentatie": 3, "BCM": 3,
        "Governance": 3, "Awareness": 3, "Cultuur": 3, "Externe borging": 1, "Normenkoppeling": 3,
    },
    "Scenario 6 — CrowdStrike 2024 (BCM-dominant)": {
        "SLA": 2, "Beveiliging": 3, "Monitoring": 2, "Documentatie": 3, "BCM": 1,
        "Governance": 3, "Awareness": 3, "Cultuur": 3, "Externe borging": 3, "Normenkoppeling": 3,
    },
}

# ──────────────────────────────────────────────────────────────
# Pagina-configuratie
# ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Ketenpunt Maturitymodel", layout="wide",
                   initial_sidebar_state="expanded")

st.title("Ketenpunt Maturitymodel")
st.caption("Beheersen van risico's derde diensten op het ketenpunt — "
           "interactieve proof-of-concept")

# ──────────────────────────────────────────────────────────────
# Sidebar: invoer maturityscores
# ──────────────────────────────────────────────────────────────
st.sidebar.header("Maturityscores")
st.sidebar.caption("Stel per domein de volwassenheid in (1 = ad hoc, 5 = geborgd), "
                   "of gebruik de tab 'Uitvraag' om scores te bepalen.")

# Scenario-selector
scenario_keuze = st.sidebar.selectbox(
    "Laad een voorbeeldscenario", ["(handmatig)"] + list(SCENARIOS.keys()),
    key="scenario_select")

# Bepaal default-bron: scenario > uitvraag > handmatig (3)
def bepaal_defaults():
    if scenario_keuze != "(handmatig)":
        return dict(SCENARIOS[scenario_keuze])
    if "uitvraag_scores" in st.session_state:
        return dict(st.session_state["uitvraag_scores"])
    return {d: 3 for d in DOMAINS}

defaults = bepaal_defaults()

# Slider-keys baseren op de actieve bron, zodat ze meeveranderen
bron_id = scenario_keuze
if scenario_keuze == "(handmatig)" and "uitvraag_scores" in st.session_state:
    bron_id = "uitvraag_" + str(st.session_state.get("uitvraag_versie", 0))

scores = {}
for laag, titel in [(1, "Laag 1 — Modifiers"),
                    (2, "Laag 2 — Operationele praktijken"),
                    (3, "Laag 3 — Implementaties")]:
    st.sidebar.subheader(titel)
    for d in DOMAINS:
        if LAGEN[d] == laag:
            scores[d] = st.sidebar.slider(
                d, 1, 5, int(defaults.get(d, 3)),
                key=f"slider_{d}_{bron_id}")

# ──────────────────────────────────────────────────────────────
# Tabs
# ──────────────────────────────────────────────────────────────
tab_uitvraag, tab1, tab2, tab3, tab4, tab_advies, tab_pad = st.tabs(
    ["Uitvraag", "Maturityprofiel", "Dwarsverbandenmatrix",
     "Prioritering", "Getypeerde graaf", "Advies & stappenplan",
     "Verbeterpad"])

# ── Tab Uitvraag ──────────────────────────────────────────────
with tab_uitvraag:
    st.subheader("Uitvraag: waar staat de organisatie nu?")
    st.write("Kies per domein de beschrijving die het best past bij de "
             "huidige situatie. Dit bepaalt de maturityscore. Klik onderaan "
             "op **Scores toepassen** om door te zetten naar de andere tabs.")
    st.caption("Tip: kies op operationeel niveau wat je herkent. Het "
               "stappenplan laat daarna zien wat er nodig is om een niveau "
               "te stijgen — en welke onderliggende domeinen moeten meegroeien.")

    uitvraag_antwoorden = {}
    for laag, titel in [(1, "Laag 1 — Modifiers (governance en cultuur)"),
                        (2, "Laag 2 — Operationele praktijken"),
                        (3, "Laag 3 — Implementaties")]:
        st.markdown(f"### {titel}")
        for d in DOMAINS:
            if LAGEN[d] == laag:
                opties = [NIVEAUS[d][n] for n in range(1, 6)]
                gekozen = st.radio(
                    f"**{d}**", opties, index=2, key=f"radio_{d}")
                # Map terug naar niveau
                niveau = opties.index(gekozen) + 1
                uitvraag_antwoorden[d] = niveau

    st.divider()
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Scores toepassen", type="primary"):
            st.session_state["uitvraag_scores"] = uitvraag_antwoorden
            st.session_state["uitvraag_versie"] = \
                st.session_state.get("uitvraag_versie", 0) + 1
            st.success("Scores toegepast — bekijk de andere tabs.")
            st.rerun()
    with col2:
        if st.button("Reset uitvraag"):
            for d in DOMAINS:
                st.session_state.pop(f"radio_{d}", None)
            st.session_state.pop("uitvraag_scores", None)
            st.rerun()

    if "uitvraag_scores" in st.session_state:
        st.info("Er zijn uitvraag-scores actief. Kies in de zijbalk een "
                "voorbeeldscenario om deze te overschrijven, of pas de "
                "sliders handmatig aan.")

# ── Tab 1: Radarprofiel ───────────────────────────────────────
with tab1:
    st.subheader("Maturityprofiel")
    st.write("Het radardiagram toont de volwassenheid per domein. "
             "Domeinen dicht bij het centrum vragen aandacht.")

    radar_vals = [scores[d] for d in DOMAINS] + [scores[DOMAINS[0]]]
    radar_labels = DOMAINS + [DOMAINS[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=radar_vals, theta=radar_labels, fill="toself",
        line_color="#1f4e8c", name="Maturity"))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        showlegend=False, height=500)
    st.plotly_chart(fig, width="stretch")

    gem = sum(scores.values()) / len(scores)
    col1, col2, col3 = st.columns(3)
    col1.metric("Gemiddelde maturity", f"{gem:.1f} / 5")
    laagst = min(scores, key=scores.get)
    col2.metric("Laagste domein", laagst, f"score {scores[laagst]}")
    hoogst = max(scores, key=scores.get)
    col3.metric("Hoogste domein", hoogst, f"score {scores[hoogst]}")

# ── Tab 2: Dwarsverbandenmatrix ───────────────────────────────
with tab2:
    st.subheader("Dwarsverbandenmatrix")
    st.write("Elke cel toont de sterkte (kleur) en het relatietype (letter) "
             "waarmee het rij-domein het kolom-domein beïnvloedt.")

    # Bouw heatmap z-waarden (score) en annotaties (type)
    z = []
    annot = []
    for r in range(10):
        zrow = []
        arow = []
        for c in range(10):
            cell = MATRIX[r][c]
            if cell is None:
                zrow.append(None)
                arow.append("")
            else:
                zrow.append(cell["score"])
                arow.append(f"{cell['score']}{cell['type']}")
        z.append(zrow)
        annot.append(arow)

    fig = go.Figure(data=go.Heatmap(
        z=z, x=DOMAINS, y=DOMAINS, colorscale="Blues",
        zmin=0, zmax=10, showscale=True,
        hoverongaps=False,
        colorbar=dict(title="Sterkte")))

    # Annotaties
    for r in range(10):
        for c in range(10):
            if annot[r][c]:
                cell = MATRIX[r][c]
                txt_color = "white" if cell["score"] >= 6 else "black"
                fig.add_annotation(
                    x=DOMAINS[c], y=DOMAINS[r], text=annot[r][c],
                    showarrow=False, font=dict(color=txt_color, size=10))

    fig.update_layout(height=650, xaxis_title="Doel-domein (kolom)",
                      yaxis_title="Bron-domein (rij)",
                      yaxis_autorange="reversed")
    st.plotly_chart(fig, width="stretch")

    # Legenda relatietypen
    st.write("**Relatietypen**")
    cols = st.columns(6)
    for i, (t, naam) in enumerate(TYPE_NAMES.items()):
        cols[i].markdown(
            f"<span style='color:{TYPE_COLORS[t]};font-weight:bold'>"
            f"{t}</span> — {naam} (max {PLAFONDS[t]})",
            unsafe_allow_html=True)

# ── Tab 3: Prioritering ───────────────────────────────────────
with tab3:
    st.subheader("Verbeterprioriteiten")
    st.write("Prioriteit = hefboomwaarde × maturity-gap. "
             "De hefboomwaarde geeft aan hoeveel andere domeinen "
             "een domein structureel beïnvloedt.")

    prioriteiten = []
    for d in DOMAINS:
        gap = 5 - scores[d]
        prio = HEFBOOM[d] * gap
        prioriteiten.append({
            "Domein": d, "Laag": LAGEN[d], "Score": scores[d],
            "Gap": gap, "Hefboom": HEFBOOM[d], "Prioriteit": prio})

    prioriteiten.sort(key=lambda x: x["Prioriteit"], reverse=True)

    # Barchart
    fig = go.Figure()
    laag_kleur = {1: "#c0392b", 2: "#e8861e", 3: "#f1c40f"}
    fig.add_trace(go.Bar(
        x=[p["Prioriteit"] for p in prioriteiten],
        y=[p["Domein"] for p in prioriteiten],
        orientation="h",
        marker_color=[laag_kleur[p["Laag"]] for p in prioriteiten],
        text=[f"{p['Prioriteit']}" for p in prioriteiten],
        textposition="auto"))
    fig.update_layout(height=450, xaxis_title="Prioriteit (hefboom × gap)",
                      yaxis_autorange="reversed")
    st.plotly_chart(fig, width="stretch")

    st.caption("Kleur = laag. Rood = Laag 1 (modifiers), oranje = Laag 2, "
               "geel = Laag 3. Laag 1 conditioneert de andere lagen: "
               "verbeter modifiers eerst.")

    # Top-3 met laag-randvoorwaarde
    st.write("**Top-3 verbeterprioriteiten**")
    top3 = prioriteiten[:3]
    for i, p in enumerate(top3, 1):
        rand = ""
        if p["Laag"] != 1:
            laag1_zwak = [d for d in DOMAINS if LAGEN[d] == 1 and scores[d] < 3]
            if laag1_zwak:
                rand = (f" ⚠ Let op: Laag 1 ({', '.join(laag1_zwak)}) is nog "
                        f"onvolwassen — verbeter modifiers eerst voor duurzaam effect.")
        st.markdown(
            f"**{i}. {p['Domein']}** (Laag {p['Laag']}) — "
            f"prioriteit {p['Prioriteit']} = hefboom {p['Hefboom']} × gap {p['Gap']}.{rand}")

    # Volledige tabel
    with st.expander("Volledige prioriteringstabel"):
        st.dataframe(prioriteiten, width="stretch", hide_index=True)

# ── Tab 4: Getypeerde graaf ───────────────────────────────────
with tab4:
    st.subheader("Getypeerde graaf")
    st.write("De graaf toont de domeinen in drie lagen. "
             "Pijlkleur = relatietype, knoopgrootte = maturity-gap. "
             "Alleen relaties met sterkte ≥ drempel worden getoond.")

    drempel = st.slider("Minimale relatiesterkte om te tonen", 0, 9, 6)
    toon_types = st.multiselect(
        "Toon relatietypen", list(TYPE_NAMES.keys()),
        default=list(TYPE_NAMES.keys()))

    # Layout: x = laag, y = positie binnen laag
    laag_y = {1: [], 2: [], 3: []}
    for d in DOMAINS:
        laag_y[LAGEN[d]].append(d)

    pos = {}
    laag_x = {1: 0, 2: 1, 3: 2}
    for laag, doms in laag_y.items():
        n = len(doms)
        for i, d in enumerate(doms):
            y = (i - (n - 1) / 2)
            pos[d] = (laag_x[laag], y)

    # Edges per type
    edge_traces = []
    for r in range(10):
        for c in range(10):
            cell = MATRIX[r][c]
            if cell is None:
                continue
            if cell["score"] < drempel:
                continue
            if cell["type"] not in toon_types:
                continue
            src, dst = DOMAINS[r], DOMAINS[c]
            x0, y0 = pos[src]
            x1, y1 = pos[dst]
            edge_traces.append(go.Scatter(
                x=[x0, x1, None], y=[y0, y1, None],
                mode="lines",
                line=dict(width=cell["score"] / 3,
                          color=TYPE_COLORS[cell["type"]]),
                hoverinfo="text",
                text=f"{src} → {dst}: {cell['score']}{cell['type']}",
                showlegend=False))

    # Nodes
    node_x = [pos[d][0] for d in DOMAINS]
    node_y = [pos[d][1] for d in DOMAINS]
    node_size = [15 + (5 - scores[d]) * 8 for d in DOMAINS]
    node_color = {1: "#c0392b", 2: "#e8861e", 3: "#f1c40f"}
    node_colors = [node_color[LAGEN[d]] for d in DOMAINS]

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        marker=dict(size=node_size, color=node_colors,
                    line=dict(width=2, color="white")),
        text=DOMAINS, textposition="middle right",
        hovertext=[f"{d}<br>Laag {LAGEN[d]}<br>Score {scores[d]}<br>"
                   f"Hefboom {HEFBOOM[d]}" for d in DOMAINS],
        hoverinfo="text", showlegend=False)

    fig = go.Figure(data=edge_traces + [node_trace])
    fig.update_layout(
        height=600, xaxis=dict(showgrid=False, zeroline=False,
                               showticklabels=True,
                               tickvals=[0, 1, 2],
                               ticktext=["Laag 1<br>Modifiers",
                                         "Laag 2<br>Praktijken",
                                         "Laag 3<br>Implementaties"]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="white")
    st.plotly_chart(fig, width="stretch")

    # Type-legenda
    st.write("**Relatietypen (pijlkleur)**")
    cols = st.columns(6)
    for i, (t, naam) in enumerate(TYPE_NAMES.items()):
        cols[i].markdown(
            f"<span style='color:{TYPE_COLORS[t]};font-weight:bold'>"
            f"━━ {t}</span><br><small>{naam}</small>",
            unsafe_allow_html=True)

# ── Tab Advies & stappenplan ──────────────────────────────────
with tab_advies:
    st.subheader("Advies & stappenplan")
    st.write("Kies hieronder welk domein je wilt verbeteren. Het stappenplan "
             "toont de concrete maatregel én — cruciaal — welke onderliggende "
             "domeinen (Laag 1 en 2) moeten meegroeien om de verbetering "
             "**bestendig** te maken.")

    # Domeinen met een gap, gesorteerd op prioriteit
    met_gap = []
    for d in DOMAINS:
        gap = 5 - scores[d]
        if gap > 0:
            met_gap.append((d, gap, HEFBOOM[d] * gap))
    met_gap.sort(key=lambda x: x[2], reverse=True)

    if not met_gap:
        st.success("Alle domeinen scoren maximaal. Focus op borging en "
                   "continue verbetering (PDCA).")
    else:
        # Keuze: welk domein verbeteren
        keuze_map = {f"{d} (score {scores[d]} → {scores[d]+1}, prioriteit {prio})": d
                     for d, gap, prio in met_gap}
        keuze_label = st.selectbox(
            "Welk domein wil je verbeteren?",
            list(keuze_map.keys()), key="verbeter_select")
        gekozen_domein = keuze_map[keuze_label]

        st.divider()

        # ── De gekozen maatregel ──
        m = MAATREGELEN[gekozen_domein]
        st.markdown(f"## {gekozen_domein} verbeteren")
        st.markdown(f"**Huidige situatie:** {NIVEAUS[gekozen_domein][scores[gekozen_domein]]}")
        st.markdown(f"**Streefniveau:** {NIVEAUS[gekozen_domein][min(scores[gekozen_domein]+1,5)]}")

        st.markdown("### Concrete maatregel")
        st.info(m["maatregel"])
        st.markdown("**Stappen:**")
        for i, stap in enumerate(m["stappen"], 1):
            st.markdown(f"{i}. {stap}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Doorlooptijd", m["doorlooptijd"])
        c2.markdown("**Verwacht effect**")
        c2.caption(m["effect"])
        c3.markdown("**Gekoppelde norm**")
        c3.caption(m["norm"])

        st.divider()

        # ── Cascade: wat moet meegroeien? (interactief afvinken) ──
        st.markdown("### Bestendigheid: het fundament moet meegroeien")

        # Mechanisme-uitleg
        st.markdown(f"**Waarom dit telt.** {m['terugval']}")
        with st.expander("Voorbeeld van terugval"):
            st.markdown(f"_{m['voorbeeld']}_")

        afhankelijk = AFHANKELIJK_VAN.get(gekozen_domein, [])
        streep = scores[gekozen_domein] + 1  # streefniveau (één hoger)

        # Bepaal blokkerende vs verzwakkende domeinen
        # Rood (blokkeert): score 2+ onder streefniveau
        # Oranje (verzwakt): score 1 onder of gelijk aan streefniveau
        # Voldoende: score >= streefniveau
        blokkeert = []
        verzwakt = []
        voldoende = []
        for a in afhankelijk:
            verschil = streep - scores[a]
            if verschil >= 2:
                blokkeert.append(a)
            elif verschil >= 0:
                verzwakt.append(a)
            else:
                voldoende.append(a)

        te_doen = blokkeert + verzwakt  # domeinen die aandacht nodig hebben

        if not afhankelijk:
            st.success(f"{gekozen_domein} is een fundament-domein (Laag "
                       f"{LAGEN[gekozen_domein]}) en hangt niet af van "
                       f"onderliggende domeinen. Verbetering hier versterkt "
                       f"juist de hele keten en is de meest bestendige "
                       f"investering.")
        elif not te_doen:
            st.success(
                f"De onderliggende domeinen ({', '.join(afhankelijk)}) zijn "
                f"al voldoende op niveau. {gekozen_domein} kan direct zijn "
                f"volwassenheidsstap maken.")
        else:
            st.warning(
                f"**{gekozen_domein} kan nog geen volwassenheidsstap maken.** "
                f"Eerst moeten de onderliggende domeinen hieronder op niveau "
                f"komen. Vink per domein de stappen af.")

            # Helper: unieke session-key per (bovenliggend, onderliggend, stap)
            def stap_key(boven, onder, idx):
                return f"chk_{boven}_{onder}_{idx}"

            # Toon blokkerende (rood) eerst, dan verzwakkende (oranje)
            gereed_status = {}
            for groep, kleur_emoji, kleur_label, kleur_hex in [
                    (blokkeert, "🔴", "BLOKKEERT", "#c0392b"),
                    (verzwakt, "🟠", "VERZWAKT", "#e8861e")]:
                for a in groep:
                    am = MAATREGELEN[a]
                    n_stappen = len(am["stappen"])
                    # Tel afgevinkte stappen
                    afgevinkt = sum(
                        1 for i in range(n_stappen)
                        if st.session_state.get(stap_key(gekozen_domein, a, i), False))
                    is_gereed = (afgevinkt == n_stappen)
                    gereed_status[a] = is_gereed

                    status_emoji = "✅" if is_gereed else kleur_emoji
                    laag_lbl = ("Laag 1 — fundament" if LAGEN[a] == 1
                                else "Laag 2 — operationeel")
                    titel = (f"{status_emoji} **{a}** — {laag_lbl} — "
                             f"score {scores[a]} — {kleur_label} "
                             f"({afgevinkt}/{n_stappen} stappen)")

                    with st.expander(titel, expanded=not is_gereed):
                        st.markdown(
                            f"<span style='color:{kleur_hex}'>"
                            f"**Status: {kleur_label}**</span> — "
                            f"{'blokkeert' if kleur_label=='BLOKKEERT' else 'verzwakt'} "
                            f"de verbetering van {gekozen_domein}.",
                            unsafe_allow_html=True)
                        st.markdown(f"**Doel:** {am['maatregel']}")
                        st.caption(f"⏱ {am['doorlooptijd']}  |  📋 {am['norm']}")

                        st.markdown("**Stappen — vink af wat gedaan is:**")
                        for i, stap in enumerate(am["stappen"]):
                            st.checkbox(
                                stap, key=stap_key(gekozen_domein, a, i))
                            # Uitleg per stap (inline; geen geneste expander)
                            u = STAP_UITLEG.get(a, {}).get(i)
                            if u:
                                st.caption(f"**Hoe pak ik stap {i+1} aan?**")
                                st.markdown(f"**Aanpak.** {u['hoe']}")
                                st.markdown("**Concrete deelacties:**")
                                for da in u["deelacties"]:
                                    st.markdown(f"- {da}")
                                st.markdown(f"**Wie betrekken:** {u['wie']}")
                                st.markdown(f"**Veelgemaakte valkuil:** {u['valkuil']}")
                                st.markdown(f"**Zo ziet 'klaar' eruit:** {u['resultaat']}")
                                st.caption(f"📋 Norm/bron: {u['norm']}")

                        # Voortgangsbalk
                        nieuw_afgevinkt = sum(
                            1 for i in range(n_stappen)
                            if st.session_state.get(stap_key(gekozen_domein, a, i), False))
                        st.progress(nieuw_afgevinkt / n_stappen,
                                    text=f"{nieuw_afgevinkt}/{n_stappen} stappen gereed")
                        if nieuw_afgevinkt == n_stappen:
                            st.success(f"{a} is gereed — fundament op niveau.")
                        else:
                            st.caption(f"⚠ Zonder afronding: {am['terugval']}")

            st.divider()

            # Gereedheid van het bovenliggende domein
            # Herbereken na alle checkboxes
            alle_gereed = all(
                all(st.session_state.get(stap_key(gekozen_domein, a, i), False)
                    for i in range(len(MAATREGELEN[a]["stappen"])))
                for a in te_doen)

            n_gereed = sum(1 for a in te_doen
                           if all(st.session_state.get(stap_key(gekozen_domein, a, i), False)
                                  for i in range(len(MAATREGELEN[a]["stappen"]))))
            st.progress(n_gereed / len(te_doen),
                        text=f"Fundament gereed: {n_gereed}/{len(te_doen)} domeinen")

            if alle_gereed:
                st.success(
                    f"✅ Alle onderliggende domeinen zijn gereed. "
                    f"**{gekozen_domein} is nu klaar om zijn volwassenheidsstap "
                    f"te maken** (score {scores[gekozen_domein]} → "
                    f"{min(scores[gekozen_domein]+1,5)}).")
                st.markdown(f"### Volwassenheidsstap: {gekozen_domein}")
                st.info(m["maatregel"])
                st.markdown("**Stappen — met uitleg:**")
                for i, stap in enumerate(m["stappen"]):
                    st.markdown(f"{i+1}. {stap}")
                    u = STAP_UITLEG.get(gekozen_domein, {}).get(i)
                    if u:
                        with st.expander(f"Hoe pak ik stap {i+1} aan?"):
                            st.markdown(f"**Aanpak.** {u['hoe']}")
                            st.markdown("**Concrete deelacties:**")
                            for da in u["deelacties"]:
                                st.markdown(f"- {da}")
                            st.markdown(f"**Wie betrekken:** {u['wie']}")
                            st.markdown(f"**Veelgemaakte valkuil:** {u['valkuil']}")
                            st.markdown(f"**Zo ziet 'klaar' eruit:** {u['resultaat']}")
                            st.caption(f"📋 Norm/bron: {u['norm']}")
                st.caption(f"⏱ {m['doorlooptijd']}  |  📋 {m['norm']}")
            else:
                st.error(
                    f"🔒 **{gekozen_domein} kan nog geen volwassenheidsstap "
                    f"maken.** Rond eerst de stappen van de onderliggende "
                    f"domeinen af (rood = blokkeert, oranje = verzwakt). "
                    f"Pas als alle fundamenten groen zijn, landt de verbetering "
                    f"van {gekozen_domein} duurzaam.")

    st.divider()

    # PDCA-kader
    st.markdown("### PDCA-cyclus")
    pcol1, pcol2, pcol3, pcol4 = st.columns(4)
    with pcol1:
        st.markdown("**Plan**")
        st.caption("Bepaal verbeterprioriteiten via hefboom × gap. "
                   "Start bij Laag 1.")
    with pcol2:
        st.markdown("**Do**")
        st.caption("Voer de maatregelen gefaseerd uit, "
                   "respecteer laag-volgorde.")
    with pcol3:
        st.markdown("**Check**")
        st.caption("Hermeet maturity na de interventie. "
                   "Is de gap gedicht?")
    with pcol4:
        st.markdown("**Act**")
        st.caption("Borg verbeteringen, stel bij en herhaal "
                   "de cyclus periodiek.")

# ── Tab Verbeterpad ───────────────────────────────────────────
with tab_pad:
    st.subheader("Verbeterpad: wat moet er allemaal meebewegen?")
    st.write(
        "Kies één domein dat je naar een hoger niveau wilt brengen. Het "
        "verbeterpad toont dan de **volledige onderliggende keten** — niet "
        "alleen de directe afhankelijkheden, maar ook de domeinen daaronder — "
        "en het niveau waarnaar elk domein moet meegroeien. De volgorde is "
        "fundament eerst (Laag 1 → 2 → 3), zodat je van onderaf opbouwt.")

    col_a, col_b = st.columns([3, 2])
    with col_a:
        doel_domein = st.selectbox(
            "Welk domein wil je verhogen?", DOMAINS, key="pad_domein")
    huidig = scores[doel_domein]
    with col_b:
        if huidig >= 5:
            st.info(f"{doel_domein} staat al op het maximum (niveau 5).")
            streef = 5
        else:
            streef = st.slider(
                "Naar welk niveau?", huidig + 1, 5, min(huidig + 2, 5),
                key="pad_streef")

    st.caption(
        "Aanname in dit pad: een ondersteunend domein moet minimaal op "
        "hetzelfde streefniveau staan als het domein dat het draagt. Een "
        "domein kan immers niet bestendig hoger zijn dan zijn fundament. "
        "Dit volgt de cascaderegel uit het model (type-M/A relaties, "
        "score >= 5); het streefniveau is instelbaar om scenario's te "
        "verkennen.")

    if huidig >= 5:
        st.success(f"{doel_domein} is al maximaal volwassen — geen verbeterpad nodig.")
    else:
        keten = keten_omhoog(doel_domein)

        # Opbouwvolgorde: fundament eerst (laag oplopend), dan op naam.
        # Het doeldomein zelf komt als laatste stap.
        onder = sorted(keten, key=lambda d: (LAGEN[d], d))
        pad = onder + [doel_domein]

        # Wat moet bewegen vs. wat staat al goed?
        moet_omhoog = [d for d in pad if scores[d] < streef]
        al_goed = [d for d in onder if scores[d] >= streef]

        st.markdown(f"## {doel_domein}: niveau {huidig} -> {streef}")

        if not onder:
            st.success(
                f"{doel_domein} is een Laag {LAGEN[doel_domein]}-fundament en "
                f"hangt niet af van onderliggende domeinen. Je kunt het direct "
                f"verhogen; het versterkt juist de hele keten eronder.")
        else:
            n_mee = len([d for d in onder if scores[d] < streef])
            st.markdown(
                f"Om **{doel_domein}** bestendig naar niveau **{streef}** te "
                f"brengen, hangt het via de keten af van **{len(onder)}** "
                f"onderliggende domeinen. Daarvan staan er **{n_mee}** nog te "
                f"laag en moeten meegroeien naar niveau {streef}.")

        st.markdown("### Opbouwvolgorde met stappen (fundament eerst)")
        st.caption(
            "🟢 = staat al op streefniveau · 🔼 = moet omhoog · "
            "🎯 = het domein dat je wilt verhogen. Klap een domein open "
            "voor de concrete maatregel en stappen.")

        laag_lbl = {1: "Laag 1 — fundament", 2: "Laag 2 — operationeel",
                    3: "Laag 3 — implementatie"}

        for i, d in enumerate(pad, 1):
            is_doel = (d == doel_domein)
            gap = streef - scores[d]
            if is_doel:
                emoji = "🎯"
            elif gap > 0:
                emoji = "🔼"
            else:
                emoji = "🟢"

            if gap > 0:
                stap_tekst = (f"niveau {scores[d]} -> {streef} "
                              f"({gap} {'stap' if gap == 1 else 'stappen'})")
            else:
                stap_tekst = f"niveau {scores[d]} — al op streefniveau"

            rol = "te verhogen domein" if is_doel else laag_lbl[LAGEN[d]]
            titel = f"{i}. {emoji} {d} — {rol} — {stap_tekst}"

            if gap > 0:
                # Domein moet bewegen: stappen tonen (doeldomein open).
                with st.expander(titel, expanded=is_doel):
                    if is_doel:
                        st.markdown(
                            f"Dit is het domein dat je wilt verhogen. "
                            f"Voer onderstaande stappen pas uit nadat de "
                            f"onderliggende domeinen hierboven op niveau "
                            f"{streef} staan.")
                    else:
                        st.markdown(
                            f"Fundament voor **{doel_domein}** — eerst op "
                            f"niveau {streef} brengen.")
                    render_stappen(d)
            else:
                # Al op niveau: geen actie, geen expander.
                st.markdown(f"**{titel}** — geen actie nodig.")

        st.divider()

        # Compacte planningstabel
        st.markdown("### Samengevat in een tabel")
        rijen = []
        for i, d in enumerate(pad, 1):
            gap = streef - scores[d]
            rijen.append({
                "Volgorde": i,
                "Domein": d + (" 🎯" if d == doel_domein else ""),
                "Laag": LAGEN[d],
                "Huidig": scores[d],
                "Vereist": streef,
                "Niveaustappen": gap if gap > 0 else 0,
                "Status": "al op niveau" if gap <= 0 else "moet omhoog",
            })
        st.dataframe(rijen, hide_index=True, use_container_width=True)

        totaal_stappen = sum(max(streef - scores[d], 0) for d in pad)
        st.info(
            f"**Totaal:** {len(moet_omhoog)} van de {len(pad)} domeinen in dit "
            f"pad moeten bewegen, samen {totaal_stappen} niveaustappen. "
            f"Begin bovenaan de lijst (de fundamenten) en werk naar beneden "
            f"naar {doel_domein}.")

        st.caption(
            "De stappen hierboven zijn ter overzicht. Wil je ze per domein "
            "afvinken met voortgangsbalk? Gebruik dan de tab "
            "**Advies & stappenplan**.")

st.divider()
st.caption("Proof-of-concept bij de afstudeerscriptie. De prioriteringsformule "
           "en hefboomwaarden volgen het model uit hoofdstuk 4; de getoonde "
           "maturityscores zijn invoer en kunnen vrij worden aangepast. "
           "Algoritmische verbeteroptimalisatie en parallellisering (bijlage G) "
           "zijn vervolgonderzoek.")
