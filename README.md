

# Automate JPlag


This is just a quick automation tool to run jplag and generate plagiarism report on student assignment submission


### Pre-Requisites

* You have python installed in your system, minimum version is python3.7(tested)
* You have java installed in your system, minimum jdk is 21(tested)


### Not a Pre-Requisite

* No need to download JPlag. This automation script will do the job for you


## How to run?

There are few steps to be taken care of before this script can be run

* #### Also you can check out the YouTube Tutorial:

    * Video Link: https://youtu.be/4boT6H_Mi0U

* #### Download the source code:

    * You can either clone it using `git clone https://github.com/abetrack3/automate-jplag.git`. (Assuming you have git installed)

    * Or, download as zip from here https://github.com/abetrack3/automate-jplag and then extract

* #### Start your IDE:

    * Open the folder containing the source code in your IDE (example: VSCode, PyCharm)

* #### Install dependencies:

    * Open up the terminal from the IDE, all of the command mentioned belkow will go through here

    * (Optional) Upgrade your pip by entering the following command in the terminal: `pip  install --upgrade pip`

    * (Optional - Recommended) Create a virtual environment beforehand

        * Enter the following command from your IDE's terminal `python -m venv plagiarismVenv'

        * Activate the environment: `.\\plagiarismVenv\\Scripts\\activate`

        * To know more about Python Virtual Environments: [Link](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/venv-win.html)

    * All the required dependencies are listed in the **requirements.txt** Just enter `pip install -r requirements.txt --no-cache-dir` into the terminal

* #### Download your students' assignment submission

    * Extract the submission zip from your google drive and place it in the folder containing the source code (to run the code easily)

* #### Run your code

    * Just enter the command in the terminal: `python main.py --submission-folder-name "{submission folder name}"`

## After running the script..

If you have come this far, it means you have successfully run this code and as a result you will find two files geneated:

* results.jplag (Contains detailed plagiarism report. The script will open up the report viewer automatically)
* result.xlsx (You will find a summarised report here)


## Found a bug? Do an open source contribution!

This script is in its very early stage so bugs and improvements are highly plausible. Feel free to create an issue, fork it, make your changes, and finally create a pull request. Feedbacks are always welcome!!