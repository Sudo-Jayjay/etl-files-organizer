import shutil
import os
import re
import fnmatch

def move_files(source_folder, destination_folder, pattern="*", use_regex=False):
    for filename in os.listdir(source_folder):
        matched = re.search(pattern, filename) if use_regex else fnmatch.fnmatch(filename, pattern)
        if matched:
            shutil.move(os.path.join(source_folder, filename), os.path.join(destination_folder, filename))
