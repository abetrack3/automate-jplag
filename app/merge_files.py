import os
from typing import List

def get_merged_solution_code(source_directory: str) -> str:

    solution_code: List[str] = []

    for current_path, _, files in os.walk(source_directory):

        if 'MACOSX' in current_path:
            
            continue


        for each_file_name in files:

            if each_file_name.endswith('.py') is not True:

                continue

            current_file_path: str = os.path.join(current_path, each_file_name)

            with open(file=current_file_path, mode='r') as input_file_object:

                subtask_solution: str = input_file_object.read()

                solution_code.append(subtask_solution)
    
    merged_solution_code: str = '\n\n'.join(solution_code)

    return merged_solution_code


def merge_each_student_suibmissions(source_directory: str, destination_directory: str) -> None:

    if os.path.exists(destination_directory) is not True:
        
        os.makedirs(destination_directory)

    student_submission_folder_names: List[str] = os.listdir(source_directory)

    for each_submission_folder in student_submission_folder_names:

        merged_solution_code: str = get_merged_solution_code(os.path.join(source_directory, each_submission_folder))

        merged_solution_file_path: str = os.path.join(destination_directory, each_submission_folder + '.py')

        with open(merged_solution_file_path, 'w') as output_file_object:

            output_file_object.write(merged_solution_code)

            print(f'Merged submission: {merged_solution_file_path}')
