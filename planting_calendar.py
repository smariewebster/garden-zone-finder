from datetime import datetime, timedelta

def parse_frost_date(date_str, year=None):
    """Convert 'Apr 15' style string to a datetime object."""
    if year is None:
        year = datetime.now().year
    return datetime.strptime(f"{date_str} {year}", "%b %d %Y")

def get_week_of(dt):
    """Return a 'Week of Mon DD' string for a given date."""
    # Round back to nearest Monday
    monday = dt - timedelta(days=dt.weekday())
    return monday.strftime("Week of %b %-d")

def is_frost_risk(action_date, last_frost, first_frost, window_days=14):
    """Returns True if action_date falls within window_days of either frost date."""
    last = parse_frost_date(last_frost)
    first = parse_frost_date(first_frost)
    return (
        abs((action_date - last).days) <= window_days or
        abs((action_date - first).days) <= window_days
    )

def build_plant_schedule(plant, last_frost_str, first_frost_str):
    """
    Builds a list of dated actions for a single plant.
    Returns a list of dicts: {week, action, warning}
    """
    last_frost = parse_frost_date(last_frost_str)
    first_frost = parse_frost_date(first_frost_str)
    schedule = []

    weeks_before = plant.get("weeks_before_frost", 0)
    direct_sow = plant["direct_sow"]
    dtm = plant["days_to_maturity"]

    # --- Garlic special case - fall planting ---
    if plant["name"] == "Garlic":
        plant_date = last_frost.replace(month=10, day=15)
        harvest_date = plant_date + timedelta(days=dtm)
        schedule.append({
            "date": plant_date,
            "week": get_week_of(plant_date),
            "action": "Plant cloves directly in ground",
            "warning": None,
        })
        schedule.append({
            "date": harvest_date,
            "week": get_week_of(harvest_date),
            "action": "Harvest when tops begin to yellow",
            "warning": None,
        })
        return schedule

    # --- Perennials / bare root plants (very long days to maturity) ---
    if dtm >= 365:
        # Trees, shrubs, perennials - plant after last frost
        plant_date = last_frost + timedelta(weeks=2)
        schedule.append({
            "date": plant_date,
            "week": get_week_of(plant_date),
            "action": "Plant bare root / container / pad in ground",
            "warning": None,
        })
        schedule.append({
            "date": plant_date + timedelta(weeks=4),
            "week": get_week_of(plant_date + timedelta(weeks=4)),
            "action": "Establish watering routine - critical first season",
            "warning": None,
        })
        return schedule

    # --- Indoor starters ---
    if not direct_sow and weeks_before > 0:
        start_date = last_frost - timedelta(weeks=weeks_before)
        transplant_date = last_frost + timedelta(weeks=2)
        harvest_date = transplant_date + timedelta(days=dtm)

        schedule.append({
            "date": start_date,
            "week": get_week_of(start_date),
            "action": "Start seeds indoors under grow lights",
            "warning": None,
        })
        schedule.append({
            "date": last_frost - timedelta(weeks=1),
            "week": get_week_of(last_frost - timedelta(weeks=1)),
            "action": "Begin hardening off seedlings (move outside 1hr/day)",
            "warning": "Frost risk - bring seedlings in if temps drop below 40F",
        })
        schedule.append({
            "date": transplant_date,
            "week": get_week_of(transplant_date),
            "action": "Transplant outdoors to garden bed",
            "warning": (
                "Frost risk - watch forecast, last frost " + last_frost_str
                if is_frost_risk(transplant_date, last_frost_str, first_frost_str)
                else None
            ),
        })
        schedule.append({
            "date": harvest_date,
            "week": get_week_of(harvest_date),
            "action": "Harvest window begins",
            "warning": (
                "Frost risk - first fall frost " + first_frost_str
                if is_frost_risk(harvest_date, last_frost_str, first_frost_str)
                else None
            ),
        })

    # --- Direct sow ---
    else:
        sow_date = last_frost + timedelta(weeks=1)
        harvest_date = sow_date + timedelta(days=dtm)

        schedule.append({
            "date": sow_date,
            "week": get_week_of(sow_date),
            "action": "Direct sow seeds in garden bed",
            "warning": (
                "Frost risk - watch forecast, last frost " + last_frost_str
                if is_frost_risk(sow_date, last_frost_str, first_frost_str)
                else None
            ),
        })
        schedule.append({
            "date": sow_date + timedelta(weeks=2),
            "week": get_week_of(sow_date + timedelta(weeks=2)),
            "action": "Thin seedlings to recommended spacing",
            "warning": None,
        })
        schedule.append({
            "date": harvest_date,
            "week": get_week_of(harvest_date),
            "action": "Harvest window begins",
            "warning": (
                "Frost risk - first fall frost " + first_frost_str
                if is_frost_risk(harvest_date, last_frost_str, first_frost_str)
                else None
            ),
        })

    return schedule


def build_full_calendar(plant_list, last_frost, first_frost):
    """
    Builds schedules for all plants, sorted chronologically.
    Returns {plant_name: [schedule entries]}
    """
    calendar = {}
    for plant in plant_list:
        schedule = build_plant_schedule(plant, last_frost, first_frost)
        if schedule:
            calendar[plant["name"]] = {
                "native": plant["native"],
                "category": plant["category"],
                "schedule": sorted(schedule, key=lambda x: x["date"]),
            }
    return calendar


def format_calendar(calendar, city, state, zone, last_frost, first_frost):
    """Formats the full calendar for terminal display."""
    lines = []
    lines.append("=" * 60)
    lines.append("PLANTING CALENDAR")
    lines.append(f"Location : {city}, {state} (Zone {zone})")
    lines.append(f"Last spring frost : {last_frost}")
    lines.append(f"First fall frost  : {first_frost}")
    lines.append("=" * 60)

    category_order = ["vegetable", "fruit", "flower"]
    category_labels = {"vegetable": "VEGETABLES", "fruit": "FRUITS", "flower": "FLOWERS"}

    for category in category_order:
        plants_in_cat = {
            name: data for name, data in calendar.items()
            if data["category"] == category
        }
        if not plants_in_cat:
            continue

        lines.append(f"\n--- {category_labels[category]} ---")

        for name, data in plants_in_cat.items():
            native_tag = " [NATIVE]" if data["native"] else ""
            lines.append(f"\n{name}{native_tag}")
            for entry in data["schedule"]:
                lines.append(f"  {entry['week']:<22} {entry['action']}")
                if entry["warning"]:
                    lines.append(f"  {'':22} ⚠  {entry['warning']}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)
