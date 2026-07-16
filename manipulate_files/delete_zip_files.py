import os

def delete_zip_files(folder):
    for filename in os.listdir(folder):
        if filename.endswith(".zip"):
            os.remove(os.path.join(folder, filename))
