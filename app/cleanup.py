import os, shutil
from typing import List


def remove_generated_artifacts(exclude_result_artifacts: bool = False) -> None:

    print('\n\nRemoving artifacts')

    removable_directories: List[str] = filter(
        lambda sub_folder: sub_folder.endswith(
            ('UNZIPPED',
            'CONVERTED',
            'JPLAG SCANNABLE',
            'result'),
            ),
        os.listdir(),
    )

    for removable_directory in removable_directories:
        
        try:
        
            shutil.rmtree(removable_directory)

            print(f'Removed: {removable_directory}')
        
        except Exception:
        
            pass

    if exclude_result_artifacts is True:

        return    

    removable_files: List[str] = ['result.zip', 'result.xlsx']

    for removable_file in removable_files:

        if os.path.exists(removable_file):

            os.remove(removable_file)

            print(f'Removed: {removable_file}')
            

    