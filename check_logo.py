from pathlib import Path

print("Current folder:", Path.cwd())

print("Root logo exists:", Path("logo.jpeg").exists())

print("Assets logo exists:", Path("assets/logo.jpeg").exists())

print("Assets folder exists:", Path("assets").exists())

if Path("assets").exists():
    print("\nContents of assets:")
    for f in Path("assets").iterdir():
        print("-", f.name)