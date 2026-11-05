"""Download the external files declared in data/MANIFEST.json and verify sha256.

The rule this enforces: large data never lives in git, but the reader can still
prove that what they downloaded is byte-identical to what the paper used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "MANIFEST.json"


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser(description="download external data files")
    ap.add_argument("--manifest", default=str(MANIFEST))
    ap.add_argument("--dest", default=str(ROOT / "data" / "raw"))
    ap.add_argument("--force", action="store_true", help="re-download even if present")
    args = ap.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    files = manifest.get("files", [])
    if not files:
        print("manifest has no files; nothing to do")
        return

    dest = Path(args.dest)
    dest.mkdir(parents=True, exist_ok=True)
    failures = []

    for item in files:
        name = item["name"]
        target = dest / name
        expected = item.get("sha256", "").lower()

        if name.startswith("REPLACE_ME") or "XXXXXXX" in item.get("url", ""):
            print("[todo] manifest still holds the placeholder entry - edit data/MANIFEST.json")
            continue

        if target.exists() and not args.force:
            actual = sha256_of(target)
            status = "ok" if (not expected or actual == expected) else "SHA MISMATCH"
            print(f"[skip] {name}  {status}")
            if status != "ok":
                failures.append(name)
            continue

        print(f"[get ] {name}  <- {item['url']}")
        try:
            urllib.request.urlretrieve(item["url"], target)
        except Exception as exc:  # noqa: BLE001 - report and keep going
            print(f"       failed: {exc}")
            failures.append(name)
            continue

        actual = sha256_of(target)
        if expected and actual != expected:
            print(f"       SHA MISMATCH\n         expected {expected}\n         got      {actual}")
            failures.append(name)
        else:
            print(f"       ok  size={target.stat().st_size}  sha256={actual[:16]}...")

    if failures:
        sys.exit(f"{len(failures)} file(s) failed: {', '.join(failures)}")
    print("all files verified")


if __name__ == "__main__":
    main()
