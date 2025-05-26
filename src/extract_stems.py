import subprocess
import sys
from pathlib import Path

from utils import load_config


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def convert_vdjstems_file(vdj_path: Path, output_root: Path) -> None:
    """Convert a single *.vdjstems file to individual FLAC stems.

    The stems are written into a sub-directory named after the source file (without
    extension) inside *output_root*.
    """
    if not vdj_path.exists():
        raise FileNotFoundError(f"{vdj_path} does not exist")

    # Create an output folder per track so files don't collide if names repeat
    track_out_dir = (output_root / vdj_path.stem).resolve()
    track_out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg", "-y",  # "-y" = overwrite silently
        "-i", str(vdj_path),
        "-map", "0:a:0", str(track_out_dir / "Vocals.flac"),
        "-map", "0:a:1", str(track_out_dir / "HiHat.flac"),
        "-map", "0:a:2", str(track_out_dir / "Bass.flac"),
        "-map", "0:a:3", str(track_out_dir / "Melody.flac"),
        "-map", "0:a:4", str(track_out_dir / "Drums.flac"),
    ]

    print(f"[INFO] Converting {vdj_path.name} → {track_out_dir.relative_to(output_root)} …")
    subprocess.run(cmd, check=True)


# ------------------------------------------------------------
# Main entry-point
# ------------------------------------------------------------

def main() -> None:
    config = load_config("extract_stems_config")

    # Directories -----------------------------
    input_dir = Path(config.get("input_files_directory", "downloads")).expanduser().resolve()
    output_dir = Path(config.get("output_directory", "extracted_stems")).expanduser().resolve()

    if not input_dir.exists():
        sys.exit(f"[ERROR] Input directory '{input_dir}' does not exist.")

    output_dir.mkdir(parents=True, exist_ok=True)

    # Gather all *.vdjstems files (recursive) --
    vdj_files = sorted(input_dir.rglob("*.vdjstems"))
    if not vdj_files:
        print("[INFO] No *.vdjstems files found. Nothing to do.")
        return

    print(f"[INFO] Found {len(vdj_files)} vdjstems file(s) in '{input_dir}'.")
    print("\n=== Starting stem extraction … ===\n")

    for vdj_path in vdj_files:
        try:
            convert_vdjstems_file(vdj_path, output_dir)
        except subprocess.CalledProcessError as ex:
            print(f"[ERROR] ffmpeg failed on {vdj_path.name}: {ex}")
        except Exception as ex:
            print(f"[ERROR] {ex}")

    print("\n=== All conversions complete! ===")


if __name__ == "__main__":
    main()
