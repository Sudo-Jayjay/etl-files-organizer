import shutil
import os

def move_files(source_folder, destination_folder):
    for filename in os.listdir(source_folder):
        shutil.move(os.path.join(source_folder, filename), os.path.join(destination_folder, filename))
