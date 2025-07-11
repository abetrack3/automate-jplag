import os
import shutil
from typing import List


def remove_generated_artifacts(exclude_result_artifacts: bool = False) -> None:
    print('\n\nRemoving artifacts')

    removable_directories: List[str] = [
        sub_folder for sub_folder in os.listdir()
        if sub_folder.endswith(('UNZIPPED', 'CONVERTED', 'JPLAG SCANNABLE', 'results'))
    ]

    for removable_directory in removable_directories:

        try:

            shutil.rmtree(removable_directory)

            print(f'Removed: {removable_directory}')

        except OSError:

            pass

    if exclude_result_artifacts:
        return

    removable_files: List[str] = ['results.jplag', 'result.xlsx']

    for removable_file in removable_files:

        if os.path.exists(removable_file):
            os.remove(removable_file)

            print(f'Removed: {removable_file}')
