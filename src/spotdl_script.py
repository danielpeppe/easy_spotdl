import subprocess
from pathlib import Path
import sys
from utils import load_config


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
    
    output_dir = (Path(__file__).parent.parent / config.get("output_directory", "downloads")).resolve()
    cmd = [
        sys.executable, "-m", "spotdl",
        "download",
        link,
        "--audio", config.get("audio_source", "youtube-music"),
        "--format", config.get("file_format", "flac"),
        "--output", output_dir,
    ]

    # Execute the command
    subprocess.run(cmd, check=True)


def main():
    config = load_config("spotdl_config")
    input_file = config.get("input_file", "spotify_links.txt")
    txt_path = (Path(__file__).parent.parent / input_file).resolve()

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



