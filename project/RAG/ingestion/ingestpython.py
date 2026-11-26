from datetime import date
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
PAGES = [
    "https://docs.python.org/3.14/tutorial/introduction.html",
    "https://docs.python.org/3.14/tutorial/controlflow.html",
    "https://docs.python.org/3.14/tutorial/datastructures.html",
    "https://docs.python.org/3.14/tutorial/interpreter.html",
]

BLOCK_TAGS = {"h1", "h2", "h3", "p", "pre", "li"}
PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = PROJECT_ROOT / "rag" / "data" / "python_tutorial_sections.jsonl"


class TutorialParser(HTMLParser):
    def __init__(self, url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.url = url
        self.current_tag: str | None = None
        self.current_depth = 0
        self.buffer: list[str] = []
        self.section = ""
        self.title = url.rsplit("/", 1)[-1]
        self.records: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.current_tag is None and tag in BLOCK_TAGS:
            self.current_tag = tag
            self.current_depth = 1
            self.buffer = []
        elif tag == self.current_tag:
            self.current_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag != self.current_tag:
            return

        self.current_depth -= 1
        if self.current_depth:
            return

        text = " ".join("".join(self.buffer).split())
        block_tag = self.current_tag
        self.current_tag = None
        self.buffer = []

        if not text:
            return

        if block_tag in {"h1", "h2", "h3"}:
            self.section = text
            if block_tag == "h1":
                self.title = text
            return

        self.records.append({
            "title": self.title,
            "url": self.url,
            "section": self.section or self.title,
            "text": text,
            "version": "3.14.10",
            "license": "PSF-2.0",
            "accessed_at": date.today().isoformat(),
        })

    def handle_data(self, data: str) -> None:
        if self.current_tag is not None:
            self.buffer.append(data)


def fetch_page(url: str) -> list[dict[str, str]]:
    request = Request(
        url,
        headers={"User-Agent": "PrepPilot educational research"},
    )
    with urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        html = response.read().decode(charset)
    soup=BeautifulSoup(html,"html.parser")
    main_content=soup.find("div",{"role":"main"})
    if main_content is None:
        raise ValueError(f"Could not find main content in {url}")
    for element in main_content.select("nav,[role='navigation'], .toctree-wrapper,.headerlink"):
        element.decompose()
    parser = TutorialParser(url)
    parser.feed(str(main_content))
    parser.close()
    return parser.records


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    records = []
    for url in PAGES:
        records.extend(fetch_page(url))

    with OUTPUT_PATH.open("w", encoding="utf-8") as output:
        for record in records:
            output.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Saved {len(records)} sections to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()