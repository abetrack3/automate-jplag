import os
import shutil
from typing import List


def remove_generated_artifacts(exclude_result_artifacts: bool = False) -> None:
    print('\n\nRemoving artifacts')

    excluded_directories = ['results'] if exclude_result_artifacts else []

    removable_directories: List[str] = [
        sub_folder for sub_folder in os.listdir()
        if sub_folder.endswith(('UNZIPPED', 'CONVERTED', 'JPLAG SCANNABLE', 'results')) and
        sub_folder not in excluded_directories
    ]

    for removable_directory in removable_directories:

        try:

            shutil.rmtree(removable_directory)

            print(f'Removed: {removable_directory}')

        except OSError:

            pass

    removable_files: List[str] = ['results.jplag']
    excluded_files = ['result.xlsx']

    if exclude_result_artifacts is not True:
        removable_files += excluded_files

    for removable_file in removable_files:

        if os.path.exists(removable_file):
            os.remove(removable_file)

            print(f'Removed: {removable_file}')
