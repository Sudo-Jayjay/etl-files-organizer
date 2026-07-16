import zipfile
import os

def unzip_files(source_folder, destination_folder):
    for filename in os.listdir(source_folder):
        if filename.endswith(".zip"):
            with zipfile.ZipFile(os.path.join(source_folder, filename)) as zf:
                zf.extractall(destination_folder)
