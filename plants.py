# Plant database for zones 5a through 9b
# native: True = native to the American Southwest/NM region
# water: low / medium / high
# days_to_maturity: approximate days from transplant (or seed where noted)

PLANTS = [
    # --- VEGETABLES ---
    {
        "name": "Green Chile Pepper",
        "category": "vegetable",
        "zones": ["6a","6b","7a","7b","8a","8b","9a","9b"],
        "native": True,
        "water": "medium",
        "days_to_maturity": 80,
        "notes": "Staple of NM cuisine. Start indoors 8 weeks before last frost.",
        "direct_sow": False,
        "weeks_before_frost": 8,
    },
    {
        "name": "Pinto Bean",
        "category": "vegetable",
        "zones": ["5a","5b","6a","6b","7a","7b","8a","8b"],
        "native": True,
        "water": "low",
        "days_to_maturity": 90,
        "notes": "Heat tolerant. Direct sow after last frost.",
        "direct_sow": True,
        "weeks_before_frost": 0,
    },
    {
        "name": "Tomato",
        "category": "vegetable",
        "zones": ["5a","5b","6a","6b","7a","7b","8a","8b","9a","9b"],
        "native": False,
        "water": "medium",
        "days_to_maturity": 70,
        "notes": "Start indoors 6-8 weeks before last frost. Mulch heavily in NM heat.",
        "direct_sow": False,
        "weeks_before_frost": 8,
    },
    {
        "name": "Zucchini",
        "category": "vegetable",
        "zones": ["5a","5b","6a","6b","7a","7b","8a","8b","9a","9b"],
        "native": False,
        "water": "medium",
        "days_to_maturity": 50,
        "notes": "Direct sow after last frost. Very productive in high desert.",
        "direct_sow": True,
        "weeks_before_frost": 0,
    },
    {
        "name": "Garlic",
        "category": "vegetable",
        "zones": ["5a","5b","6a","6b","7a","7b","8a","8b"],
        "native": False,
        "water": "low",
        "days_to_maturity": 240,
        "notes": "Plant cloves in fall (Oct-Nov) for summer harvest.",
        "direct_sow": True,
        "weeks_before_frost": 0,
    },
    {
        "name": "Kale",
        "category": "vegetable",
        "zones": ["5a","5b","6a","6b","7a","7b","8a","8b","9a","9b"],
        "native": False,
        "water": "medium",
        "days_to_maturity": 55,
        "notes": "Cold hardy. Can overwinter in zone 6b with light protection.",
        "direct_sow": True,
        "weeks_before_frost": 0,
    },
    {
        "name": "Corn (Heirloom Blue)",
        "category": "vegetable",
        "zones": ["6a","6b","7a","7b","8a","8b","9a","9b"],
        "native": True,
        "water": "medium",
        "days_to_maturity": 100,
        "notes": "Traditional Pueblo crop. Direct sow in blocks for pollination.",
        "direct_sow": True,
        "weeks_before_frost": 0,
    },
    {
        "name": "Squash (Cushaw)",
        "category": "vegetable",
        "zones": ["6a","6b","7a","7b","8a","8b","9a","9b"],
        "native": True,
        "water": "low",
        "days_to_maturity": 110,
        "notes": "Traditional NM crop. Extremely drought tolerant.",
        "direct_sow": True,
        "weeks_before_frost": 0,
    },

    # --- FRUITS ---
    {
        "name": "Prickly Pear Cactus",
        "category": "fruit",
        "zones": ["6a","6b","7a","7b","8a","8b","9a","9b"],
        "native": True,
        "water": "low",
        "days_to_maturity": 365,
        "notes": "Pads and fruit both edible. Extremely drought tolerant.",
        "direct_sow": False,
        "weeks_before_frost": 0,
    },
    {
        "name": "Apricot",
        "category": "fruit",
        "zones": ["5a","5b","6a","6b","7a","7b"],
        "native": False,
        "water": "low",
        "days_to_maturity": 1095,
        "notes": "Thrives in NM. Late frosts can damage blossoms - plant on a north slope.",
        "direct_sow": False,
        "weeks_before_frost": 0,
    },
    {
        "name": "Grape",
        "category": "fruit",
        "zones": ["6a","6b","7a","7b","8a","8b"],
        "native": False,
        "water": "low",
        "days_to_maturity": 1095,
        "notes": "NM has a long winemaking tradition. Well-draining alkaline soil is ideal.",
        "direct_sow": False,
        "weeks_before_frost": 0,
    },

    # --- FLOWERS ---
    {
        "name": "Desert Marigold",
        "category": "flower",
        "zones": ["6a","6b","7a","7b","8a","8b","9a","9b"],
        "native": True,
        "water": "low",
        "days_to_maturity": 60,
        "notes": "Bright yellow. Blooms spring through fall. Self-seeds readily.",
        "direct_sow": True,
        "weeks_before_frost": 0,
    },
    {
        "name": "Rocky Mountain Penstemon",
        "category": "flower",
        "zones": ["5a","5b","6a","6b","7a","7b"],
        "native": True,
        "water": "low",
        "days_to_maturity": 90,
        "notes": "Attracts hummingbirds. Very drought tolerant once established.",
        "direct_sow": False,
        "weeks_before_frost": 8,
    },
    {
        "name": "Zinnia",
        "category": "flower",
        "zones": ["5a","5b","6a","6b","7a","7b","8a","8b","9a","9b"],
        "native": False,
        "water": "low",
        "days_to_maturity": 60,
        "notes": "Thrives in heat. Direct sow after last frost. Great pollinator plant.",
        "direct_sow": True,
        "weeks_before_frost": 0,
    },
    {
        "name": "Apache Plume",
        "category": "flower",
        "zones": ["5a","5b","6a","6b","7a","7b","8a","8b"],
        "native": True,
        "water": "low",
        "days_to_maturity": 365,
        "notes": "Feathery seed heads after bloom. Excellent wildlife habitat.",
        "direct_sow": False,
        "weeks_before_frost": 0,
    },
    {
        "name": "Sunflower",
        "category": "flower",
        "zones": ["5a","5b","6a","6b","7a","7b","8a","8b","9a","9b"],
        "native": True,
        "water": "low",
        "days_to_maturity": 80,
        "notes": "Native to North America. Direct sow after last frost.",
        "direct_sow": True,
        "weeks_before_frost": 0,
    },
]

def get_plants_for_zone(zone):
    """Returns all plants compatible with the given zone."""
    return [p for p in PLANTS if zone in p["zones"]]

def group_by_category(plants):
    """Groups a list of plants into a dict by category."""
    grouped = {}
    for plant in plants:
        cat = plant["category"]
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(plant)
    return grouped
