from rich import print
from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.style import Style
from rich.console import Group
from rich.markdown import Markdown
from rich.bar import Bar
import sys
import json 

SFU_RED = "#a6192e"
DEFAULT = "default"
key_style = Style(color="yellow", bold=True)
name_style = Style(bold=True)

with open(sys.argv[1]) as f:
    data = json.load(f)

if type(data) == list:
    print("Not enough data")
    print(data)
    exit(1)
details = dict()
# details["Instructor"] = data.get("instructor").get("name")
# COURSE INFO PANEL
info = data.get("info")
# link_style = Style(color="#a6192e", bold=True, link=link)
course_name = Text(f'{info.get("name")} ({info.get("units")})', style=name_style)
course_title = Markdown(f"## {info.get('title')}")
info_keys = {
    "Term": "term",
    # "Title": "title",
    "WQB": "designation",
    "Delivery": "deliveryMethod",
    "Prereqs": "prerequisites",
}
for k, v in info_keys.items():
    details[k] = info.get(v)

courseSchedule = data.get("courseSchedule")
if courseSchedule:
    campus = courseSchedule[0].get("campus")
if campus:
    details["Campus"] = campus
else:
    details["Campus"] = "N/A"

# INSTRUCTOR PANEL
table = Table(show_header=False, box=None)
table.add_column("Key")
table.add_column("Value")

table.add_row("", "") # padding
for k,v in details.items():
    table.add_row(Text(k, style=key_style), Text(v))

table.add_row("", "") # padding

# SCHEDULE

sched = Table(title="Schedule", title_justify="left", 
        leading=True)

for day in ["Mo", "Tu", "We", "Th", "Fr"]:
    sched.add_column(day, justify="center", style=f"on {DEFAULT}",
            max_width=10, min_width=10)

sched.add_row(
    None,
    Text("10:30\n\n12:20", style=f"on {SFU_RED}"),
    None,
    Text("10:30\n11:20", style=f"on {SFU_RED}"),
    None,
    # Text("test", style=f"white on {SFU_RED}", justify="left"),
    # None,
    # Text("to", style=f"default on default", justify="left"),
    # Text("test", style=f"white on {SFU_RED}", justify="left"),
    # None,
    # Text("test", style=f"white on {SFU_RED}", justify="left"),
)

link = f"http://www.sfu.ca/outlines.html?{info.get('outlinePath')}"
# outline_link = Markdown(f"---\n\n[{link}]({link})")
outline_link = Text(f"{link}", style="blue")

group = Group(
    course_title,
    table,
    sched,
    # outline_link,
)

print(Panel(group, title=course_name, title_align="left", expand=False, 
    subtitle=outline_link, subtitle_align="left", box=box.HEAVY))
# TODO: check https://excalidraw.com/#json=x9-Ji-YybrRFIHFWa1e6E,hBs8lWHvyEnOGA04GAP2vg

