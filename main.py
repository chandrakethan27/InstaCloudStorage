import argparse
import hashlib
import os
import random
import sys
import time
from pathlib import Path

from config import load_credentials
from tracker import Tracker
from uploader import Uploader

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def scan_folder(folder: str) -> list[str]:
    return [
        str(p)
        for p in Path(folder).iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    ]


def compute_md5(filepath: str) -> str:
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def run(folder: str, tracker: Tracker, uploader: Uploader) -> dict:
    files = scan_folder(folder)
    counts = {"uploaded": 0, "skipped": 0, "failed": 0}

    print(f"Found {len(files)} image(s) in {folder}")

    for i, filepath in enumerate(files, 1):
        filename = os.path.basename(filepath)
        try:
            md5 = compute_md5(filepath)
        except OSError as e:
            print(f"  [{i}/{len(files)}] SKIP (unreadable): {filename} — {e}")
            counts["failed"] += 1
            continue

        if tracker.is_uploaded(md5):
            print(f"  [{i}/{len(files)}] SKIP (already uploaded): {filename}")
            counts["skipped"] += 1
            continue

        print(f"  [{i}/{len(files)}] Uploading: {filename}...")
        success = uploader.upload_photo(filepath)

        if success:
            tracker.mark_uploaded(filepath, md5)
            counts["uploaded"] += 1
            print(f"  [{i}/{len(files)}] OK: {filename}")
            if i < len(files):
                delay = random.uniform(30, 60)
                print(f"  Waiting {delay:.0f}s before next upload...")
                time.sleep(delay)
        else:
            counts["failed"] += 1
            print(f"  [{i}/{len(files)}] FAILED: {filename}")

    return counts


def main():
    parser = argparse.ArgumentParser(description="Upload photos to Instagram")
    parser.add_argument("--folder", required=True, help="Path to folder containing photos")
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print(f"Error: folder not found: {args.folder}")
        sys.exit(1)

    try:
        username, password = load_credentials()
    except EnvironmentError as e:
        print(f"Error: {e}")
        print("Copy .env.example to .env and fill in your credentials.")
        sys.exit(1)

    print("Logging in to Instagram...")
    try:
        uploader = Uploader(username, password)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("Login successful.")
    tracker = Tracker()

    try:
        counts = run(args.folder, tracker, uploader)
    finally:
        tracker.close()

    print(f"\nDone. Uploaded: {counts['uploaded']}  Skipped: {counts['skipped']}  Failed: {counts['failed']}")


if __name__ == "__main__":
    main()
