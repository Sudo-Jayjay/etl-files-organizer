import shutil
import os
import re
import fnmatch

def move_files(source_folder, destination_folder, pattern="*", use_regex=True):
    for filename in os.listdir(source_folder):
        matched = re.search(pattern, filename) if use_regex else fnmatch.fnmatch(filename, pattern)
        if matched:
            shutil.move(os.path.join(source_folder, filename), os.path.join(destination_folder, filename))

if __name__ == "__main__":
    move_files(r"C:\Users\VERZ0003\OneDrive - Bon Secours Mercy Health\Documents\arrived_files", r"\\mdcofs900011\corpshared$\NetMgt\Managed Care Analytics\Reporting\SQL Scripts\Physician Monthly Data Import Process\prod_01__PHYSICIAN_CONSOL_BSMH\LkpTables\PlanIndexes\weekly_new_plans\01_mapped_weekly_plans", pattern="*.csv", use_regex=False)