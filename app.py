from flask import Flask, render_template, request, jsonify
from zone_lookup import lookup
from plants import get_plants_for_zone, is_native_to_region, state_to_region
from organizer import organize_tips, format_for_display
from planting_calendar import build_full_calendar, format_calendar

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/zone", methods=["POST"])
def zone_lookup():
    """API endpoint - takes zip, returns zone + frost dates as JSON."""
    data = request.get_json()
    zipcode = data.get("zip", "").strip()

    if not zipcode or not zipcode.isdigit() or len(zipcode) != 5:
        return jsonify({"error": "Invalid zip code"}), 400

    location = lookup(zipcode)
    if not location:
        return jsonify({"error": "Zip code not found"}), 404

    return jsonify(location)

@app.route("/report")
def report():
    """Full plant report page."""
    zipcode = request.args.get("zip", "").strip()

    if not zipcode:
        return render_template("index.html")

    location = lookup(zipcode)
    if not location:
        return render_template("index.html")

    plant_list = get_plants_for_zone(location["zone"])
    region = state_to_region(location["state"])

    # Tag native status per plant for this region
    for plant in plant_list:
        plant["is_native"] = is_native_to_region(plant, region)

    # No scraping on web version - too slow for a page load
    scraped_data = {p["name"]: {} for p in plant_list}
    organized = organize_tips(scraped_data, plant_list)

    # Build calendar with default sow preferences
    calendar = build_full_calendar(plant_list, location["last_spring_frost"], location["first_fall_frost"])

    return render_template(
        "report.html",
        location=location,
        organized=organized,
        calendar=calendar,
        zipcode=zipcode,
    )

@app.route("/calendar")
def calendar_view():
    """Planting calendar page, optionally filtered to selected plants."""
    zipcode = request.args.get("zip", "").strip()
    plants_param = request.args.get("plants", "").strip()

    if not zipcode:
        return render_template("index.html")

    location = lookup(zipcode)
    if not location:
        return render_template("index.html")

    plant_list = get_plants_for_zone(location["zone"])

    # Filter to selected plants if provided
    if plants_param:
        selected_names = {name.strip() for name in plants_param.split(",") if name.strip()}
        plant_list = [p for p in plant_list if p["name"] in selected_names]
    else:
        selected_names = None

    calendar = build_full_calendar(
        plant_list,
        location["last_spring_frost"],
        location["first_fall_frost"],
    )

    return render_template(
        "calendar.html",
        location=location,
        calendar=calendar,
        zipcode=zipcode,
        selected_plants=sorted(selected_names) if selected_names else None,
    )

if __name__ == "__main__":
    app.run(debug=True)
