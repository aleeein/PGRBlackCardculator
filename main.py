from datetime import datetime, timedelta

def get_date_input(prompt):
    """Get a date input from the user in YYYY-MM-DD format."""
    while True:
        try:
            date_input = input(prompt)
            return datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD format.")

def calculate_bc(start_date, end_date, bought_monthly, remaining_days=0, num_monthly_packs=0, buy_pack_later=False, buy_date=None):
    """Calculate the total BC based on user inputs."""
    total_bc = 0
    weeks_after = 0
    days_remainder = 0
    months_after = 0

    if bought_monthly:
        if remaining_days > 0:
            daily_bc = 100 * remaining_days
            daily_missions_bc = 30 * remaining_days
            weeks = remaining_days // 7
            weekly_bc = weeks * 1000
            total_bc += daily_bc + daily_missions_bc + weekly_bc

        days_after_monthly_end = (end_date - (start_date + timedelta(days=remaining_days))).days
        if days_after_monthly_end > 0:
            weeks_after = days_after_monthly_end // 7
            days_remainder = days_after_monthly_end % 7
            months_after = days_after_monthly_end // 30
            total_bc += (3300 * num_monthly_packs)  # 3000 BC + 300 BC initial
            total_bc += (30 * days_after_monthly_end) + (1000 * weeks_after)
    
    else:
        if buy_pack_later and buy_date:
            days_after_buying = (end_date - buy_date).days
            if days_after_buying > 0:
                weeks_after = days_after_buying // 7
                days_remainder = days_after_buying % 7
                months_after = days_after_buying // 30
                total_bc += (3300 * num_monthly_packs)  # 3000 BC + 300 BC initial per pack
                total_bc += (30 * days_after_buying) + (1000 * weeks_after)
        else:
            # Calculate BC from daily and weekly missions only
            days_total = (end_date - start_date).days
            weeks_after = days_total // 7
            days_remainder = days_total % 7
            months_after = days_total // 30
            total_bc += (30 * days_total) + (1000 * weeks_after)
    
    return total_bc, weeks_after, days_remainder, months_after

# Main program
start_date = get_date_input("Enter the start date (YYYY-MM-DD): ")
end_date = get_date_input("Enter the end date (YYYY-MM-DD): ")
bought_monthly = input("Have you already bought the monthly pack? (yes/no): ").strip().lower()

if bought_monthly == "yes":
    remaining_days = int(input("How many days are remaining in your current monthly pack? "))
    days_after_current_pack = (end_date - (start_date + timedelta(days=remaining_days))).days
    weeks = days_after_current_pack // 7
    days_remainder = days_after_current_pack % 7
    months_after = days_after_current_pack // 30
    num_monthly_packs = int(input(f"From the end of your monthly period to the target date, the period is approximately {months_after} months which is {weeks} weeks, and {days_remainder} days. How many monthly packs will you buy? "))
    total_bc, weeks_after, days_remainder, months_after = calculate_bc(start_date, end_date, bought_monthly=True, remaining_days=remaining_days, num_monthly_packs=num_monthly_packs)
elif bought_monthly == "no":
    buy_pack_later = input("Do you want to buy the monthly pack? (yes/no): ").strip().lower()
    if buy_pack_later == "yes":
        buy_date = get_date_input("When will you buy the monthly pack? (YYYY-MM-DD): ")
        num_monthly_packs = int(input("How many monthly packs will you buy during the remaining period? "))
        total_bc, weeks_after, days_remainder, months_after = calculate_bc(start_date, end_date, bought_monthly=False, buy_pack_later=True, buy_date=buy_date, num_monthly_packs=num_monthly_packs)
    else:
        total_bc, weeks_after, days_remainder, months_after = calculate_bc(start_date, end_date, bought_monthly=False)

print("---------------------------------------------")
print(f"Total BC you will obtain from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} is: {total_bc} BC")