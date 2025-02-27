# spin_up_utility  
### *developed by Jason Hall 2/12/2025*
   
## Description
- This utility provides multiple features for working with local TCP instances

## Usage
* To use this utility (multiple options):
  1. Download and extract the latest release
  2. Download and run the executable
  3. Download and unzip the latest release
      - Run the executable
  4. Download entire project and run python file from a cmd prompt as Administrator
      - download the latest version of Python at "https://www.python.org/downloads/"  
      - download the entire github project  
      - open a cmd prompt as admin  
      - navigate to the downloaded directory, e.g., ->> cd "path/to/the/downloaded/directory"  
      - run spin_up_utility main.py file via command "python main.py"

 
## Prerequisites
- This utility requires that the TCP folder be located at: C:/Program Files (x86)/TimeClock Plus 7.0/  
- The utility should always be run as administrator

## Notes
- The utility can be exited at any time by pressing ctrl+c  

## TODO
- Auto refresh option
- Add ability to stop specific TCP services
- Clean up code
  - A lot of the code is duplicated that could be rewritten to utilize common methods
- List pri repository files
  - After thorough testing it seems the only way to make this possible would be to get with the AWS S3 admin and request "directory listing" permissions
- Modify specific yaml file options/keys
  - Python has a great class for dealing with yaml files
  - Started exploratory testing in this feature that was promising
- Add GUI functionality

## Changelog:  
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
  - also brought functionality to download interface 021125  
* extract and move to TCP folder 022125  
* re-factor code  
* Download pri repository file  
* open yaml files  
