import os
import calendar
from datetime import date


def suffix(d):
    return "th" if 11 <= d <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(d % 10, "th")


def custom_strftime(date, format):
    return date.strftime(format).replace("{S}", str(date.day) + suffix(date.day))


def main(args):
    diary_md = f"{args.name}.md"
    if args.index:
        index_to_diary = os.path.join(args.name, diary_md)
        if not os.path.exists(args.index):
            with open(args.index, "x", encoding="utf8") as index_file:
                index_file.write(f"# {args.index.split('.')[0]}\n")
                index_file.write(f"\n- ## [{args.name}]({index_to_diary})\n")
        else:
            with open(args.index, "a", encoding="utf8") as index_file:
                if not os.path.exists(args.name):
                    index_file.write(f"\n## [{args.name}]({index_to_diary})\n")

        diary_to_index = f"[{args.index.split('.')[0]}](../{args.index}) · "
        year_to_index = f"[{args.index.split('.')[0]}](../{args.index}) · "
        month_to_index = f"[{args.index.split('.')[0]}](../../{args.index}) · "
        day_to_index = f"[{args.index.split('.')[0]}](../../../{args.index}) · "
    else:
        diary_to_index = ""
        year_to_index = ""
        month_to_index = ""
        day_to_index = ""

    os.makedirs(args.name, exist_ok=True)
    if not os.path.exists(os.path.join(args.name, diary_md)):
        with open(
            os.path.join(args.name, diary_md), "x", encoding="utf8"
        ) as diary_file:
            diary_file.write(f"# {diary_to_index}{args.name}\n")

    with open(os.path.join(args.name, diary_md), "a", encoding="utf8") as diary_file:
        for year in args.years:
            year_folder = os.path.join(args.name, str(year))
            try:
                os.makedirs(year_folder, exist_ok=False)
            except OSError:
                print(f"{year} already exists in {args.name}")
                continue

            year_md = f"{year}.md"
            diary_file.write(f"\n- ## [{year}]({year_md})\n")

            year_path = os.path.join(args.name, year_md)
            with open(year_path, "x", encoding="utf8") as year_file:
                year_file.write(
                    f"# {year_to_index}[{args.name}]({diary_md}) · {date.strftime(date(year, 1, 1), '%Y')}\n"
                )

                for month in range(1, 13):
                    month_numbered = date.strftime(date(year, month, 1), "%m-%B")
                    month_md = f"{month_numbered}.md"
                    year_to_month = os.path.join(str(year), month_md)
                    year_file.write(
                        f"\n- ## [{date.strftime(date(year, month, 1), '%B')}]({year_to_month})\n"
                    )

                    if args.daily:
                        month_folder = os.path.join(year_folder, month_numbered)
                        os.makedirs(month_folder, exist_ok=False)

                    month_path = os.path.join(year_folder, month_md)
                    with open(month_path, "x", encoding="utf8") as month_file:
                        month_file.write(
                            f"# {month_to_index}[{args.name}](../{diary_md}) · [{year}](../{year_md}) · {date.strftime(date(year, month, 1), '%B')}\n"
                        )

                        for day in calendar.Calendar().itermonthdates(year, month):
                            if day.month == month:
                                if args.daily:
                                    day_md = f"{custom_strftime(day, '{S}')}.md"
                                    month_to_day = os.path.join(month_numbered, day_md)
                                    month_file.write(
                                        f"\n- ## [{custom_strftime(day, '%A {S}')}]({month_to_day})\n"
                                    )

                                    day_path = os.path.join(month_folder, day_md)
                                    with open(
                                        day_path, "x", encoding="utf8"
                                    ) as day_file:
                                        day_file.write(
                                            f"# {day_to_index}[{args.name}](../../../{diary_md}) · [{year}](../../{year_md}) · [{date.strftime(date(year, month, 1), '%B')}](../{month_md}) · {custom_strftime(day, '%A {S}')}\n"
                                        )
                                else:
                                    month_file.write(
                                        f"\n> ## {custom_strftime(day, '%A {S}')}\n"
                                    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Markdown Diary", add_help=False)

    required = parser.add_argument_group("Required Arguments")
    required.add_argument("-n", "--name", help="Diary Name", required=True)

    optional = parser.add_argument_group("Optional Arguments")
    optional.add_argument(
        "-h", "--help", action="help", help="show this help message and exit"
    )
    optional.add_argument(
        "-y",
        "--years",
        help="Diary Year(s) (default is current year)",
        nargs="+",
        default=[date.today().year],
        type=int,
    )
    optional.add_argument(
        "-d",
        "--daily",
        action="store_true",
        help="Create file per day (default is file per month)",
    )
    optional.add_argument(
        "-i",
        "--index",
        help="Use index file (off by default, Index.md if turned on but not specified)",
        nargs="?",
        const="Index.md",
    )

    main(parser.parse_args())
