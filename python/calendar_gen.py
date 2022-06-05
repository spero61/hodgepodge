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

print(calendar.month(year, month), end="")
