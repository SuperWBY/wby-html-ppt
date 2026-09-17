#!/usr/bin/env python3
"""Create, arrange, validate, build, and preview a static HTML slide studio."""
import argparse
import functools
import html
import http.server
import json
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote

from build import build


ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass
class DeckStudio:
    root: Path

    @property
    def manifest_path(self) -> Path:
        return self.root / "deck.json"

    def load(self) -> dict[str, Any]:
        data = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        slides = data.get("slides")
        if not isinstance(slides, list) or not all(isinstance(item, str) for item in slides):
            raise ValueError("deck.json requires a slides array of relative paths")
        if len(slides) != len(set(slides)):
            raise ValueError("deck.json contains duplicate slide paths")
        for item in slides:
            candidate = (self.root / item).resolve()
            if Path(item).is_absolute() or not candidate.is_relative_to(self.root):
                raise ValueError(f"Slide path leaves this deck: {item}")
        return data

    def save(self, data: dict[str, Any]) -> None:
        if self.manifest_path.exists():
            self.manifest_path.with_suffix(".json.bak").write_bytes(self.manifest_path.read_bytes())
        staged = self.manifest_path.with_suffix(".json.pending")
        staged.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        staged.replace(self.manifest_path)

    def find(self, data: dict[str, Any], query: str) -> tuple[int, str]:
        results = [(index, item) for index, item in enumerate(data["slides"])
                   if item == query or Path(item).stem == query]
        if len(results) != 1:
            raise ValueError(f"Expected one slide named {query!r}; found {len(results)}")
        return results[0]

    def page_path(self, item: str) -> Path:
        path = (self.root / item).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError("Slide path leaves this deck")
        return path

    def initialize(self, title: str) -> dict[str, Any]:
        self.root.mkdir(parents=True, exist_ok=True)
        if self.manifest_path.exists():
            raise ValueError("deck.json already exists; inspect it with status")
        (self.root / "slides").mkdir(exist_ok=True)
        (self.root / "assets").mkdir(exist_ok=True)
        self.save({"title": title, "slides": []})
        return {"project": str(self.root), "pages": 0}

    def add(self, page_id: str, title: str, after: str | None) -> dict[str, Any]:
        if not ID.fullmatch(page_id):
            raise ValueError("Slide IDs use lowercase letters, digits, and hyphens")
        data = self.load()
        item = f"slides/{page_id}.html"
        path = self.page_path(item)
        if item in data["slides"] or path.exists():
            raise ValueError("That slide already exists")
        position = len(data["slides"])
        if after:
            position = self.find(data, after)[0] + 1
        path.parent.mkdir(parents=True, exist_ok=True)
        escaped = html.escape(title)
        path.write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{escaped}</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ width: 1920px; height: 1080px; margin: 0; overflow: hidden; font-family: Arial, sans-serif; }}
  main {{ padding: 80px; }} h1 {{ font-size: 64px; }}
</style></head><body><main data-wby-draft><h1>{escaped}</h1>
<!-- Design this slide for its speaking goal, then remove data-wby-draft. -->
</main></body></html>''', encoding="utf-8")
        data["slides"].insert(position, item)
        self.save(data)
        return {"path": str(path), "position": position + 1, "draft": True}

    def reorder(self, page_id: str, destination: int) -> dict[str, Any]:
        data = self.load()
        if not 1 <= destination <= len(data["slides"]):
            raise ValueError("Destination must be between 1 and the page count")
        index, item = self.find(data, page_id)
        data["slides"].pop(index)
        data["slides"].insert(destination - 1, item)
        self.save(data)
        return {"slides": data["slides"]}

    def unlist(self, page_id: str) -> dict[str, Any]:
        data = self.load()
        index, item = self.find(data, page_id)
        data["slides"].pop(index)
        self.save(data)
        return {"slides": data["slides"], "source_preserved": str(self.page_path(item))}

    def status(self) -> dict[str, Any]:
        data = self.load()
        pages = []
        for number, item in enumerate(data["slides"], 1):
            path = self.page_path(item)
            source = path.read_text(encoding="utf-8") if path.is_file() else ""
            match = re.search(r"<title[^>]*>(.*?)</title>", source, re.I | re.S)
            pages.append({"page": number, "path": item, "exists": path.is_file(),
                          "draft": "data-wby-draft" in source,
                          "title": html.unescape(match.group(1)) if match else ""})
        return {"title": data.get("title", ""), "pages": pages,
                "next_review": "Inspect layout and interaction in a browser; static status cannot judge visual quality."}

    def ready(self) -> dict[str, Any]:
        data = self.load()
        for item in data["slides"]:
            path = self.page_path(item)
            if not path.is_file():
                raise ValueError(f"Missing slide source: {item}")
            if "data-wby-draft" in path.read_text(encoding="utf-8"):
                raise ValueError(f"Unfinished scaffold: {item}")
        return data

    def check(self) -> dict[str, Any]:
        data = self.ready()
        with tempfile.TemporaryDirectory() as temporary:
            result = build(self.root, self.manifest_path, Path(temporary) / "checked.html")
        return {"pages": len(data["slides"]), "embedded_assets": result["assets"],
                "packaging": "passed", "browser_review": "Still required for layout, controls, and reduced motion."}

    def build(self, output: Path | None) -> dict[str, Any]:
        self.ready()
        return build(self.root, self.manifest_path, output or self.root / "dist/presentation.html")


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "add", "move", "remove", "status", "check", "build", "preview"):
        command = commands.add_parser(name)
        command.add_argument("project", type=Path)
        if name == "init":
            command.add_argument("--title", default="Untitled presentation")
        if name == "add":
            command.add_argument("id")
            command.add_argument("--title", required=True)
            command.add_argument("--after")
        if name in ("move", "remove"):
            command.add_argument("id")
        if name == "move":
            command.add_argument("--to", type=int, required=True)
        if name in ("build", "preview"):
            command.add_argument("--output", type=Path)
        if name == "preview":
            command.add_argument("--port", type=int, default=4173)
    return parser.parse_args()


def main() -> None:
    args = arguments()
    studio = DeckStudio(args.project.resolve())
    try:
        if args.command == "init": result = studio.initialize(args.title)
        elif args.command == "add": result = studio.add(args.id, args.title, args.after)
        elif args.command == "move": result = studio.reorder(args.id, args.to)
        elif args.command == "remove": result = studio.unlist(args.id)
        elif args.command == "status": result = studio.status()
        elif args.command == "check": result = studio.check()
        elif args.command == "build": result = studio.build(args.output.resolve() if args.output else None)
        else:
            built = studio.build(args.output.resolve() if args.output else None)
            handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(Path(built["file"]).parent))
            with http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
                print(json.dumps({"preview": f"http://127.0.0.1:{server.server_port}/{quote(Path(built['file']).name)}", "note": "Local preview only. Rebuild after edits; Ctrl+C stops the server."}), flush=True)
                try: server.serve_forever()
                except KeyboardInterrupt: pass
            result = {"preview": "stopped"}
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as error:
        raise SystemExit(f"Failed: {error}")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
