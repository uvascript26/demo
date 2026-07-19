"""
Kennisbasis voor het ketenpunt-maturitymodel.

Bevat per domein:
- niveaus: vijf operationeel herkenbare beschrijvingen (maturity 1-5)
- maatregel: concrete verbeteractie om een niveau te stijgen
- effect: verwacht effect van de maatregel
- doorlooptijd: indicatieve tijd
- norm: gekoppelde norm/regelgeving
- afhankelijk_van: Laag 1/2 domeinen die moeten meegroeien (cascade)

De afhankelijkheden zijn afgeleid uit de dwarsverbandenmatrix (type-M en
type-A relaties naar dit domein).
"""

# Operationeel herkenbare niveaubeschrijvingen per domein (maturity 1-5)
NIVEAUS = {
    "Governance": {
        1: "Niemand is duidelijk eigenaar van de relaties met derde diensten; beslissingen ontstaan ad hoc.",
        2: "Eén persoon regelt het informeel, maar het is niet vastgelegd of belegd op directieniveau.",
        3: "Eigenaarschap is formeel toegewezen en beslissingen worden vastgelegd.",
        4: "Governance wordt periodiek geëvalueerd; rollen en mandaten zijn helder en gemeten.",
        5: "Governance is geborgd, wordt continu verbeterd en is onderdeel van de besturingscyclus.",
    },
    "Cultuur": {
        1: "Risico's worden niet besproken; 'we regelen het onderling wel' is de norm.",
        2: "Risico's komen soms ter sprake, maar leren van incidenten gebeurt niet structureel.",
        3: "Risico's zijn bespreekbaar en incidenten worden geëvalueerd.",
        4: "Er is een actieve leercultuur; afspraken worden als sturingsinstrument gezien.",
        5: "Risicobewustzijn is verankerd in gedrag op alle niveaus; double-loop leren is normaal.",
    },
    "Monitoring": {
        1: "Er is geen zicht op prestaties of beschikbaarheid van derde diensten.",
        2: "Monitoring gebeurt reactief, pas als er iets misgaat.",
        3: "Prestaties worden structureel gevolgd met vastgelegde KPI's.",
        4: "KPI's/KRI's worden geëvalueerd en gekoppeld aan actie.",
        5: "Monitoring is continu, geautomatiseerd en gekoppeld aan verbetercyclus.",
    },
    "BCM": {
        1: "Er is geen continuïteitsplan voor uitval van derde diensten.",
        2: "Er is een plan, maar leveranciersuitval is daarin niet uitgewerkt.",
        3: "Continuïteitsplan dekt leveranciersuitval; RTO/RPO zijn bepaald.",
        4: "Continuïteitsscenario's worden periodiek getest.",
        5: "BCM is geborgd, getest en continu verbeterd over de hele keten.",
    },
    "Awareness": {
        1: "Medewerkers weten niet welke derde diensten kritiek zijn.",
        2: "Sommige medewerkers zijn zich bewust, maar er is geen training.",
        3: "Er is structurele bewustwording en training over ketenrisico's.",
        4: "Awareness wordt gemeten en gericht bijgestuurd.",
        5: "Awareness is verankerd; medewerkers handelen proactief bij incidenten.",
    },
    "SLA": {
        1: "Er zijn geen of verouderde contracten met kritieke leveranciers.",
        2: "Er zijn contracten, maar zonder afspraken over wijziging, audit of exit.",
        3: "Contracten bevatten afspraken over wijziging, audit, herstel en exit.",
        4: "SLA's worden periodiek getoetst en geëvalueerd.",
        5: "Contractbeheer is geborgd en gekoppeld aan leveranciersmanagement.",
    },
    "Beveiliging": {
        1: "Koppelingen met derde diensten zijn technisch niet beveiligd ingericht.",
        2: "Basale maatregelen bestaan, maar zonder beheer van toegang of herziening.",
        3: "Toegang en koppelingen worden beheerd en herzien.",
        4: "Beveiligingsmaatregelen worden periodiek getest.",
        5: "Beveiliging is geborgd, gemonitord en continu bijgewerkt.",
    },
    "Documentatie": {
        1: "Processen en afspraken rond derde diensten zijn niet gedocumenteerd.",
        2: "Er is enige documentatie, maar verouderd of moeilijk vindbaar.",
        3: "Documentatie is actueel, vindbaar en gestructureerd.",
        4: "Documentatie wordt onderhouden en gebruikt voor verantwoording.",
        5: "Documentatie is geborgd en maakt ketenbeheersing aantoonbaar.",
    },
    "Externe borging": {
        1: "Er worden geen assurance-rapporten van leveranciers opgevraagd.",
        2: "Rapporten worden opgevraagd maar niet beoordeeld.",
        3: "Assurance-rapporten (SOC 2 / ISAE 3402) worden beoordeeld en opgevolgd.",
        4: "Borging is gekoppeld aan leveranciersbeoordeling en gemeten.",
        5: "Externe borging is geborgd en onderdeel van continu leveranciersbeheer.",
    },
    "Normenkoppeling": {
        1: "Het is onduidelijk welke regelgeving op de keten van toepassing is.",
        2: "Regelgeving is bekend, maar niet vertaald naar afspraken.",
        3: "Compliance-eisen zijn vertaald naar concrete afspraken met leveranciers.",
        4: "Naleving wordt periodiek getoetst en aantoonbaar gemaakt.",
        5: "Compliance is geborgd en continu gemonitord over de keten.",
    },
}

# Concrete maatregelen per domein: wat te doen om te stijgen
MAATREGELEN = {
    "Governance": {
        "maatregel": "Wijs een formele eigenaar aan voor ketenrelaties en leg het mandaat en de besluitvorming vast op directieniveau.",
        "stappen": [
            "Benoem één verantwoordelijke (rol, niet persoon) voor het beheer van derde diensten.",
            "Leg vast welke beslissingen op directieniveau worden genomen en welke gedelegeerd zijn.",
            "Stel een eenvoudig besluitvormingskader op (wie beslist waarover bij ketenrisico's).",
            "Veranker de rol in de reguliere overlegcyclus (bijv. kwartaalrapportage aan directie).",
        ],
        "effect": "Beslissingen over uitbesteding worden navolgbaar en consistent; verantwoordelijkheid is niet langer persoonsafhankelijk.",
        "doorlooptijd": "1-3 maanden",
        "norm": "COBIT 2019, ISO 27001 (A.5 leiderschap)",
        "terugval": "Zonder formeel belegd eigenaarschap vervallen verbeteringen elders zodra de betrokken persoon vertrekt of het druk krijgt. Governance is het anker: ontbreekt het, dan zakt elke andere verbetering terug naar persoonsafhankelijk handelen.",
        "voorbeeld": "Een MKB-organisatie richt prima monitoring in, maar omdat niemand formeel eigenaar is, stopt de opvolging zodra de initiatiefnemer met een ander project bezig is. Na een half jaar wordt niemand meer gealarmeerd door de dashboards.",
    },
    "Cultuur": {
        "maatregel": "Introduceer periodieke risicobesprekingen en incidentevaluaties (ook bijna-incidenten) waarin leren centraal staat.",
        "stappen": [
            "Plan een vast terugkerend moment om ketenrisico's en incidenten te bespreken.",
            "Bespreek ook bijna-incidenten, zonder schuldvraag (psychologische veiligheid).",
            "Leg geleerde lessen vast en koppel ze aan concrete acties.",
            "Laat de directie het goede voorbeeld geven door risico's serieus te nemen.",
        ],
        "effect": "Risico's worden bespreekbaar; de organisatie verschuift van brandjes blussen naar structureel leren (double-loop).",
        "doorlooptijd": "3-6 maanden (cultuurverandering)",
        "norm": "COSO 2013, Schein (organisatiecultuur), Argyris (double-loop leren)",
        "terugval": "Cultuur is de traagste maar diepste laag. Zonder een leercultuur worden formele maatregelen als bureaucratie ervaren en stilletjes genegeerd. De organisatie blijft single-loop reageren: incidenten worden geblust, maar onderliggende aannames niet herzien.",
        "voorbeeld": "Een organisatie voert na een incident netjes nieuwe procedures in, maar omdat 'we regelen het onderling wel' de norm blijft, worden de procedures binnen enkele maanden weer omzeild. Bij het volgende incident blijkt niets structureel veranderd.",
    },
    "Monitoring": {
        "maatregel": "Definieer KPI's/KRI's voor kritieke leveranciers en richt structurele monitoring en rapportage in.",
        "stappen": [
            "Inventariseer welke derde diensten kritiek zijn voor de bedrijfsvoering.",
            "Definieer per kritieke dienst meetbare KPI's/KRI's (beschikbaarheid, responstijd, incidenten).",
            "Richt een eenvoudige rapportage of dashboard in dat afwijkingen zichtbaar maakt.",
            "Koppel afwijkingen aan een opvolgproces (wie doet wat bij een alarm).",
        ],
        "effect": "Afwijkingen worden tijdig zichtbaar; prestaties van derde diensten zijn objectief te volgen.",
        "doorlooptijd": "2-4 maanden",
        "norm": "ISO 27001 (A.5.22), NIST SP 800-207",
        "terugval": "Monitoring zonder governance-eigenaar wordt een dashboard dat niemand bekijkt. Zonder cultuur van opvolging worden alarmen genegeerd. De techniek staat er, maar de organisatorische inbedding ontbreekt.",
        "voorbeeld": "Een dashboard meldt al weken verhoogde foutpercentages bij een SaaS-leverancier, maar omdat opvolging niet is belegd, onderneemt niemand actie tot de dienst volledig uitvalt.",
    },
    "BCM": {
        "maatregel": "Breid het continuïteitsplan uit met leveranciersuitval, bepaal RTO/RPO en plan periodieke tests.",
        "stappen": [
            "Identificeer welke processen stilvallen bij uitval van een kritieke leverancier.",
            "Bepaal per proces de hersteldoelstellingen (RTO/RPO).",
            "Werk concrete fallback-scenario's uit (handmatig proces, alternatieve leverancier).",
            "Test het scenario periodiek en evalueer de uitkomst.",
        ],
        "effect": "De organisatie kan een leveranciersuitval opvangen; hersteltijd en -verlies zijn beheerst.",
        "doorlooptijd": "3-6 maanden",
        "norm": "ISO 22301, DORA (operationele weerbaarheid)",
        "terugval": "Een continuïteitsplan dat niet wordt getest, is een papieren plan. Zonder een cultuur die tijd vrijmaakt voor tests en zonder governance die het afdwingt, veroudert het plan ongemerkt tot het bij een echte uitval niet blijkt te werken.",
        "voorbeeld": "Een organisatie heeft een BCP voor eigen IT-uitval, maar testte nooit het scenario 'onze beveiligingsleverancier valt zelf uit'. Bij de CrowdStrike-uitval in 2024 bleek er geen handelingsperspectief — het plan dekte de verkeerde dreiging.",
    },
    "Awareness": {
        "maatregel": "Richt training en bewustwording in over kritieke derde diensten en handelingsperspectief bij incidenten.",
        "stappen": [
            "Maak inzichtelijk welke derde diensten kritiek zijn voor welke teams.",
            "Geef gerichte voorlichting over de risico's en de eigen rol daarin.",
            "Oefen het handelingsperspectief bij uitval (wie bel je, wat doe je).",
            "Herhaal periodiek en sluit aan op actuele incidenten.",
        ],
        "effect": "Medewerkers herkennen ketenrisico's en weten te handelen bij uitval; de menselijke factor wordt sterker.",
        "doorlooptijd": "2-4 maanden",
        "norm": "ISO 27001 (A.6.3), NIS2 (awareness)",
        "terugval": "Eenmalige training zonder herhaling vervaagt snel. Zonder een cultuur die het belang ervan uitdraagt, zien medewerkers awareness als verplicht nummer en valt het kennisniveau terug naar nul bij personeelsverloop.",
        "voorbeeld": "Na een phishing-training daalt het aantal incidenten kortstondig, maar omdat er geen herhaling of cultuurverankering is, is het effect na een jaar volledig verdwenen en klikken nieuwe medewerkers net zo vaak.",
    },
    "SLA": {
        "maatregel": "Herzie contracten met kritieke leveranciers: voeg afspraken toe over change notification, auditrechten, herstel (RTO/RPO) en exit.",
        "stappen": [
            "Inventariseer de bestaande contracten met kritieke leveranciers.",
            "Identificeer de ontbrekende clausules (wijziging, audit, herstel, exit).",
            "Onderhandel aanvullende afspraken bij contractverlenging of -herziening.",
            "Leg vast hoe en wanneer SLA-naleving wordt getoetst.",
        ],
        "effect": "De organisatie kan leveranciers daadwerkelijk aansturen; het gat tussen verantwoordelijkheid en mogelijkheid wordt gedicht.",
        "doorlooptijd": "3-6 maanden (contractcyclus)",
        "norm": "EBA Guidelines, DORA (contractuele waarborgen), ISO 27001 (A.5.20)",
        "terugval": "Een scherp contract zonder monitoring op naleving en zonder eigenaar die erop stuurt, wordt een la-document. Bij een geschil blijkt dat niemand de afspraken heeft bijgehouden of afgedwongen.",
        "voorbeeld": "Een organisatie bedingt auditrechten in het contract, maar maakt er nooit gebruik van omdat niemand het beheer heeft belegd. Bij een datalek bij de leverancier blijkt er geen zicht op de beheersmaatregelen, ondanks het contractuele recht.",
    },
    "Beveiliging": {
        "maatregel": "Richt toegangsbeheer en technische beveiliging van koppelingen in volgens zero-trust-principes; plan periodieke tests.",
        "stappen": [
            "Breng de koppelingen met derde diensten en de bijbehorende toegangen in kaart.",
            "Pas least-privilege toe: alleen noodzakelijke toegang, expliciet geautoriseerd.",
            "Richt logging en monitoring op de koppelingen in.",
            "Test de beveiliging periodiek en herzie toegangsrechten.",
        ],
        "effect": "Koppelingen met derde diensten zijn beheerst; toegang wordt expliciet geautoriseerd en gemonitord.",
        "doorlooptijd": "3-6 maanden",
        "norm": "NIST SP 800-207, CIS Controls, ISO 27001 (A.8)",
        "terugval": "Toegangsrechten die eenmalig worden ingericht maar nooit herzien, groeien ongemerkt scheef (privilege creep). Zonder governance op periodieke herziening ontstaat na verloop van tijd weer een onbeheerst toegangslandschap.",
        "voorbeeld": "Een organisatie richt netjes toegangsbeheer in, maar omdat herziening niet is belegd, behouden vertrokken leveranciers en oud-medewerkers maandenlang actieve toegang tot kritieke koppelingen.",
    },
    "Documentatie": {
        "maatregel": "Documenteer processen, afspraken en bewijsvoering rond derde diensten en houd deze actueel en vindbaar.",
        "stappen": [
            "Leg per kritieke derde dienst de belangrijkste processen en afspraken vast.",
            "Bepaal waar documentatie wordt bewaard en wie haar onderhoudt.",
            "Koppel documentatie aan wijzigingen (update bij elke contract- of proceswijziging).",
            "Maak documentatie vindbaar voor wie haar nodig heeft.",
        ],
        "effect": "Ketenbeheersing wordt aantoonbaar; vormt de bewijsbasis voor externe borging en compliance.",
        "doorlooptijd": "2-4 maanden",
        "norm": "ISO 27001 (gedocumenteerde informatie), EBA (uitbestedingsregister)",
        "terugval": "Documentatie die niet wordt onderhouden, veroudert sneller dan ze wordt gemaakt. Zonder een proces dat updates afdwingt bij wijzigingen, is de documentatie binnen een jaar onbetrouwbaar en daarmee waardeloos als bewijsbasis.",
        "voorbeeld": "Een organisatie documenteert haar processen voor een audit, maar omdat onderhoud niet is belegd, wijkt de documentatie na een jaar zo sterk af van de praktijk dat de volgende audit erop afketst.",
    },
    "Externe borging": {
        "maatregel": "Vraag assurance-rapporten (SOC 2 / ISAE 3402) op bij kritieke leveranciers en beoordeel en volg deze actief op.",
        "stappen": [
            "Bepaal van welke kritieke leveranciers assurance-rapporten beschikbaar zijn.",
            "Vraag de rapporten op en beoordeel ze inhoudelijk (niet alleen archiveren).",
            "Toets de uitzonderingen en bevindingen tegen de eigen risico's.",
            "Volg tekortkomingen actief op bij de leverancier.",
        ],
        "effect": "Zicht op beheersmaatregelen bij leveranciers; afwijkingen worden zichtbaar en opvolgbaar.",
        "doorlooptijd": "2-4 maanden",
        "norm": "ISAE 3402 / SOC 2, DORA (toezicht op derden)",
        "terugval": "Een assurance-rapport opvragen en ongelezen archiveren geeft schijnzekerheid. Zonder documentatie van de eigen processen (type-S) kun je de bevindingen niet eens tegen je eigen situatie toetsen.",
        "voorbeeld": "Een organisatie verzamelt netjes ISAE 3402-rapporten van leveranciers, maar leest ze niet. Een rapport vermeldt een belangrijke uitzondering in de back-upcontrole; die blijft onopgemerkt tot een leverancier data verliest.",
    },
    "Normenkoppeling": {
        "maatregel": "Breng van toepassing zijnde regelgeving (AVG, NIS2, DORA) in kaart en vertaal naar concrete afspraken en toetsing.",
        "stappen": [
            "Bepaal welke regelgeving van toepassing is op de organisatie en haar keten.",
            "Vertaal de eisen naar concrete afspraken met leveranciers (in SLA's).",
            "Leg vast hoe naleving wordt aangetoond en getoetst.",
            "Toets periodiek en actualiseer bij nieuwe regelgeving.",
        ],
        "effect": "Compliance is geen papieren oefening meer; eisen zijn verankerd in de keten en toetsbaar.",
        "doorlooptijd": "3-6 maanden",
        "norm": "AVG, NIS2, DORA",
        "terugval": "Compliance zonder onderliggende SLA-afspraken (type-S) en documentatie is een papieren claim. Bij een toezichtsonderzoek blijkt de naleving niet aantoonbaar omdat de contractuele en gedocumenteerde basis ontbreekt.",
        "voorbeeld": "Een organisatie verklaart NIS2-compliant te zijn, maar omdat de eisen niet in de leverancierscontracten zijn verankerd, kan zij bij een incident niet aantonen dat de leverancier aan de eisen voldeed.",
    },
}
