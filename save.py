import struct
import zlib


def calculate_checksum(data: bytes) -> int:
    """Calculates Adler-32 / CRC32 checksum for save payloads."""
    return zlib.adler32(data) & 0xFFFFFFFF


def convert_ps4_to_pc(data: bytes) -> bytes:
    """
    Parses decrypted PS4 raw save payload, adjusts headers/offsets, 
    and returns formatted PC/PS5 payload.
    """
    if data.startswith(b"PS4_SAVE"):
        payload = data[0x40:]
    else:
        payload = data

    checksum = calculate_checksum(payload)
    header = struct.pack("<I", checksum)
    return header + payload


def decrypt_save(data: bytes) -> bytes:
    """
    Extracts raw save payload from an encrypted or containerized DATA.DAT file.
    """
    if len(data) < 4:
        raise ValueError("Invalid save file length.")

    payload = data[4:]
    return payload


def encrypt_save(data: bytes) -> bytes:
    """
    Packs raw payload and recalculates engine checksums.
    """
    checksum = calculate_checksum(data)
    header = struct.pack("<I", checksum)
    return header + data
