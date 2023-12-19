import argparse
import datetime
import csv
import subprocess


def read_tasks(file_path, target_date):
    tasks = ''
    with open(file_path, newline='') as file:
        reader = csv.reader(file)
        next(reader)  # header rowをスキップ
        for row in reader:
            if row[0] == target_date:
                tasks = row
                break
    return tasks


def format_date(input_date_str):
    day_names_kanji = {
        "Sun": "日", "Mon": "月", "Tue": "火",
        "Wed": "水", "Thu": "木", "Fri": "金",
        "Sat": "土",
    }
    date_obj = datetime.datetime.strptime(input_date_str, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%m/%d')
    day_of_week = date_obj.strftime("%a")
    kanji_day = day_names_kanji.get(day_of_week, "Unknown")
    return f"{formatted_date}({kanji_day})"


def create_reports(tasks, main_agenda):
    if not tasks:
        return None, None

    date, start_time, end_time, duration = tasks[:4]
    header = f"{format_date(date)} {start_time}-{end_time} (*{duration.replace(':00', 'h')}*)\n\n"

    agenda = f"作業予定\n{header}"
    report = f"作業時間\n{header}"

    for i in range(4, len(tasks), 3):
        task, detail1, detail2 = tasks[i:i + 3]
        if task:
            agenda += f"* {main_agenda} - {task}\n"
            report += f"* {main_agenda} - {task}\n"
            if detail1:
                report += f"    * {detail1}\n"
            if detail2:
                report += f"    * {detail2}\n"

    report += "\n> 週明けに前週のTimesheetを添付\n"
    report += f"> リアルタイムの工数は[ClickUp Timesheet]({'https://app.clickup.com/9007129404/dashboards/8cdvrtw-63'})で確認可\n"
    report += "> ClickUp ID: clickup@grrow.jp"

    return agenda, report


def write_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)


def main():
    parser = argparse.ArgumentParser(description='Generate daily reports.')
    parser.add_argument('offset', nargs='?', type=int, default=0,
                        help='offset (e.g., -1: 昨日, 1: 明日)')
    parser.add_argument('csv_file', nargs='?', default='./data/daily_report_data.csv',
                        help='CSVファイルの経路')
    args = parser.parse_args()

    target_date = (datetime.date.today() + datetime.timedelta(days=args.offset)).strftime('%Y-%m-%d')
    tasks = read_tasks(args.csv_file, target_date)

    if tasks:
        main_agenda = '*Visionbank*'
        agenda, report = create_reports(tasks, main_agenda)

        write_file('daily_agenda.md', agenda)
        write_file('daily_report.md', report)

        subprocess.run(["open", "daily_agenda.md"])
        subprocess.run(["open", "daily_report.md"])

    else:
        print("データがありません。指定された日が週末か祝日のようです。")


if __name__ == "__main__":
    main()
