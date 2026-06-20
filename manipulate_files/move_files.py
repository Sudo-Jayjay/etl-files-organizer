from imports import *

load_dotenv()
src = os.getenv("SRC")
dst = os.getenv("DST")

for file in os.listdir(src):
    src_path = os.path.join(src, file)
    if os.path.isfile(src_path):
        shutil.move(src_path, dst)
        print(f"Moved: {file}")

print("Done!")