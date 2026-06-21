from .imports import *

def _move_item(item: Path, target: Path, overwrite: bool) -> Path | None:
    """Moves a single item to target, respecting the overwrite flag. O(1)"""
    if target.exists():
        if not overwrite:
            print(f"[mover] [SKIP] Skipped (already exists): {item.name}")
            return None
        shutil.rmtree(target) if target.is_dir() else target.unlink()

    shutil.move(str(item), str(target))
    print(f"[mover] [OK] {item.name} -> {target}")
    return target


def move_files(source_dir: str, destination_dir: str, overwrite: bool = False, cleanup: bool = False) -> list[Path]:
    """Moves all items from source_dir to destination_dir, skipping destination if nested inside source. O(n)"""
    source = Path(source_dir).resolve()
    destination = Path(destination_dir).resolve()

    if not source.is_dir():
        raise NotADirectoryError(f"[mover] Directory not found: '{source_dir}'")

    destination.mkdir(parents=True, exist_ok=True)

    moved = [
        result
        for item in source.iterdir()
        if item.resolve() != destination
        for result in [_move_item(item, destination / item.name, overwrite)]
        if result is not None
    ]

    if cleanup and source.exists():
        shutil.rmtree(source)
        print(f"[mover] [CLEANUP] Deleted source folder: {source}")

    return moved