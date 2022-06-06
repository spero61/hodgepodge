# Monthly Calendar Generator (.xlsx)
import calendar, datetime, sys, openpyxl
from openpyxl.utils import get_column_letter, column_index_from_string
from openpyxl.styles import Font

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

input_filename = "calendar_template.xlsx"
fomatted_month = f"{month}" if month >= 10 else f"0{month}"
output_filename = f"calendar-{year}-{fomatted_month}.xlsx"

# to set the first day of the week to Sunday (6)
calendar.setfirstweekday(calendar.SUNDAY)

# day_list starts on Sunday.
week_header = calendar.weekheader(3)
day_list = week_header.split(" ")  # ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

# cf. list(calendar.day_name) for full day names ['Monday', 'Tuesday' ... 'Sunday']
day_names = list(calendar.day_abbr)  # ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# 1st day of the month in int: (MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY) = range(7)
first_day_idx = calendar.weekday(year=year, month=month, day=1)

# last day of the month (e.g., 30)
last_day_int = calendar._monthlen(year=year, month=month)
last_day_idx = calendar.weekday(year=year, month=month, day=last_day_int)

# (e.g., Wed)
first_day_str = day_names[first_day_idx]
last_day_str = day_names[last_day_idx]

# load calendar template excel file
wb = openpyxl.load_workbook(input_filename)
sheet = wb["template"]

# # check cell values for debugging
# last_cell = f"{get_column_letter(sheet.max_column)}{sheet.max_row}"  # G14
# for row in sheet["A1":last_cell]:
#     for cell in row:
#         print(cell.coordinate, cell.value)
#     print("~~~ end of row ~~~")

sheet["A1"].value = calendar.month_name[month]  # calendar.month_name[1] = "January"
sheet["F1"].value = month

cell_objs = []
for idx in range(3, 14, 2):
    for row in sheet[f"A{idx}":f"G{idx}"]:
        for cell in row:
            cell.value = ""  # clear cells
            cell_objs.append(cell)

# {'Sun': 0, 'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6}
day_dict = {}
for i in range(7):
    day_dict[day_list[i]] = i

start_day = day_dict[first_day_str]
date = 1
for i in range(start_day, start_day + last_day_int):
    cell_objs[i].value = date
    date += 1

wb.save(output_filename)
print(f"{output_filename} has created")
wb.close()
