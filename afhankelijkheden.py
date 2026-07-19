"""Cascade-afhankelijkheden afgeleid uit de dwarsverbandenmatrix.
Per domein: welke lagere-laag domeinen moeten meegroeien (type-M/A, score>=5)."""

AFHANKELIJK_VAN = {
    "SLA": [
        "Monitoring",
        "BCM",
        "Governance",
        "Awareness",
        "Cultuur"
    ],
    "Beveiliging": [
        "Monitoring",
        "BCM",
        "Governance",
        "Awareness",
        "Cultuur"
    ],
    "Monitoring": [
        "Governance",
        "Cultuur"
    ],
    "Documentatie": [
        "Monitoring",
        "BCM",
        "Governance",
        "Awareness",
        "Cultuur"
    ],
    "BCM": [
        "Governance",
        "Cultuur"
    ],
    "Governance": [],
    "Awareness": [
        "Governance",
        "Cultuur"
    ],
    "Cultuur": [],
    "Externe borging": [
        "Monitoring",
        "BCM"
    ],
    "Normenkoppeling": [
        "Monitoring",
        "BCM",
        "Governance",
        "Awareness",
        "Cultuur"
    ]
}
