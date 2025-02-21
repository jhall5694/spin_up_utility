spin_up_utility
developed by Jason Hall 2/12/2025

*To use this utility, open the "dist" folder to download and run "spin_up_utility.exe"
**Alternatively, the utility can be run from a cmd window as Administrator
***download the latest version of Python at "https://www.python.org/downloads/"
***download the entire github project
***open a cmd window as admin
***navigate to the downloaded directory, e.g., ->> cd "path/to/the/downloaded/directory"
***run spin_up_utility main.py file via command "python main.py"
*This utility provides multiple features for working with local TCP instances
*Prerequisite: This utility requires that the TCP folder be located at: C:/Program Files (x86)/TimeClock Plus 7.0/
*The utility can be exited at any time by pressing ctrl+c
*The utility should always be run as administrator

Changes:
1.0
* Initial base functionality

1.1
* Added ability to press enter to perform action on current running version/folder
* Ability to open admin page from utility

1.2
* open version folder
* add program exit

1.3
* Actions stored in list
* Add main program loop

1.4
* fixed wrong folder index
* added stop step before start action 
* copy config files
* Open log file folders
* Check that each TCP service is running
* select by typing version 021025
  ** also brought functionality to download interface 021125
* extract and move to TCP folder 022125
* re-factor code
* Download pri repository file
* open yaml files

