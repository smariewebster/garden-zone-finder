from datetime import datetime, timedelta

def parse_frost_date(date_str, year=None):
    """Convert 'Apr 15' style string to a datetime object."""
    if year is None:
        year = datetime.now().year
    return datetime.strptime(f"{date_str} {year}", "%b %d %Y")

def get_week_of(dt):
    """Return a 'Week of Mon DD' string for a given date."""
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

def _indoor_schedule(plant, last_frost, last_frost_str, first_frost_str):
    """Builds the start-indoors schedule for a plant."""
    weeks_before = plant.get("weeks_before_frost", 0)
    dtm = plant["days_to_maturity"]
    start_date = last_frost - timedelta(weeks=weeks_before)
    transplant_date = last_frost + timedelta(weeks=2)
    harvest_date = transplant_date + timedelta(days=dtm)
    return sorted([
        {
            "date": start_date,
            "week": get_week_of(start_date),
            "action": "Start seeds indoors under grow lights",
            "warning": None,
        },
        {
            "date": last_frost - timedelta(weeks=1),
            "week": get_week_of(last_frost - timedelta(weeks=1)),
            "action": "Begin hardening off seedlings (move outside 1hr/day)",
            "warning": "Frost risk - bring seedlings in if temps drop below 40F",
        },
        {
            "date": transplant_date,
            "week": get_week_of(transplant_date),
            "action": "Transplant outdoors to garden bed",
            "warning": (
                "Frost risk - watch forecast, last frost " + last_frost_str
                if is_frost_risk(transplant_date, last_frost_str, first_frost_str)
                else None
            ),
        },
        {
            "date": harvest_date,
            "week": get_week_of(harvest_date),
            "action": "Harvest window begins",
            "warning": (
                "Frost risk - first fall frost " + first_frost_str
                if is_frost_risk(harvest_date, last_frost_str, first_frost_str)
                else None
            ),
        },
    ], key=lambda x: x["date"])

def _direct_sow_schedule(plant, last_frost, last_frost_str, first_frost_str, cool_season=False):
    """Builds the direct sow schedule for a plant."""
    dtm = plant["days_to_maturity"]
    sow_date = last_frost - timedelta(weeks=4) if cool_season else last_frost + timedelta(weeks=1)
    harvest_date = sow_date + timedelta(days=dtm)
    return sorted([
        {
            "date": sow_date,
            "week": get_week_of(sow_date),
            "action": "Direct sow seeds in garden bed",
            "warning": (
                "Frost risk - watch forecast, last frost " + last_frost_str
                if is_frost_risk(sow_date, last_frost_str, first_frost_str)
                else None
            ),
        },
        {
            "date": sow_date + timedelta(weeks=2),
            "week": get_week_of(sow_date + timedelta(weeks=2)),
            "action": "Thin seedlings to recommended spacing",
            "warning": None,
        },
        {
            "date": harvest_date,
            "week": get_week_of(harvest_date),
            "action": "Harvest window begins",
            "warning": (
                "Frost risk - first fall frost " + first_frost_str
                if is_frost_risk(harvest_date, last_frost_str, first_frost_str)
                else None
            ),
        },
    ], key=lambda x: x["date"])

def build_plant_schedule(plant, last_frost_str, first_frost_str):
    """
    Returns schedule info for a plant.

    For plants where direct_sow is False and weeks_before_frost > 0,
    returns both an indoor-start and a direct-sow option:
      {"type": "dual", "option_a": [...], "option_b": [...]}

    For all other plants, returns a single schedule:
      {"type": "single", "schedule": [...]}
    """
    last_frost = parse_frost_date(last_frost_str)
    first_frost = parse_frost_date(first_frost_str)
    weeks_before = plant.get("weeks_before_frost", 0)
    direct_sow = plant["direct_sow"]
    dtm = plant["days_to_maturity"]
    cool_season = plant.get("cool_season", False)

    # --- Garlic special case - fall planting ---
    if plant["name"] == "Garlic":
        plant_date = last_frost.replace(month=10, day=15)
        harvest_date = plant_date + timedelta(days=dtm)
        return {"type": "single", "schedule": sorted([
            {"date": plant_date, "week": get_week_of(plant_date), "action": "Plant cloves directly in ground", "warning": None},
            {"date": harvest_date, "week": get_week_of(harvest_date), "action": "Harvest when tops begin to yellow", "warning": None},
        ], key=lambda x: x["date"])}

    # --- Perennials / bare root (long DTM, not seed-started) ---
    if dtm >= 365 and weeks_before == 0:
        plant_date = last_frost + timedelta(weeks=2)
        return {"type": "single", "schedule": [
            {"date": plant_date, "week": get_week_of(plant_date), "action": "Plant bare root / container / pad in ground", "warning": None},
            {"date": plant_date + timedelta(weeks=4), "week": get_week_of(plant_date + timedelta(weeks=4)), "action": "Establish watering routine - critical first season", "warning": None},
        ]}

    # --- Dual schedule: indoor start (A) or direct sow (B) ---
    if not direct_sow and weeks_before > 0:
        return {
            "type": "dual",
            "option_a": _indoor_schedule(plant, last_frost, last_frost_str, first_frost_str),
            "option_b": _direct_sow_schedule(plant, last_frost, last_frost_str, first_frost_str, cool_season=False),
        }

    # --- Direct sow only ---
    return {"type": "single", "schedule": _direct_sow_schedule(plant, last_frost, last_frost_str, first_frost_str, cool_season)}


def build_full_calendar(plant_list, last_frost, first_frost):
    """Builds schedules for all plants. Returns {plant_name: {category, native_regions, schedule_info}}"""
    calendar = {}
    for plant in plant_list:
        schedule_info = build_plant_schedule(plant, last_frost, first_frost)
        calendar[plant["name"]] = {
            "native_regions": plant["native_regions"],
            "category": plant["category"],
            "schedule_info": schedule_info,
        }
    return calendar


def format_calendar(calendar, city, state, zone, last_frost, first_frost):
    """
    For plants with dual schedules, displays both options and prompts the user
    to choose per plant. Returns the final formatted calendar string.
    """
    category_order = ["vegetable", "fruit", "flower", "herb"]
    category_labels = {"vegetable": "VEGETABLES", "fruit": "FRUITS", "flower": "FLOWERS", "herb": "HERBS"}

    # --- Step 1: Prompt choices for dual-schedule plants ---
    choices = {}
    dual_plants = {
        name: data for name, data in calendar.items()
        if data["schedule_info"]["type"] == "dual"
    }

    if dual_plants:
        print("\n" + "=" * 60)
        print("PLANTING METHOD CHOICES")
        print("Choose a planting method for each plant below.")
        print("=" * 60)

        for name, data in dual_plants.items():
            info = data["schedule_info"]
            native_tag = " [NATIVE]" if data["native_regions"] else ""
            print(f"\n{name}{native_tag}")

            print("  Option A - Start Indoors:")
            for entry in info["option_a"]:
                print(f"    {entry['week']:<22} {entry['action']}")
                if entry["warning"]:
                    print(f"    {'':22} ⚠  {entry['warning']}")

            print("  Option B - Direct Sow:")
            for entry in info["option_b"]:
                print(f"    {entry['week']:<22} {entry['action']}")
                if entry["warning"]:
                    print(f"    {'':22} ⚠  {entry['warning']}")

            while True:
                choice = input(f"  Choose A or B for {name}: ").strip().upper()
                if choice in ("A", "B"):
                    choices[name] = choice
                    break
                print("  Please enter A or B.")

    # --- Step 2: Build final calendar output ---
    lines = []
    lines.append("=" * 60)
    lines.append("PLANTING CALENDAR")
    lines.append(f"Location : {city}, {state} (Zone {zone})")
    lines.append(f"Last spring frost : {last_frost}")
    lines.append(f"First fall frost  : {first_frost}")
    lines.append("=" * 60)

    for category in category_order:
        plants_in_cat = {
            name: data for name, data in calendar.items()
            if data["category"] == category
        }
        if not plants_in_cat:
            continue

        lines.append(f"\n--- {category_labels[category]} ---")

        for name, data in plants_in_cat.items():
            native_tag = " [NATIVE]" if data["native_regions"] else ""
            lines.append(f"\n{name}{native_tag}")

            info = data["schedule_info"]
            if info["type"] == "dual":
                choice = choices.get(name, "A")
                schedule = info["option_a"] if choice == "A" else info["option_b"]
                label = "Start Indoors" if choice == "A" else "Direct Sow"
                lines.append(f"  [Method: Option {choice} - {label}]")
            else:
                schedule = info["schedule"]

            for entry in schedule:
                lines.append(f"  {entry['week']:<22} {entry['action']}")
                if entry["warning"]:
                    lines.append(f"  {'':22} ⚠  {entry['warning']}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)
