import csv
import argparse
from datetime import datetime, timedelta


def process_csv(file_path):
    # Dictionary to store the city type for each day (with date as key)
    days_dict = {}

    with open(file_path) as csvfile:
        csvreader = csv.DictReader(csvfile)

        # Iterate through each project in the CSV
        for project in csvreader:
            city_type = project["city_type"]
            start_date = datetime.strptime(project["start_date"], "%m/%d/%Y").date()
            end_date = datetime.strptime(project["end_date"], "%m/%d/%Y").date()

            # Generate list of all dates between start_date and end_date
            current_date = start_date
            while current_date <= end_date:
                # Add the date to the dictionary if it's not already there
                if current_date not in days_dict:
                    days_dict[current_date] = city_type
                else:
                    # If there is already a city_type for this date and it's HC, we keep HC
                    if city_type == "HC":
                        days_dict[current_date] = "HC"
                current_date += timedelta(days=1)

    return days_dict


# Function to calculate reimbursement based on city type and day type
def calculate_reimbursement_days(days_dict):
    sorted_dates = sorted(days_dict.keys())
    # Account for edge case of no days
    if len(sorted_dates) == 0:
        return 0

    # First and last days are always travel
    first_day = sorted_dates[0]
    last_day = sorted_dates[-1]
    total_reimbursement = 45
    if days_dict[first_day] == "HC":
        total_reimbursement += 10

    # If there is only a single day, don't count it twice
    if first_day != last_day:
        total_reimbursement += 45
        if days_dict[last_day] == "HC":
            total_reimbursement += 10

    for i in range(1, len(sorted_dates) - 1):
        prev_day = sorted_dates[i - 1]
        current_day = sorted_dates[i]
        next_day = sorted_dates[i + 1]

        # Determine if the day is a full day or travel day
        if (next_day - prev_day).days == 2:
            reimbursement = 75
        else:
            reimbursement = 45

        # Check if the city type is HC and add the premium
        if days_dict[current_day] == "HC":
            reimbursement += 10

        total_reimbursement += reimbursement

    return total_reimbursement


def main():
    parser = argparse.ArgumentParser(description="Calculate reimbursement.")
    parser.add_argument(
        "csv_file", help="Path to the CSV file containing the project data."
    )
    args = parser.parse_args()

    days_dict = process_csv(args.csv_file)

    # Calculate the total reimbursement
    total_reimbursement = calculate_reimbursement_days(days_dict)

    print(f"Total Reimbursement: ${total_reimbursement}")


if __name__ == "__main__":
    main()
