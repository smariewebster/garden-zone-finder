# Contributing to Garden Zone Finder

Contributions are welcome — especially from Southwest and New Mexico gardeners who know what actually grows here. Whether you're adding a native plant, fixing companion data, or reporting a bad frost date, your local knowledge makes this tool better.

---

## How to Add a Plant

Plants live in the `PLANTS` list in `plants.py`. Each plant is a dict with the following required fields:

```python
{
    "name": "Blue Corn",
    "category": "vegetable",          # vegetable, fruit, flower, or herb
    "zones": ["5b", "6a", "6b", "7a", "7b", "8a"],
    "native_regions": ["southwest"],  # see guidelines below; empty list if not native
    "water": "low",                   # low, medium, or high
    "days_to_maturity": 100,
    "notes": "Traditional Pueblo staple. Drought-tolerant once established. Plant after soil warms.",
    "direct_sow": True,               # True = direct sow; False = start indoors
    "weeks_before_frost": 0,          # weeks before last frost to start indoors (0 if direct_sow)
    "companions": [
        {"name": "Beans", "reason": "fix nitrogen that corn depletes"},
        {"name": "Squash", "reason": "ground cover suppresses weeds"},
    ],
    "avoid": [
        {"name": "Tomato", "reason": "compete for nutrients and attract shared pests"},
    ],
}
```

**Optional fields:**

- `cool_season: True` — add this for crops that should be sown 4 weeks *before* last frost (carrots, peas, spinach, etc.)

---

## Plant Submission Guidelines

- **All fields are required.** Do not omit any key from the structure above.
- **`native_regions`** must use only these seven values (as a list):
  - `southwest`, `great_plains`, `northeast`, `southeast`, `midwest`, `northwest`, `california`
  - Use an empty list `[]` if the plant is not native to any of these regions.
- **`companions` and `avoid`** entries must each have both a `name` key and a `reason` key. Aim for 2–4 companions and 1–3 avoid entries. Use accurate, sourced companion planting data — not folklore.
- **`notes`** should be practical and specific. Where relevant, include high desert or Southwest growing context (elevation, drought tolerance, monsoon timing, caliche soil, etc.).
- **`zones`** should reflect the plant's realistic hardiness range, not just where it can technically survive.
- **`days_to_maturity`** should reflect outdoor growing time from transplant (for indoor-started plants) or from direct sow.

---

## How to Submit a PR

1. **Fork the repo** on GitHub and clone your fork locally.

2. **Create a branch** named after the plant you're adding:
   ```bash
   git checkout -b add-blue-corn
   ```

3. **Add your plant** to the `PLANTS` list in `plants.py`. Maintain alphabetical order within each category grouping if possible.

4. **Run the verify command** to confirm the file imports cleanly and the count looks right:
   ```bash
   python3 -c 'from plants import PLANTS; print(len(PLANTS), "plants loaded")'
   ```

5. **Open a pull request** against the `main` branch. In the PR description, include:
   - The plant name and category
   - Your zone/location if relevant
   - Any sources for companion planting data

---

## Other Ways to Contribute

- **Wrong frost dates?** Frost date data comes from phzmapi.org. If your local dates are off, open an issue with your zip code and the correct dates from your local extension office.
- **Bad companion planting data?** Open an issue or PR with a correction and a source. Accuracy matters more than completeness.
- **Feature ideas?** File an issue describing the feature and the use case. Southwest/high desert gardening edge cases especially welcome.

---

Questions? Open an issue on GitHub.
