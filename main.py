import sys
from argparse import ArgumentParser
from app.cleanup import remove_generated_artifacts
from app.decorators import timeit
from app.excel_report_generator import generate_excel_report
from app.jplag_utility import check_java_environment, check_jplag_jar_exists, download_jplag_jar, run_jplag_jar
from app.merge_files import merge_each_student_suibmissions
from app.notebook_to_script_converter import batch_convert_ipynb_to_py
from app.unzip_files import extract_zip_and_rar_files


# Define Paramters - These will get updated based on the value given on command line arguments
SUBMISSION_SOURCE_FOLDER_NAME: str = '' # name of the folder where submissions are stored
ASSIGNMENT_SUBMITTED_AS_ZIP_FILE: bool = False # if students are submitting multiple files in a zip, if it is a single file submission then mark it as False



# Define Constants
REQUIRED_JAVA_VERSION: int = 17
UNZIPPED_FILES_FOLDER_NAME: str = f'{SUBMISSION_SOURCE_FOLDER_NAME} UNZIPPED'
CONVERTED_FILES_FOLDER_NAME: str = f'{SUBMISSION_SOURCE_FOLDER_NAME} CONVERTED'
JPLAG_SCANNABLE_FOLDER_NAME: str = f'{SUBMISSION_SOURCE_FOLDER_NAME} JPLAG SCANNABLE'



@timeit
def __main__() -> None:


    try:

        # Taking parameters from Command Line Arguments
        argument_parser = ArgumentParser()
        argument_parser.add_argument('--submission-folder-name', type=str, required=True)
        argument_parser.add_argument('--zipped-submission', action='store_true')
        argument_parser.set_defaults(zipped_submission=False)

        arguments = argument_parser.parse_args()
        SUBMISSION_SOURCE_FOLDER_NAME = arguments.submission_folder_name
        ASSIGNMENT_SUBMITTED_AS_ZIP_FILE = arguments.zipped_submission


        # Removing any residual files from previous runs
        remove_generated_artifacts()


        # check whether java is installed or not
        current_java_version: int = check_java_environment()

        if current_java_version == -1:

            sys.exit(1)


        # check minimum java version
        if current_java_version < REQUIRED_JAVA_VERSION:

            print(f'Current java version is {current_java_version}. Required Java version is {REQUIRED_JAVA_VERSION}')

            sys.exit(1)


        # Check for JPlag, download if needed
        if check_jplag_jar_exists() is False:

            print('JPlag not found')

            download_jplag_jar()

        else:

            print('JPlag already downloaded')


        # unzipping each students' submission files
        if ASSIGNMENT_SUBMITTED_AS_ZIP_FILE is True:
            extract_zip_and_rar_files(SUBMISSION_SOURCE_FOLDER_NAME, UNZIPPED_FILES_FOLDER_NAME)


        # Convert any IPython NoteBook Files in plain pure python script
        batch_convert_ipynb_to_py(UNZIPPED_FILES_FOLDER_NAME if ASSIGNMENT_SUBMITTED_AS_ZIP_FILE else SUBMISSION_SOURCE_FOLDER_NAME,
                                  CONVERTED_FILES_FOLDER_NAME)


        # If students are submitting multiple files in a zip format then we need to merge those code files into a single file for each student
        if ASSIGNMENT_SUBMITTED_AS_ZIP_FILE is True:
            merge_each_student_suibmissions(CONVERTED_FILES_FOLDER_NAME, JPLAG_SCANNABLE_FOLDER_NAME)


        # Run JPlag and generate plagiarism report
        run_jplag_jar(JPLAG_SCANNABLE_FOLDER_NAME if ASSIGNMENT_SUBMITTED_AS_ZIP_FILE is True else CONVERTED_FILES_FOLDER_NAME)


        # Generate Human Readable Excel Report
        generate_excel_report()


    except KeyboardInterrupt:

        pass

    finally:

        # Removing any residual files from current runs
        remove_generated_artifacts(exclude_result_artifacts=True)



if __name__ == '__main__':
    __main__()