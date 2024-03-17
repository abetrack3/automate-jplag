import os
import shutil
import zipfile
import patoolib
from concurrent.futures import ThreadPoolExecutor

def extract_zip_file(zip_file, extract_path):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

def extract_rar_file(rar_file, extract_path):
    os.makedirs(extract_path)
    patoolib.extract_archive(rar_file, outdir=extract_path)

def extract_zip_and_rar_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with ThreadPoolExecutor() as executor:

        for filename in os.listdir(input_dir):
            file_path = os.path.join(input_dir, filename)
            file_name_without_extension: str = os.path.splitext(filename)[0]
            destination_file_path: str = os.path.join(output_dir, file_name_without_extension)

            if filename.endswith('.zip'):
                executor.submit(extract_zip_file, file_path, destination_file_path)
                print(f'Extracted: {filename} (ZIP)')

            elif filename.endswith('.rar'):
                executor.submit(extract_rar_file, file_path, destination_file_path)
                print(f'Extracted: {filename} (RAR)')

            elif filename.endswith('.ipynb') or filename.endswith('.py'):
                os.makedirs(destination_file_path)
                shutil.copy(file_path, destination_file_path)
                print(f'Copied: {filename}')

    executor.shutdown(wait=True)

