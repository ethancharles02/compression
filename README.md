# Project Compression

## Contact
Ethan Charles:
GitHub: ethancharles02
Email: ethan.charles02@gmail.com

Josh Pettingill:
GitHub: JoshPettingill
Email: jpett4@gmail.com

## Purpose
The whole purpose of this project is to develop a new way of compressing files, and to learn more about compression through applied learning.

## Documentation

### Usage Instructions

#### exe
Command to create the exe: "pyinstaller "src/__main__.py" -n Compressor --onefile --distpath "." --noconsole --clean"
Or run the compile.py file
Once it is done, the exe will be in a newly created dist folder

This program should work as any other .exe file. On a windows opperating system you should be able to double click on the file or run it from the command line.

#### Python
In order to run this program you will need the src directory from this project, and have the latest version of python installed on your machine. All the scripts use standard python packages, so you shouldn't need to install anything else. Once you have all of that configured, you should be able to call python on the "__main__.py" file, and python should launch the progam.

#### Basic instructions
Once run, the program should bring up the Graphical User Interface (GUI). 

From the GUI you should be able to use the file/folder buttons to select an input file/folder respectively, and you can use the browse button to select an output folder. If you don't select an output folder, then the result will be placed in the same folder as the input file/folder. There should be a drop down menu to choose which algorithm for compression you would like to run, as well as an option to choose either compression or decompression.

Once you have input those locations and settings, you should be able to click the run button, and a window will pop up with the results of the compression/decompression and the input path and output folder used.

### Technologies

* Python 3.8.5

#### Development enviroment
* Visual Studio Code with basic python extensions installed.

#### Python Modules
This project includes several python modules. The following is a list of them.
* os 
* sys
* time
* shutil 
* io 
* functools
* random 
* math
* tkinter
* Numpy (IMPORTANT must be: 1.20.1. The command is "pip install numpy==1.20.1")
* BitArray
* unittest for testing

### Architecture


### Testing

#### Unit Testing
Unit Testing for this project was done with the python unittest module. In the project there is a tests folder which contains all the unit tests for each of the modules that were produced. 

#### Integration Testing
Some of the Unit tests also work as integration tests. Other integration test documents can be found in the tests folder. These documents include test cases with results for the tests we ran.

#### System Testing
System test documents can be found in the test folder. These documents include test cases with results for the tests we ran.

### Future Work

* Introduce parallelism with multiprocessing for folder compression
* Run all tests in the SRS
* Update diagrams for architecture documentation
* Create progress bar for compression and decompression

#### ETHAN

#### JOSH
* Test changes made to GUI
