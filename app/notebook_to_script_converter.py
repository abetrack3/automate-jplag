from concurrent.futures import ThreadPoolExecutor
import os
from typing import List
import nbformat
from nbconvert import PythonExporter
import shutil

# Defining Constants
PYTHON_SCRIPT_EXTENSION: str = '.py'
PYTHON_NOTEBOOK_EXTENSION: str = '.ipynb'
SKIPPABLE_DIRECTORIES: List[str] = [
    'bin',
    'lib',
    'Lib',
    'lib64',
    'share',
    'MACOSX',
    'Scripts',
    'include',
    'Include',
    'pyvenv.cfg',
    '__pycache__',
]


def convert_ipynb_to_py(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as notebook_file:
        notebook_content = nbformat.read(notebook_file, as_version=4)

    python_exporter = PythonExporter()
    python_code, _ = python_exporter.from_notebook_node(notebook_content)

    with open(output_path, 'w', encoding='utf-8') as python_file:
        python_file.write(python_code)

    print(f'\nConverted: {output_path}')


def batch_convert_ipynb_to_py(input_dir, output_dir):

    print('\nStarting Notebook conversions...\n')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with ThreadPoolExecutor() as executor:

        for current_path, _, file_names in os.walk(input_dir):

            if any(skippable_directory in current_path for skippable_directory in SKIPPABLE_DIRECTORIES):

                continue

            file_names: List[str] = list(filter(lambda file_name: file_name.endswith((PYTHON_SCRIPT_EXTENSION, PYTHON_NOTEBOOK_EXTENSION)), file_names))


            for each_file_name in file_names:

                input_file_path: str = os.path.join(current_path, each_file_name)
                output_file_dir: str = current_path.replace(input_dir, output_dir)
                output_file_path: str = os.path.join(output_file_dir, each_file_name)

                if not os.path.exists(output_file_dir):

                    os.makedirs(output_file_dir)


                if each_file_name.endswith(PYTHON_SCRIPT_EXTENSION):

                    shutil.copy2(input_file_path, output_file_path)


                elif each_file_name.endswith(PYTHON_NOTEBOOK_EXTENSION):

                    output_file_path = output_file_path.replace(PYTHON_NOTEBOOK_EXTENSION, PYTHON_SCRIPT_EXTENSION)

                    executor.submit(convert_ipynb_to_py, input_file_path, output_file_path)

    executor.shutdown(wait=True)


