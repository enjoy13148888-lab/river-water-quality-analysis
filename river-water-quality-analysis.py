import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

DATA_FILE = r"C:\COSC480 code\cosc480-25s2-project\river-water-quality-raw-data-by-nrwqn-site-1989-2013.csv"

#read file
def read_csv_data(filename: str, columns: list[str]) -> list[tuple]:
    """
    IMPORTANT NOTE:
      When completing Part one and Part Two of the project you do NOT need to understand how this function works.
    Reads in data from a list of csv files.
    Returns columns of data requested, in the order given in
    """
    df = pd.read_csv(filename)
    desired_columns = df[columns]
    return list(desired_columns.itertuples(index=False, name=None))

#set list to sort years
def get_unique_years_from_csv(filename):
    rows = read_csv_data(filename, ["sDate"])
    years = set()
    for row in rows:
        try:
            date = datetime.strptime(row[0], "%d/%m/%Y")  
            years.add(date.year)
        except Exception:
            continue
    return sorted(years)


unique_years = get_unique_years_from_csv(DATA_FILE)

#set list to sort river
def get_unique_rivers_from_csv(filename):
    rows = read_csv_data(filename, ["river"])
    river_set = set()
    for row in rows:
        if row[0]:  
            river_set.add(row[0].strip())  
    return sorted(river_set)

unique_rivers = get_unique_rivers_from_csv(DATA_FILE)

#create int to be category
def menu_select(options: list[str]) -> int:
    """
    - Prints a list of enumerated options and collects the users
    - The user is prompted until they enter a valid menu index
    - returns valid user selection
    """
    prompt = f"0-{len(options) - 1}:: "
    i = 0
    while i < len(options):
        print(f'[{i}] {options[i]}')
        i += 1

    #user's selection
    selection = int(input(prompt))
    while selection < 0 or selection >= len(options):
        print(f'{selection} is not a valid option\nTry again')
        selection = int(input(prompt))
    return selection

# print water quality for one year
def print_water_quality_report(year_of_interest: int, river_names: list[str]) -> None:
    """Prints a table outlining the number of crashes in a given year for a given speed limit"""
    data = read_csv_data(DATA_FILE, ["river", "sDate", "values"])
    print("Water Quality")
    print(f"{'Name':15}{'Count':>8}{'High':>10}{'Low':>10}{'Avg':>10}")
    found_any = False
    for name in river_names:
        count = 0
        total = 0
        high = None
        low = None
        for river_name, date_str, reading in data:
            date = datetime.strptime(date_str, "%d/%m/%Y")
            if name == river_name and year_of_interest == date.year:
                total += reading
                count += 1
                if high is None or reading > high:
                    high = reading
                if low is None or reading < low:
                    low = reading
        if count > 0:
            found_any = True
            avg = total / count
            print(f"{name:15}{count:8}{high:10.2f}{low:10.2f}{avg:10.2f}")
        else:
            print(name, 0, "N/A", "N/A", "N/A")
    if not found_any:  
        print("Warning: No records found for the selected year and rivers.")

# print reports for all years
def print_water_quality_report_all_years(river_names: list[str]) -> None:
    years = get_unique_years_from_csv(DATA_FILE)
    for year in years:
        print(f"\nYear: {year}")
        print_water_quality_report(year, river_names)

def plot_water_quality_over_time(river_names: list[str]) -> None:
    data = read_csv_data(DATA_FILE, ["river", "sDate", "values"])
    river_dict = {name: {} for name in river_names}
    for river_name, date_str, value in data:
        try:
            date = datetime.strptime(date_str, "%d/%m/%Y")
        except Exception:
            continue
        year = date.year
        if river_name in river_dict:
            river_dict[river_name].setdefault(year, []).append(value)
    # average of years
    for river_name in river_names:
        years = sorted(river_dict[river_name].keys())
        avg_values = [sum(river_dict[river_name][y]) / len(river_dict[river_name][y]) for y in years]
        plt.plot(years, avg_values, marker='o', label=river_name)
    plt.xlabel("Year")
    plt.ylabel("Average Water Quality Value")
    plt.title("Water Quality Over Time")
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    """Small application that presents tables and graphs based on water quality data."""
    
    menu_options = [
        "Water Quality Report-Single Year","Water Quality Report-All Year",
        "Water Quality Over Time Graph",
        "Exit"
    ]
    option = menu_select(menu_options)
    if option == 0:
        while True:
            try:
                year_input = input(f"Enter a year between {unique_years[0]} and {unique_years[-1]}: ")
                year = int(year_input)
                if year in unique_years:
                    break
                else:
                    print(f"Error: Year {year} not found in the data. Please enter a year from {unique_years[0]} to {unique_years[-1]}.")
            except ValueError:
                print("Error: Invalid year. Please enter a numerical year .")
        
        while True:
            rivers_string = input("Enter river names (comma separated):  ")
            river_names = [r.strip() for r in rivers_string.split(",") if r.strip()]
            invalid_rivers = [r for r in river_names if r not in unique_rivers]
            if invalid_rivers:
                print("Error: These river names are not found in the data:")
                for ir in invalid_rivers:
                    print(f" - {ir}")
                print("Please enter valid river names.")
            else:
                break
        print_water_quality_report(year, river_names)
    elif option==1:
        while True:
            rivers_string = input("Enter river names (comma separated):  ")
            river_names = [r.strip() for r in rivers_string.split(",") if r.strip()]
            invalid_rivers = [r for r in river_names if r not in unique_rivers]
            if invalid_rivers:
                print("Error: These river names are not found in the data:")
                for ir in invalid_rivers:
                    print(f" - {ir}")
                print("Please enter valid river names.")
            else:
                break
        print_water_quality_report_all_years(river_names)

    elif option == 2:
        while True:
            river_name = input("Enter a single river name: ").strip()
            if not river_name:
                print("Error: Input cannot be empty. Please enter a river name.")
                continue
            if river_name not in unique_rivers:
                print(f"Error: '{river_name}' is not found in the data. Please enter a valid river name.")
            else:
                break
        plot_water_quality_over_time([river_name])
    elif option == 3:
        print("Bye")


main()



