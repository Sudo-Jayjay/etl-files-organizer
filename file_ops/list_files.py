import os
import re

def list_files(folder, pattern=None):
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if pattern:
        files = [f for f in files if re.search(pattern, f)]
    return [os.path.join(folder, f) for f in files]

# Use Case:
# if __name__ == "__main__":
#     files = list_files("folder", pattern=r"\.csv$")
#     for file in files:
#         print(file)