import subprocess
from pathlib import Path
import sys
import yaml

# Path to config file and default input fallback
CONFIG_PATH = Path(__file__).with_name("config.yaml")

def load_config(config_path: Path):
    if not config_path.exists():
        sys.exit(f"[ERROR] Config file '{config_path.name}' not found.")
    with config_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def read_links(txt_path: Path):
    if not txt_path.exists():
        sys.exit(f"[ERROR] '{txt_path.name}' not found in the workspace.")
    with txt_path.open(encoding="utf-8") as fp:
        for line in fp:
            link = line.strip()
            if link and link.startswith("https://open.spotify.com/"):
                yield link
            elif link:
                print(f"[SKIP] Not a valid Spotify link: {link}")

def download(link: str, config: dict):
    cmd = [
        sys.executable, "-m", "spotdl",
        "download",
        link,
        "--audio", config.get("audio_source", "youtube"),
        "--format", config.get("file_format", "mp3"),
        "--output", config.get("output_directory", "downloads"),
    ]

    # Execute the command
    subprocess.run(cmd, check=True)

def main():
    config = load_config(CONFIG_PATH)
    input_file = config.get("input_file", "spotify_links.txt")
    txt_path = Path(__file__).with_name(input_file)

    links = list(read_links(txt_path))
    if not links:
        print("[INFO] No valid Spotify links found in the input file.")
        input("Press Enter to close...")  # Keeps the terminal open
        sys.exit(0)
    else:
        print(f"[INFO] Found {len(links)} valid Spotify links.")
    print("\n=== Starting downloads... ===\n")

    for link in links:
        download(link, config)

    print("\n=== All downloads completed! ===")
    sys.exit(0)

if __name__ == "__main__":
    main()
