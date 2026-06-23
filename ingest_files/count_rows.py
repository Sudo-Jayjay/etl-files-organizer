import mmap
import time

def count_lines(filepath: str) -> int:
    """Count lines using memory-mapped file access with timing diagnostics."""

    print("[...] Opening file...")
    t0 = time.perf_counter()
    f = open(filepath, "rb")
    print(f"[OK] File opened in {time.perf_counter() - t0:.2f}s")

    print("[...] Mapping file...")
    t1 = time.perf_counter()
    mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    print(f"[OK] File mapped in {time.perf_counter() - t1:.2f}s")

    print("[...] Counting lines...")
    t2 = time.perf_counter()
    count = mm.read().count(b"\n")
    print(f"[OK] Lines counted in {time.perf_counter() - t2:.2f}s")

    mm.close()
    f.close()
    return count