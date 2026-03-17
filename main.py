from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from zone_lookup import lookup
from plants import get_plants_for_zone
from scraper import scrape_all_plants
from organizer import organize_tips, format_for_display

console = Console()

def get_zip_input():
    """Prompt user for a zip code and validate it."""
    while True:
        zipcode = input("\nEnter your zip code: ").strip()
        if zipcode.isdigit() and len(zipcode) == 5:
            return zipcode
        console.print("[red]Invalid zip code. Please enter a 5-digit US zip code.[/red]")

def ask_yes_no(prompt):
    """Simple yes/no prompt."""
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter y or n.")

def save_output(text, zipcode):
    """Save output to a text file."""
    filename = f"garden_report_{zipcode}.txt"
    with open(filename, "w") as f:
        f.write(text)
    console.print(f"\n[green]Report saved to {filename}[/green]")

def main():
    console.print("\n[bold green]GARDEN ZONE FINDER[/bold green]")
    console.print("Find what grows in your zone with tips from around the web.\n")

    # Step 1 - Zip code lookup
    zipcode = get_zip_input()

    with Progress(SpinnerColumn(), TextColumn("{task.description}"), transient=True) as progress:
        progress.add_task("Looking up your growing zone...", total=None)
        location = lookup(zipcode)

    if not location:
        console.print(f"[red]Could not find data for zip code {zipcode}. Please try another.[/red]")
        return

    console.print(f"\n[bold]Location:[/bold] {location['city']}, {location['state']}")
    console.print(f"[bold]Growing Zone:[/bold] {location['zone']}")
    console.print(f"[bold]Last Spring Frost:[/bold] {location['last_spring_frost']}")
    console.print(f"[bold]First Fall Frost:[/bold] {location['first_fall_frost']}")

    # Step 2 - Plant list
    plant_list = get_plants_for_zone(location["zone"])

    if not plant_list:
        console.print(f"\n[yellow]No plants found in database for zone {location['zone']}.[/yellow]")
        return

    console.print(f"\n[bold]{len(plant_list)} plants found for zone {location['zone']}.[/bold]")

    # Step 3 - Optional scraping
    scraped_data = {}
    if ask_yes_no("\nScrape the web for growing tips? (takes ~2 min)"):
        console.print("\n[yellow]Scraping gardening sites... this may take a moment.[/yellow]")
        with Progress(SpinnerColumn(), TextColumn("{task.description}"), transient=True) as progress:
            progress.add_task("Scraping tips from gardening sites...", total=None)
            scraped_data = scrape_all_plants(plant_list, location["zone"])
        console.print("[green]Scraping complete.[/green]")
    else:
        console.print("\n[yellow]Skipping scrape - showing plant database only.[/yellow]")
        # Populate empty tips so organizer still works
        scraped_data = {p["name"]: {} for p in plant_list}

    # Step 4 - Organize and display
    organized = organize_tips(scraped_data, plant_list)
    output = format_for_display(
        organized,
        location["zone"],
        location["city"],
        location["state"],
        location["last_spring_frost"],
        location["first_fall_frost"],
    )

    print(output)

    # Step 5 - Optional save
    if ask_yes_no("\nSave report to a text file?"):
        save_output(output, zipcode)

if __name__ == "__main__":
    main()
