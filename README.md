# Microstructural Lick Analysis
### Pre-installation
For now, we only have a version of this that works with python 2.7. Please confirm that you have this version following these steps:
https://edu.google.com/openonline/course-builder/docs/1.10/set-up-course-builder/check-for-python.html
If you don't have python 2.7, follow this webpage to install it (it will likely be python 2.7.14):
https://wiki.python.org/moin/BeginnersGuide/Download
### Installing and Running the program
##### Downloading
- Go to: https://github.com/pungaliy/Microstructural_Lick_Analysis
- Click the green button marked "Clone or Download"
- Click "download zip", and download it to an appropriate folder on your computer. The zip file should be called "Microstructural_Lick_Analysis-master.zip"
- Unzip the file. You should see a folder named "Microstructural_Lick_Analysis-master"
- Enter the folder
- There should be four files
  * extract_params.py
  * summarize_data.py
  * param_file.csv
  * README.md
##### Importing the data
- Next, create a new folder within the "Microstructural_Lick_Analysis-master" folder and put all csv data into your new folder
- Copy this folder name **exactly as it's shown** into the first column, second row of param_file.csv
- Now enter all other relevant information into param_file.csv. Please do not leave any fields blank
- Once this is complete, and you have python 2.7 installed, you're ready for the final few steps
##### Navigating to the correct folder
- Open command prompt (Windows) or terminal (Mac)
- Navigate to the "Microstructural_Lick_Analysis-master" folder by typing
    ```cd [pathname]```
    where the pathname is can be found in the by rightclicking the folder in My Computer (windows) or Finder (mac). Look for a filename that looks something like ```usr/directory/more_directories```
Obviously, the directory names will vary, but something similar should show up. For more help, please look up how to use the cd command on the operating system you are using
##### Running the program
- Once you are in this directory, which should contain the four files mentioned above as well as a folder containing the csv files, run the following command in command prompt/terminal: ```python summarize_data.py```
- Your results should be placed in a file called output.csv located in the Microstructural_Lick_Analysis-master" folder
- Note that the program **will overwrite** the output.csv folder each time it is run. If you'd like to save the results, move the file to a different folder.






