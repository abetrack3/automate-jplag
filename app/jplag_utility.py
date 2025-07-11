import os
import re
import sys
import requests
import subprocess
from tqdm import tqdm

JPLAG_SUCCESSFUL_RUN_PROMPT: str = '''

#########################################################################
#                                                                       #
#                                                                       #
# JPlag has successfully generated Plagiarism report.                   #
#                                                                       #
# You can find it in a file called "result.zip"                         #
#                                                                       #
# Upload the zip file to https://jplag.github.io/JPlag to view the      #
# report in a readable format                                           #
#                                                                       #
#                                                                       #
#########################################################################
'''

# Constants
JPLAG_JAR_FILE_NAME: str = 'jplag.jar'
JPLAG_JAR_DOWNLOAD_URL: str = ('https://github.com/jplag/JPlag/releases/download/v6.1.0/jplag-6.1.0-jar-with'
                               '-dependencies.jar')


def check_java_environment() -> int:
    try:
        # Run 'java -version' command to check if Java is installed
        java_version_info = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT, text=True)

        # Extract and print the Java version
        version_match = re.search(r'"(\d+\.\d+)', java_version_info)

        if version_match:

            java_version = version_match.group(1)

            print(f"Java is installed. Version: {java_version}")

            return int(float(java_version))

        else:

            print("Java version information could not be determined.")

    except subprocess.CalledProcessError:

        print("Java is not installed or not in the system's PATH.")

    except Exception as e:

        print(f"An error occurred: {e}")

    return -1


def check_jplag_jar_exists(jar_path: str = JPLAG_JAR_FILE_NAME) -> bool:
    return os.path.exists(jar_path)


def download_jplag_jar(jar_url: str = JPLAG_JAR_DOWNLOAD_URL, jar_path: str = JPLAG_JAR_FILE_NAME) -> None:
    try:

        # Send a GET request to the URL
        response = requests.get(jar_url, stream=True)

        # Check if the request was successful (HTTP status code 200)
        response.raise_for_status()

        # Get the total file size from the "Content-Length" header
        file_size = int(response.headers.get('Content-Length', 0))

        # Create a tqdm progress bar
        progress_bar = tqdm(desc='Downloading JPlag', total=file_size, unit='B', unit_scale=True)

        # Open a file for writing in binary mode
        with open(jar_path, 'wb') as file:

            # Iterate over the response content in chunks
            for chunk in response.iter_content(chunk_size=1024):
                # Write the chunk to the file
                file.write(chunk)

                # Update the progress bar
                progress_bar.update(len(chunk))

        # Close the progress bar
        progress_bar.close()

        print(f"JPlag download complete. File saved to {jar_path}")

    except requests.exceptions.RequestException as e:

        print(f"Download failed: {e}")

    except Exception as e:

        print(f"An error occurred: {e}")


def run_jplag_jar(source_directory: str, jar_path: str = JPLAG_JAR_FILE_NAME) -> None:
    try:

        process = subprocess.Popen(['java', '-jar', jar_path, source_directory, '--language', 'python3',
                                    '--mode', 'RUN', '--shown-comparisons', '-1', '--normalize', '--min-tokens', '5',
                                    '--csv-export', '--overwrite'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   text=True)

        for console_output_line in process.stdout:
            print(console_output_line.strip())

        return_code = process.wait()

        if return_code == 0:

            print('JPlag execution successful')

            print(JPLAG_SUCCESSFUL_RUN_PROMPT)

        else:

            print('JPlag execution failed')

            sys.exit(return_code)

    except Exception as caught_exception:

        print('An error occurred while running JPlag')

        print(caught_exception)

        sys.exit(1)
