#!/usr/bin/env python3
"""Add (or replace) a version of a tweak in repo.json from its APK.

    tools/add-version.py dev.novacain.hive path/to/hive.apk \
        https://github.com/novaca1n/hive/releases/download/v0.1/hive-0.1.apk \
        --changelog-en "First release" --changelog-ru "Первый выпуск"

Version name/code come from the APK itself (aapt2 from the Android SDK: $ANDROID_HOME or /mnt/build/android-dev/sdk),
sha256 and size from the file — so they always match what the store downloads.
"""
import argparse, datetime, glob, hashlib, json, os, re, subprocess, sys

def aapt2():
    sdk = os.environ.get("ANDROID_HOME", "/mnt/build/android-dev/sdk")
    found = sorted(glob.glob(os.path.join(sdk, "build-tools", "*", "aapt2")))
    if not found:
        sys.exit("aapt2 not found — set ANDROID_HOME")
    return found[-1]

ap = argparse.ArgumentParser()
ap.add_argument("id"); ap.add_argument("apk"); ap.add_argument("url")
ap.add_argument("--changelog-en", default=""); ap.add_argument("--changelog-ru", default="")
ap.add_argument("--repo", default=os.path.join(os.path.dirname(__file__), "..", "repo.json"))
a = ap.parse_args()

badging = subprocess.run([aapt2(), "dump", "badging", a.apk], capture_output=True, text=True, check=True).stdout
m = re.search(r"package: name='([^']+)' versionCode='(\d+)' versionName='([^']*)'", badging)
if not m:
    sys.exit("can't read the APK")
pkg, code, name = m.group(1), int(m.group(2)), m.group(3)
if pkg != a.id:
    sys.exit(f"APK is {pkg}, not {a.id}")

data = open(a.apk, "rb").read()
version = {"name": name, "code": code, "apk": a.url, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data),
           "date": datetime.date.today().isoformat()}
log = {k: v for k, v in (("en", a.changelog_en), ("ru", a.changelog_ru)) if v}
if log:
    version["changelog"] = log

repo = json.load(open(a.repo, encoding="utf-8"))
tweak = next((t for t in repo["tweaks"] if t["id"] == a.id), None)
if tweak is None:
    sys.exit(f"{a.id} isn't in repo.json yet — add its entry first")
tweak["versions"] = [v for v in tweak.get("versions", []) if v["code"] != code] + [version]
tweak["versions"].sort(key=lambda v: v["code"], reverse=True)
with open(a.repo, "w", encoding="utf-8") as f:
    json.dump(repo, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"{a.id} {name} ({code}) → {a.url}")
