"""
initiate_zip_files/unzip.py — Extracts all ZIP files from a source directory.
"""
from .imports import *

def _extract_zip(zip_path: Path, destination: Path, cleanup: bool = False) -> Path | None:
    """Extracts a single ZIP to destination, optionally deletes the ZIP after. O(1)"""
    destination.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(destination)
        print(f"[unzip] [OK] {zip_path.name} -> {destination}/")

        if cleanup:
            zip_path.unlink()
            print(f"[unzip] [CLEANUP] Deleted: {zip_path.name}")

        return destination
    except zipfile.BadZipFile:
        print(f"[unzip] [FAIL] Skipped (corrupt ZIP): {zip_path.name}")
        return None
    except Exception as e:
        print(f"[unzip] [FAIL] {zip_path.name}: {e}")
        return None


def unzip_all(source_dir: str, extract_dir: str = None, cleanup: bool = False) -> list[Path]: # type: ignore
    """Extracts all ZIPs in source_dir, optionally deletes ZIPs after extraction. O(n)"""
    source = Path(source_dir)

    if not source.is_dir():
        raise NotADirectoryError(f"[unzip] Directory not found: '{source_dir}'")

    zip_files = list(source.glob("*.zip"))

    if not zip_files:
        print(f"[unzip] No ZIP files found in '{source_dir}'.")
        return []

    return [
        result
        for zip_path in zip_files
        for result in [
            _extract_zip(
                zip_path=zip_path,
                destination=Path(extract_dir) if extract_dir else source / zip_path.stem,
                cleanup=cleanup,
            )
        ]
        if result is not None
    ]