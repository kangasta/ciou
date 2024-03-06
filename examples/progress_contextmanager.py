from ciou.progress import Progress
from requests import get

p = Progress()
p.start()

with p.task("GET github.com"):
    get("https://github.com")

p.stop()
