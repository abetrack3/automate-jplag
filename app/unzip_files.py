import os
import zipfile
import patoolib

def extract_zip_file(zip_file, extract_path):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

def extract_rar_file(rar_file, extract_path):
    patoolib.extract_archive(rar_file, outdir=extract_path)

def extract_zip_and_rar_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)

        if filename.endswith('.zip'):
            file_name_without_extension: str = filename.split('.')[0]
            extract_zip_file(file_path, os.path.join(output_dir, file_name_without_extension))
            print(f'Extracted: {filename} (ZIP)')

        elif filename.endswith('.rar'):
            extract_rar_file(file_path, output_dir)
            print(f'Extracted: {filename} (RAR)')

if __name__ == '__main__':
    input_directory = 'input_directory_path'  # Replace with the path to your input directory
    output_directory = 'output_directory_path'  # Replace with the path to your output directory

    extract_zip_and_rar_files(input_directory, output_directory)