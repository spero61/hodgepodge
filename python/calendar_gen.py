# Monthly Calendar Generator (.xlsx)
import sys
import datetime
import calendar
import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment, Border, Side

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

# set output_filename (e.g., calendar-2022-06.xlsx)
fomatted_month = f"{month}" if month >= 10 else f"0{month}"
output_filename = f"calendar-{year}-{fomatted_month}.xlsx"

# to set the first day of the week to Sunday (6)
calendar.setfirstweekday(calendar.SUNDAY)

# day_list starts on Sunday.
week_header = calendar.weekheader(3)

# ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
day_list = week_header.split(" ")

# ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
day_names = list(calendar.day_abbr)

# 1st day of the month in int: (MONDAY = 0, TUESDAY = 1, ... )
first_day_idx = calendar.weekday(year=year, month=month, day=1)

# last day of the month (e.g., 30)
last_day_int = calendar._monthlen(year=year, month=month)
last_day_idx = calendar.weekday(year=year, month=month, day=last_day_int)

# (e.g., Wed)
first_day_str = day_names[first_day_idx]
last_day_str = day_names[last_day_idx]

# create a workbook
wb = openpyxl.Workbook()  # wb: workbookws
ws = wb.active  # ws: worksheet
ws.title = f"{calendar.month_abbr[month].upper()}-{year}"

# color palette for months
color_holidays = [
    "",
    "C0AB8C",  # January
    "B0CFC0",  # February
    "F1E67C",  # March
    "FFC5BF",  # April
    "5AC3B2",  # May
    "6667AB",  # June
    "0074BF",  # July
    "00696F",  # August
    "D59B89",  # September
    "8B6852",  # October
    "953640",  # November
    "DD1C0D",  # December
]

# set named styles: https://openpyxl.readthedocs.io/en/stable/styles.html
color_holiday = color_holidays[month]
color_darkgray = "333333"
font_weekend_head = Font(size=21, bold=True, color=color_holiday)
font_weekday_head = Font(size=21, bold=True, color=color_darkgray)
font_holiday = Font(size=27, bold=True, color=color_holiday)
font_weekday = Font(size=27, bold=True, color=color_darkgray)
font_month_str = Font(size=58, bold=True, color=color_darkgray)
font_month_int = Font(size=58, bold=True, color=color_holiday)
alignment_head = Alignment(horizontal="center", vertical="bottom")
alignment_day = Alignment(horizontal="center", vertical="top")
border_top_thick = Border(top=Side(border_style="thick", color=color_darkgray))

# Month str (e.g., JUNE)
ws["A1"].value = calendar.month_name[month].upper()
ws["A1"].font = font_month_str
ws["A1"].alignment = Alignment(horizontal="center", vertical="center")

# Month int (e.g., 6)
ws["F1"].value = month
ws["F1"].font = font_month_int
ws["F1"].alignment = Alignment(horizontal="center", vertical="center")

ws.merge_cells("A1:E1")
ws.merge_cells("F1:G1")

# set row height and column width respectively
for row in range(ws.max_row):
    if row == 1:  # month
        ws.row_dimensions[row].height = 80.25
    elif row == 2:  # header
        ws.row_dimensions[row].height = 37.5
    else:  # day
        ws.row_dimensions[row].height = 50.25

column_letters = tuple(
    get_column_letter(col_num + 1) for col_num in range(ws.max_column)
)
for column_letter in column_letters:
    ws.column_dimensions[column_letter].width = 11.25

# day head cells (e.g., Sun, Mon, Tue, ..., Sat)
day_idx = 0
for row in ws["A2:G2"]:
    for cell in row:
        cell.value = day_list[day_idx]
        day_idx += 1
        cell.alignment = alignment_head
        if cell.coordinate.startswith("A") or cell.coordinate.startswith("G"):
            cell.font = font_weekend_head
        else:
            cell.font = font_weekday_head

# match colors for each date cell
cell_objs = []
for idx in range(3, 24, 4):
    for row in ws[f"A{idx}:G{idx}"]:
        for cell in row:
            if cell.coordinate.startswith("A"):  # Sundays
                cell.font = font_holiday
            elif cell.coordinate.startswith("G"):  # Saturdays
                cell.font = font_holiday
            else:  # Weekdays
                cell.font = font_weekday
            cell.alignment = alignment_day
            cell_objs.append(cell)

# write each date to the correspond cell
# {"Sun": 0, "Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6}
day_dict = {}
for i in range(7):
    day_dict[day_list[i]] = i

start_day = day_dict[first_day_str]
date = 1
for i in range(start_day, start_day + last_day_int):
    cell_objs[i].value = date
    date += 1

# draw default cell borders for the weekhead row
for cell in ws["3:3"]:
    cell.border = border_top_thick

# add thick line as cell borders so as to fit it to the specific calendar
# e.g., October 2022 requires 6 additional border lines
#       while February 2026 needs 4 more lines
for idx in range(7, 28, 4):
    if ws[f"A{idx - 4}"].value or ws[f"G{idx - 4}"].value:
        for cell in ws[f"{idx}:{idx}"]:
            cell.border = border_top_thick

# to add space between rows (by adding a row to the top of row 2)
ws.insert_rows(2)

# set print settings
last_cell = f"{get_column_letter(ws.max_column)}{ws.max_row}"
ws.print_area = f"A1:{last_cell}"
ws.page_setup.orientation = ws.ORIENTATION_PORTRAIT
ws.page_setup.paperSize = ws.PAPERSIZE_A4

# check every cell value for debugging
"""
for row in ws["A1":last_cell]:
    row_num = ""
    for cell in row:
        print(cell.coordinate, cell.value)
        row_num = cell.coordinate[1:]
    print(f"~~~ end of row {row_num} ~~~")
print("last_cell", last_cell)
"""

wb.save(output_filename)
print(f"[{output_filename}] has created at {dt}")
wb.close()
