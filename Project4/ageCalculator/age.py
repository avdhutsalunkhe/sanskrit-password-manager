birth_day = int(input("Enter your birth day: "))
birth_month = int(input("Enter your birth month: "))
birth_year = int(input("Enter your birth year: "))

print("Date of Birth:", birth_day, "/", birth_month, "/", birth_year)

current_day = int(input("Enter your current day: "))
current_month = int(input("Enter your current month: "))
current_year = int(input("Enter your current year: "))

print("Current Date:", current_day, "/", current_month, "/", current_year)

# Check for invalid inputs (future birth date)
if (birth_year > current_year) or (birth_year == current_year and birth_month > current_month) or \
   (birth_year == current_year and birth_month == current_month and birth_day > current_day):
    print("Hi, Time Traveller!")
else:
    # Days in each month
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Adjust for day and month
    if current_day < birth_day:
        current_month -= 1
        current_day += month_days[birth_month - 1]

    if current_month < birth_month:
        current_year -= 1
        current_month += 12

    calculated_day = current_day - birth_day
    calculated_month = current_month - birth_month
    calculated_year = current_year - birth_year

    print("Your Age is:", calculated_year, "years", calculated_month, "months", calculated_day, "days")
