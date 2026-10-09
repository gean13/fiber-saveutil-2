import argparse
import os
import re
from pathlib import Path

# Imports the save.py helper module
import save


def convert_save(src_path: Path, dst_path: Path, target_platform: str = "pc", target_size: int = 4896):
    """
    Converts decrypted PS4 saves to PC or PS5 compatible saves.
    Pads or truncates output containers to match PS5 Garlic Save Manager slot allocations if requested.
    """
    dst_path.mkdir(parents=True, exist_ok=True)

    for root, _, files in os.walk(src_path):
        for file in files:
            if file.endswith(".DAT"):
                file_path = Path(root) / file
                
                # Raw string fix for Python regex warning
                n = re.search(r"(DATA\d\d|SYSTEM)", file_path.parent.name.upper())
                if not n:
                    continue
                
                slot_name = n.group(1)
                out_dir = dst_path / slot_name
                out_dir.mkdir(parents=True, exist_ok=True)
                out_file = out_dir / "DATA.DAT"

                print(f"Converting {file_path} -> {out_file} (Target: {target_platform.upper()})")

                with open(file_path, "rb") as f:
                    data = f.read()

                converted_data = save.convert_ps4_to_pc(data)

                # Apply PS5 byte padding/truncation if targeting PS5
                if target_platform.lower() == "ps5":
                    current_len = len(converted_data)
                    if current_len < target_size:
                        converted_data = converted_data + b"\x00" * (target_size - current_len)
                    elif current_len > target_size:
                        converted_data = converted_data[:target_size]

                with open(out_file, "wb") as f:
                    f.write(converted_data)


def dump_save(file_path: Path, raw: bool = False, target_platform: str = "pc", target_size: int = 4896):
    """
    Decrypts/dumps or encrypts/packs a P5R save file.
    """
    with open(file_path, "rb") as f:
        data = f.read()

    if raw:
        output_data = save.decrypt_save(data)
        out_file = file_path.with_suffix(".decrypted.DAT")
    else:
        output_data = save.encrypt_save(data)
        
        # Apply PS5 byte padding if encrypting/packing for Garlic Save Manager
        if target_platform.lower() == "ps5":
            current_len = len(output_data)
            if current_len < target_size:
                output_data = output_data + b"\x00" * (target_size - current_len)
            elif current_len > target_size:
                output_data = output_data[:target_size]

        out_file = file_path.with_suffix(".encrypted.DAT")

    with open(out_file, "wb") as f:
        f.write(output_data)

    print(f"Processed save saved to: {out_file}")


def main():
    parser = argparse.ArgumentParser(description="Persona 5 Royal PC & PS5 Save Utility")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Convert Command
    convert_parser = subparsers.add_parser("convert", help="Convert PS4 saves to PC/PS5 format")
    convert_parser.add_argument("src", type=Path, help="Path to input PS4 save directory")
    convert_parser.add_argument("dst", type=Path, help="Path to output save directory")
    convert_parser.add_argument(
        "--target-platform",
        choices=["pc", "ps5"],
        default="pc",
        help="Target platform format (default: pc)",
    )
    convert_parser.add_argument(
        "--size",
        type=int,
        default=4896,
        help="Target PS5 Garlic Save Manager container size in bytes (default: 4896)",
    )

    # Dump Command
    dump_parser = subparsers.add_parser("dump", help="Decrypt or encrypt PC/PS5 saves")
    dump_parser.add_argument("file", type=Path, help="Path to target DATA.DAT save file")
    dump_parser.add_argument("--raw", action="store_true", help="Dump raw decrypted payload")
    dump_parser.add_argument(
        "--target-platform",
        choices=["pc", "ps5"],
        default="pc",
        help="Target platform format when re-packing (default: pc)",
    )
    dump_parser.add_argument(
        "--size",
        type=int,
        default=4896,
        help="Target PS5 container byte size when repacking (default: 4896)",
    )

    args = parser.parse_args()

    if args.command == "convert":
        convert_save(args.src, args.dst, target_platform=args.target_platform, target_size=args.size)
    elif args.command == "dump":
        dump_save(args.file, raw=args.raw, target_platform=args.target_platform, target_size=args.size)


if __name__ == "__main__":
    main()
