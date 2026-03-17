def organize_tips(scraped_data, plant_list):
    """
    Takes raw scraped data and plant list, returns tips
    organized by category then by plant.

    scraped_data format: {plant_name: {url: [tips]}}
    Returns: {category: [{plant info + tips + sources}]}
    """
    # Build a lookup from plant name to plant metadata
    plant_lookup = {p["name"]: p for p in plant_list}

    organized = {}

    for plant_name, sources in scraped_data.items():
        plant = plant_lookup.get(plant_name)
        if not plant:
            continue

        category = plant["category"]
        if category not in organized:
            organized[category] = []

        # Flatten all tips across sources, deduplicate
        all_tips = []
        source_urls = []
        seen = set()

        for url, tips in sources.items():
            source_urls.append(url)
            for tip in tips:
                # Simple dedup - skip if first 60 chars already seen
                key = tip[:60].lower().strip()
                if key not in seen:
                    seen.add(key)
                    all_tips.append(tip)

        organized[category].append({
            "name": plant_name,
            "native": plant["native"],
            "water": plant["water"],
            "days_to_maturity": plant["days_to_maturity"],
            "direct_sow": plant["direct_sow"],
            "notes": plant["notes"],
            "tips": all_tips[:8],  # Cap at 8 tips per plant
            "sources": source_urls,
        })

    return organized


def format_for_display(organized, zone, city, state, last_frost, first_frost):
    """
    Takes organized data and returns a formatted string
    ready for terminal display.
    """
    lines = []
    lines.append("=" * 60)
    lines.append(f"GARDEN ZONE FINDER")
    lines.append(f"Location : {city}, {state}")
    lines.append(f"Zone     : {zone}")
    lines.append(f"Last spring frost : {last_frost}")
    lines.append(f"First fall frost  : {first_frost}")
    lines.append("=" * 60)

    category_order = ["vegetable", "fruit", "flower"]
    category_labels = {
        "vegetable": "VEGETABLES",
        "fruit": "FRUITS",
        "flower": "FLOWERS",
    }

    for category in category_order:
        plants = organized.get(category, [])
        if not plants:
            continue

        lines.append(f"\n--- {category_labels[category]} ---")

        for plant in plants:
            native_tag = " [NATIVE]" if plant["native"] else ""
            lines.append(f"\n{plant['name']}{native_tag}")
            lines.append(f"  Water needs    : {plant['water']}")
            lines.append(f"  Days to mature : {plant['days_to_maturity']}")
            lines.append(f"  Direct sow     : {'Yes' if plant['direct_sow'] else 'No - start indoors'}")
            lines.append(f"  Notes          : {plant['notes']}")

            if plant["tips"]:
                lines.append("  Scraped tips:")
                for tip in plant["tips"]:
                    # Wrap long tips at 80 chars
                    wrapped = tip[:200] + "..." if len(tip) > 200 else tip
                    lines.append(f"    * {wrapped}")

            if plant["sources"]:
                lines.append("  Sources:")
                for url in plant["sources"]:
                    lines.append(f"    - {url}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)
