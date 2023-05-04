from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from rich.markdown import Markdown
from rich.console import Console

console = Console()


frame_style = Style(frame=True)

text = Text("hello word", style="encircle")
console.print(text)
