from rich import print
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.console import Group
import json
import argparse


def get_data() -> dict:
    """Read JSON data from argument.

    Returns:
        A dict value holding the JSON outline
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('outline_file', help='outline JSON file')
    args = parser.parse_args()
    with open(args.outline_file) as f:
        data: dict = json.load(f)

    return data


def get_details(outline: dict) -> dict:
    """Get relevant details from outline.

    Extract and format relevant fields from outline in a dict object.

    Args:
        outline: course outline as a json object

    Returns:
        A dict mapping course details with their values. If a detail was not
        found in the outline it will be added as a key mapped to a default
        value.
    """
    info: dict           = outline.get("info", dict())
    instructors: list    = outline.get("instructor", list())
    courseSchedule: list = outline.get("courseSchedule", list())
    # get details from info object
    details = dict()
    details["name"]         = info.get("name", "")
    details["units"]        = info.get("units", "")
    details["title"]        = info.get("title", "")
    details["term"]         = info.get("term", "")
    details["desc"]         = info.get("description", "")
    details["wqb"]          = info.get("designation", "")
    details["specialTopic"] = info.get("specialTopic", "")
    if details["wqb"] == "N/A":
        details["wqb"] = ""
    details["prerequisites"] = info.get("prerequisites", "")
    # get instructor(s) from instructors list
    details["instructor"] = ", ".join(i.get("name", "")
                                         for i in instructors if "name" in i)
    details["link"] = f"http://www.sfu.ca/outlines.html?{info.get('outlinePath')}"
    # get schedule from courseSchedule object
    details["schedule"] = list()
    for day in courseSchedule:
        if daynames := day.get("days", ""):
            for dayname in daynames.split(","):
                details["schedule"].append(dict())
                details["schedule"][-1]["day"] = dayname.strip()
                details["schedule"][-1]["location"] = \
                    day.get("buildingCode", "") + day.get("roomNumber", "")
                details["schedule"][-1]["startTime"] = day.get("startTime", "")
                details["schedule"][-1]["endTime"] = day.get("endTime", "")
                details["schedule"][-1]["sectionCode"] = \
                    day.get("sectionCode", "")

    return details


def get_title_panel(details: dict) -> Panel:
    """Get a panel containing the title of the course.

    Displays the title info consistent with the format found in the web view
    (i.e. http://www.sfu.ca/outlines.html?2023/fall/cmpt/450/d100):

        <term> - <name>
        <title> (<units>)

    Args:
        details: A dict mapping course details with their values.

    Returns:
        A rich.panel.Panel containing the course title.
    """
    lines = [
        f'{details.get("term", "")} - {details.get("name", "")}',
        f'{details.get("title", "")} ({details.get("units", "")})',
    ]
    if details["specialTopic"]:
        lines.append(details["specialTopic"])
    return Panel.fit(
        "\n".join(lines),
        style="bold"
    )


def get_week_table(schedule: list) -> Table | None:
    """Get a week table from courseSchedule list object

    Format courseSchedule as a table representing a week view of the course.

    Args:
        schedule: courseSchedule list object

    Returns:
        A dict a table representing a week view of the course. If schedule is
        an empty list return None.
    """
    if not schedule:
        return None

    week_table = Table()
    classes = dict()

    # initialize week
    for day in ["Mo", "Tu", "We", "Th", "Fr"]:
        week_table.add_column(day, justify="center", min_width=7)
        classes[day] = None

    # the earliest start time is needed for aligning multiple days according to
    # their times like a typical week view on a calendar
    earliest_start = min(int(day['startTime'].split(":")[0]) 
                         for day in schedule)
    for day in schedule:
        start    = f"{day['startTime']}"
        end      = f"{day['endTime']}"
        start_hr = int(start.split(":")[0])
        end_hr   = int(end.split(":")[0])
        duration = end_hr - start_hr
        newline  = "\n" # f-strings can't contain backslashes
        classes[day["day"]] = Group(
            day["location"],
            f"{newline * (start_hr - earliest_start)}",
            Text(f" {start} {newline * duration} {end} ", style="on #a6192e")
        )

    week_table.add_row(*classes.values())

    return week_table


def get_details_table(details: dict) -> Table:
    """Get a table containing the course details.

    Args:
        details: A dict mapping course details with their values.

    Returns:
        A rich.table.Table containing course details.
    """
    table = Table(
        show_header=False,
        show_lines=True,
        caption=Text.assemble("Web view: ", (f"{details['link']}", "blue"))
    )

    table.add_column("Key",   style="bold #a6192e")
    table.add_column("Value", max_width=70)

    if details["desc"]:
        table.add_row("Description", details["desc"] + " " + details["wqb"])
    if details["prerequisites"]:
        table.add_row("Prerequisites", details["prerequisites"])
    if details["instructor"]:
        table.add_row("Instructor", details["instructor"])
    if details["schedule"]:
        table.add_row("Schedule", get_week_table(details["schedule"]))

    return table


def main():
    data          = get_data()
    details       = get_details(data)
    title_panel   = get_title_panel(details)
    details_table = get_details_table(details)

    print(Panel.fit(Group(title_panel, details_table)))


if __name__ == '__main__':
    main()
