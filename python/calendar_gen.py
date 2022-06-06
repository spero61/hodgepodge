# Calendar Generator
import calendar, datetime, sys

# default: current month (no command line argument is provided)
dt = datetime.datetime.now()
year = dt.year
month = dt.month

# Usage: python calendar_gen.py [year] [month]
if len(sys.argv) == 3:
    try:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
    except ValueError as err:
        print(err, "You should enter year and month in integer numbers")
        sys.exit(1)

# display the calendar and let user know the correct usage
elif len(sys.argv) != 1:
    print("=== Usage: python calendar_gen.py [year] [month] ===\n")

# to set the first day of the week to Sunday (6)
calendar.setfirstweekday(calendar.SUNDAY)

week_header = calendar.weekheader(3)
# day_list starts on Sunday.
day_list = week_header.split(" ")  # ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

# cf. list(calendar.day_name) for full day names ['Monday', 'Tuesday' ... 'Sunday']
day_names = list(calendar.day_abbr)  # ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# 1st day of the month in int: (MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY) = range(7)
first_day_idx = calendar.weekday(year=year, month=month, day=1)

# last day of the month (e.g., 30)
last_day_int = calendar._monthlen(year=year, month=month)
last_day_idx = calendar.weekday(year=year, month=month, day=last_day_int)

first_day_str = day_names[first_day_idx]
last_day_str = day_names[last_day_idx]


print(month)  # int
print(calendar.month_name[month])  # January = 1
print(first_day_str, 1)
print(last_day_str, last_day_int)
print()

print(calendar.month(theyear=year, themonth=month))
