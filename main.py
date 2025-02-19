import psutil
import os
import webbrowser
import datetime
import sys
import time
import shutil
import boto3 # AWS access
import yaml
import zipfile

'''  Changes
* Actions stored in list
* Add main program loop
'''

class spin_up():
  def __init__(self):
    self.curr_windows_user = self.get_windows_user()
    self.path_root = 'C:/Program Files (x86)/TimeClock Plus 7.0/'
    self.path_downloads = 'c:/Users/' + self.curr_windows_user + '/Downloads'
    self.path_cfg_root = 'cfg/'
    self.filename_cfg_adm = "config.adm.yaml"
    self.filename_cfg_app = "config.app.yaml"
    self.filename_cfg_ctl = "config.ctl.yaml"
    self.filename_cfg_hub = "config.hub.yaml"
    self.filename_cfg_pwh = "config.pwh.yaml"
    self.path_adm_cfg = 'adm/lib/tcpws-1.0.0/cfg/'
    self.path_bin_root = 'bin/'
    self.path_cfg_template = 'cfg_template/'
    self.path_adm_log = 'adm/lib/tcpws-1.0.0/log/'
    self.path_app_log = 'app/lib/tcpws-1.0.0/log/'
    self.path_control_panel = 'adm/etc/controlpanel/Tcp.ControlPanel.exe' 
    self.path_default_config_files = 'cfg_template' 
    self.list_running_versions = []
    self.list_installed_versions = []
    self.latest_rc_build = 0
    self.latest_drc_build = 0
    self.list_cfg_files = ["adm","app","workstation hub"]
    self.list_adm_cfg_fields = [""]
    self.list_app_cfg_fields = [""]
    self.list_pwh_cfg_fields = ["server enabled"]
    self.list_read_write = ["read (enter)","write"]
    self.list_folder_names = []
    #self.dict_str_actions = {"s":"Start","p":"Stop","r":"Restart","a":"Open Admin portal","rf":"Open TCP root folder","vf":"Open version folder","l":"Open log file","cf":"Copy config files","rw":"read/write cfg settings","d":"Download file from QA S3","df":"Open downloads folder","t":"TCP control panel","":"Reset (enter)","x":"Exit"}
    self.dict_str_actions = {"s":"Start","p":"Stop","r":"Restart","a":"Open Admin portal","rf":"Open TCP root folder","vf":"Open version folder","l":"Open log file","cf":"Copy config files","d":"Download file from QA S3","z":"Unzip file", "df":"Open downloads folder","t":"TCP control panel","":"Reset (enter)","x":"Exit"}    
    self.list_str_action_keys = list(self.dict_str_actions.keys())
    self.list_str_action_values = list(self.dict_str_actions.values())
    self.list_str_log_folders = ["adm","app"]
    self.list_yes_no = ["yes(enter)","no"]
    
    self.path_last_downloaded_file = ""    

      
    #filepath = "C:/Program Files (x86)/TimeClock Plus 7.0/7.1.57.145/cfg/config.pwh.yaml"
    #self.yaml_to_list(filepath)
    #self.soft_exit()
    
    self.show_first_run_notice()
    # start main loop
    #self.create_window()
    self.main()
    
  # logging -----------------------------------------------------------------
  def write_to_log_file(self, data):
    self.file_write = open("log.txt","a") # log file
    self.file_write.write(str(datetime.datetime.now()) + " : " + data + "\n")
    self.file_write.close()

  def write_to_notes_file(self,data):
    self.file_write = open("notes.txt","a") # log file
    self.file_write.write(data + " : " + str(datetime.datetime.now()) + "\n")
    self.file_write.close()

  def date_time_str(self):
    now = datetime.datetime.now()
    mo = str(now.month)
    if len(mo) < 2:
      mo = "0" + mo
    da = str(now.day)
    if len(da) < 2:
      da = "0" + da
    yr = str(now.year)[2:4]
    hr = str(now.hour)
    if len(hr) < 2:
      hr = "0" + hr
    mi = str(now.minute)
    if len(mi) < 2:
      mi = "0" + mi
    timestamp = mo + da + yr + "_" + hr + mi
    return timestamp


  def create_window(self):
    None

  # application -----------------------------------------------------------------
  def soft_exit(self):
    self.write_to_log_file('exit btn pressed')
    self.file_write.close()
    sys.exit()
    exit

  def pause(self, str_var):
    cl = input("%s : press enter to continue --> "%str_var)    

 #self.window.destroy()
    #self.window.quit()
  
  
  
  
  # data workers -----------------------------------------------------------------
  # determine what version if any is already running
  def get_list_running_versions(self):
    local_list_running_versions = []
    local_list_running_services = []
    for service in psutil.win_service_iter():
      curr_service_name = service.name()
      #print(curr_service_name)
      if curr_service_name.find("TimeClockPlus") > -1:
        curr_version = self.get_version_from_service_string(curr_service_name)
        local_list_running_services.append(curr_service_name)
        if curr_version != "":
          # add running version string to list of running versions (if not already present)
          if not curr_version in local_list_running_versions:
            local_list_running_versions.append(curr_version)
            #print(curr_version)
            
    return [local_list_running_versions,local_list_running_services]

  # get TCP version from service name string
  def get_version_from_service_string(self,str_name):
    return_val = ""
    pos_version_start = str_name.find('[')
    if pos_version_start > -1:
      str_version = str_name[pos_version_start + 1:]
      pos_version_end = str_version.find('-')
      if pos_version_end > -1:
        str_version = str_version[0:pos_version_end]
        return_val = str_version
        
    return return_val
    
  # get TCP versions available for download
  def list_available_downloads(self):
    repo_path = "http://pri.tcplusondemand.com.s3-website-us-east-1.amazonaws.com/core/qa/"
    print(repo_path)
    for root, dirs, files in os.walk(repo_path):
      print("here")
      for file in files:
        print(os.path.join(root, file))    

  # get list of TCP version folder names - also keep track of latest rc and drc build numbers
  def get_list_installed_versions(self):
    local_list_folder_names = []
    local_list_installed_versions = []
    for item in os.scandir(self.path_root):
      if item.is_dir() == True:
        curr_folder_name = item.name
        num_decimals = curr_folder_name.count(".")
        if num_decimals < 3: # not a version folder
          continue
        list_temp = self.get_version_and_breakout_from_folder_string(curr_folder_name)
        #print(list_temp)
        curr_folder_version_full = list_temp[0]
        curr_folder_major = int(list_temp[1])
        curr_folder_minor = int(list_temp[2])
        curr_folder_build = int(list_temp[3])
        curr_folder_revision = int(list_temp[4])
        
        if curr_folder_version_full != "":
          if not curr_folder_version_full in local_list_installed_versions:
            local_list_installed_versions.append(curr_folder_version_full)
            local_list_folder_names.append(curr_folder_name)
          if curr_folder_revision < 10: # RC
            if curr_folder_build > self.latest_rc_build:
              self.latest_rc_build = curr_folder_build           
          else: # DRC
            if curr_folder_build > self.latest_drc_build:
              self.latest_drc_build = curr_folder_build

    return [local_list_installed_versions, local_list_folder_names]
    
  # get TCP version from folder name string
  def get_version_and_breakout_from_folder_string(self,str_name):
    #print(str_name)
    #print(len(str_name))
    str_version_full = ""
    
    end_index = len(str_name)
    num_decimals = 0
    for str_char_index in range(len(str_name)):
      curr_char = str_name[str_char_index]
      if curr_char == ".":
        num_decimals = num_decimals + 1
        if num_decimals == 4:
          end_index = str_char_index
          break
    if num_decimals > 2:
      str_version_full = str_name[0:end_index]
      
    list_temp = str_version_full.split('.')  
    
    return [str_version_full,list_temp[0],list_temp[1],list_temp[2],list_temp[3]]
     
  # download a file from pri.tcplusondemand.com/core/qa    
  def download_file(self):
    cl = True
    while cl == True:
      print("select method to specify file")
      print(self.generate_string(["version number (enter)","full filename"]))
      str_action_choice = input("Make a selection --> ")
      self.clear_cmd_window()
      if str_action_choice == "2":
        str_filename_to_download = input("enter the full filename you wish to download from pri.tcplusondemand.com/core/qa (press c to cancel) --> ")
      else:
        str_to_present = "\nEnter the full or partial version number(c = cancel) --> "
        version_selection_type = input(str_to_present)
        if version_selection_type == "":
          continue
        if version_selection_type == "c":
          return        
        str_version = self.build_version_str_from_user_input(version_selection_type)
        if str_version == "error":
          self.invalid_user_input_notice()
        if str_version == "c":
          return
    
        if str_version != "":
            str_filename_to_download = "tcp.core-" + str_version + ".zip"
      
      str_file_to_download = "pri.tcplusondemand.com/core/qa/" + str_filename_to_download
      
      str_action_choice = input("\nattempt to download %s? (c = cancel)"%str_file_to_download)
      if str_action_choice == "c":
        return
      print("\nattempting to download : %s"%str_file_to_download)
      
      # open link in browser - temporary solution until consistent aws s3 functionality is obtained
      webbrowser.open('http://%s'%str_file_to_download)
      
      self.path_last_downloaded_file = 'C:/Users/' + self.curr_windows_user + '/Downloads' + str_filename_to_download
      
      
      # method utilizing aws s3 needs more research to be consistent
      '''
      try:
        client = boto3.client(
            's3',
            aws_access_key_id='AKIAWPJDIGEAFHFWVZVM',
            aws_secret_access_key='10o20Ekrgf19LoKP3yWw3kxpes3ae7i0ulu5'
        )
        s3 = boto3.resource('s3')
      except:
        print("not able to connect to AWS S3 - Check credentials")
      else:
        try:
          s3.Bucket('pri.tcplusondemand.com').download_file(str_file_to_download, str_file_to_download)
        except:
          print("problem downloading the file - exact filename match required")   
          #raise
        else:
          print("file successfully downloaded")
      '''
      print("\nattempt another download?")
      print(self.generate_string(self.list_yes_no))
      str_action_choice = input("Make a selection --> ")
      if str_action_choice != "" and str_action_choice != "1":
        break
      else:
        cl = True
        self.clear_cmd_window()
   
  def unzip_file(self):
    if self.path_last_downloaded_file == "":
      path_temp = input("Enter full path to the zip file --> ")
      try:
        exists = os.path.exists(path_temp)
      except:
        self.pause("make sure zip file exists then try again")
        return
      else:
        self.path_last_downloaded_file = path_temp
        
    path_file_to_download = self.path_last_downloaded_file.replace("\\","/")
    
    cl = input("Press enter to attempt to extract %s ? (c = cancel)"%path_file_to_download)
    if cl == "c":
      return
    try:
      with zipfile.ZipFile(path_file_to_download, 'r') as zip_ref:
        path_downloads = 'C:/Users/' + self.curr_windows_user + '/Downloads'
        print("file extracting to %s \n please wait..."%path_downloads)
        zip_ref.extractall(path_downloads)
    except:
      self.pause("make sure zip file exists then try again")
      return "extract failed"
    else:
      self.pause("file extracted to %s"%path_downloads)  
  
  # generate string for user input
  def generate_string(self, list_data):
    index = 1
    str_new = ""
    for str_curr in list_data:
      str_new = str_new + "%s) %s\n"%(index,str_curr)
      index += 1
    return str_new
    
  def get_action_index_from_action_string(self, str_var):
    try:
      list_index = self.list_str_action_values.index(str_var)
    except:
      list_index = len(self.list_str_action_values) + 999
    return list_index
    
  def get_folder_index_from_version_string(self,str_var):
    try:
      action_version_folder_index = self.list_folder_names.index(str_var)
    except:
      action_version_folder_index = len(self.list_folder_names) + 999
    return action_version_folder_index
    
  # user entered version number string - generate full version string
  def build_version_str_from_user_input(self,str_var):
    str_full_version = "error"
    
    for char in str_var: # verify user entered valid input
      match char:
        case "0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"|"0"|".":
          None
        case default: # invalid input
          return ""
    
    list_temp = str_var.split(".") # create list by splitting full user input by decimal, e.g. "7.1.57.132" -> ["7","1","57","132"], e.g. "56.1" -> ["56","1"]
    #print(list_temp)
    list_version_split = ["","","",""]
    
    # determine if user entered DRC or RC version number
    len_revision_str = len(list_temp[len(list_temp) - 1])
    
    # set defaults
    list_version_split[0] = "7" # major
    list_version_split[1] = "1" # minor
    if len_revision_str == 1: # build
      list_version_split[2] = str(self.latest_rc_build)
    else:
      list_version_split[2] = str(self.latest_drc_build)    
    
    # major
    if len(list_temp) > 3:
      list_version_split[0] = list_temp[len(list_temp) - 4] 

     # minor
    if len(list_temp) > 2:
      list_version_split[1] = list_temp[len(list_temp) - 3]

    # build  
    if len(list_temp) > 1:
      list_version_split[2] = list_temp[len(list_temp) - 2]
      
    # revision
    if len(list_temp) > 0:
      list_version_split[3] = list_temp[len(list_temp) - 1]
    
    #print(list_version_split)
    separator = "."
    str_full_version = separator.join(list_version_split)
    #print("str_full_version: %s"%str_full_version)
    return str_full_version
    
  # open log files
  def open_log_file(type):
    None
  
  # get current computer USER
  def get_windows_user(self):
    curr_user = os.getenv("USERNAME")
    return curr_user
 
  # modify config files
  def read_write_config_file(self, file_cfg, field, val=""):
    path_file_cfg = ""
    str_field = ""
    
    match file_cfg:
      case "adm":
        path_file_cfg = self.filename_cfg_adm
        match field:
          case "auto_import":
            None
      
      case "app":
        path_file_cfg = self.filename_cfg_app
        match field:
            case "auto_import":
              None
        
      case "workstation hub":
        path_file_cfg = self.filename_cfg_pwh
        match field:
          case "server enabled":
            section = "nginx"
            str_field = "http.server.enabled"
            if val == "yes":
              val = "true"
            else:
              val = "false"

    if val == "": # user is requesting to get a cfg field value
      None
    else: # user requesting to set a cfg field value
      None

  def cfg_file_interface(self, path_version_folder):
    # user chooses config file
    valid_selection = False
    while valid_selection == False:
      print("action selected: read/write cfg settings")
      print("choose a config file to read/write")
      str_action = self.generate_string(self.list_cfg_files)
      print(str_action)
      str_action_choice = input("Make a selection (c = cancel) --> ")
      
      match str_action_choice:
        case "c":
          return
          
        case "1": # adm
          valid_selection = True
          user_file_selection_display = "adm"
          user_fields_to_present = self.list_adm_cfg_fields
          
        case "2": # app
          valid_selection = True
          user_file_selection_display = "app"
          user_fields_to_present = self.list_app_cfg_fields
          
        case "3": # workstation hub
          valid_selection = True
          user_file_selection_display = "workstation hub"
          user_fields_to_present = self.list_pwh_cfg_fields
          print(user_fields_to_present)
          
        case default:
          self.invalid_user_input_notice()
          continue
          

    # user chooses cfg file field
    valid_selection = False
    while valid_selection == False:
      print("cfg file selected: %s"%user_file_selection_display)
      print("choose a cfg file field")
      str_action = self.generate_string(user_fields_to_present)
      print(str_action)
      str_action_choice = input("Make a selection (c = cancel) --> ")
      
      match str_action_choice:
        case "c":
          return
          
        case default:
          try:
            str_field = user_fields_to_present[int(str_action_choice) - 1]
          except:
            self.invalid_user_input_notice()
            continue
          else:
            valid_selection = True          
    
    # user chooses read/write
    valid_selection = False
    while valid_selection == False:
      str_action = self.generate_string(self.list_read_write)
      print(str_action)
      str_action_choice = input("Make a selection (c = cancel) --> ")
      
      match str_action_choice:
        case "c":
          return
          
        case default:
          try:
            str_action_read_write = self.list_read_write[int(str_action_choice) - 1]
          except:
            self.invalid_user_input_notice()
            continue        
          else:
            valid_selection = True
      
    str_val_to_write = ""  
    if str_action_read_write == "write":  
      valid_selection = False
      while valid_selection == False:
        str_val_to_write = input("value to write (c = cancel) --> ")      
        
        match str_action_choice:
          case "c":
            return
            
          case "":
            self.invalid_user_input_notice()
            continue
            
          case default:
            valid_selection = True
    
    # call function to perform action on cfg file
    self.read_write_config_file(user_file_selection_display, str_field, str_val_to_write) # read_write_config_file(self, file_cfg, field, val=""):

  def yaml_to_list(self,filepath):
    print("askjldh")
    print(filepath)
    with open(filepath, 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        
    # Print the values as a dictionary
    print(data)
 
  # GUI -----------------------------------------------------------------
  def create_window(self):
    None
    
  def clear_cmd_window(self):
    os.system('cls')
    
  def thisfunc(self):
    None
    
  def load_folder_names(self):
    self.list_folder_names = self.get_list_installed_versions()[1]
    
  def print_folder_names(self):
    # print list of folder names
    print("\nfolder names")
    str_print = self.generate_string(self.list_folder_names)
    print(str_print)
  
  def show_first_run_notice(self):
    self.clear_cmd_window()
    str_to_present = "spin_up_utility\n"
    str_to_present = str_to_present + "developed by Jason Hall 2/12/2025\n"
    str_to_present = str_to_present + "\n"
    str_to_present = str_to_present + "*This utility provides multiple features for working with local TCP instances\n"
    str_to_present = str_to_present + "*Prerequisite: This utility requires that the TCP folder be located at: %s\n"%self.path_root
    str_to_present = str_to_present + "*The utility can be exited at any time by pressing ctrl+c\n"
    print(str_to_present)
    input("Press enter to continue --> ")
    
  def list_action_options(self):
    # user selects an action
    print("\nActions:\n")
    str_action = ""
    indx = 1
    for val in self.dict_str_actions.items():    
      space_multiplier = (len(str(indx)) - 2) * -1
      str_spaces_indx = " " * space_multiplier
      space_multiplier = (len(val[0]) - 2) * -1
      str_spaces_shortcut_key = " " * space_multiplier 
      str_action = str_action + "\n" + str(indx) + ") " + str_spaces_indx + " [" + val[0] + "]" + str_spaces_shortcut_key + " : " + val[1]
      indx = indx + 1
    print(str_action)  
    
  def show_running_version_and_services(self):      
    # print list of running versions
    list_running_versions_and_services = self.get_list_running_versions()
    self.list_running_versions = list_running_versions_and_services[0]
    self.list_running_services = list_running_versions_and_services[1]
    print("\nrunning versions")
    print(self.list_running_versions)
    print("\nrunning services")
    str_print = self.generate_string(self.list_running_services)
    print(str_print)
    self.print_divider()
    
  def print_divider(self):
    str_to_present = "-" * 40
    print(str_to_present)
    
  def invalid_user_input_notice(self):
    self.pause("invalid input")
    
  # command line utilization until GUI is ready 
  def main(self):
    continue_application = True    
    while continue_application == True:
      # clear terminal window
      self.clear_cmd_window()

      # get user action choice
      valid_selection = False
      while valid_selection == False:
        self.clear_cmd_window()
        self.show_running_version_and_services()
        self.list_action_options()
        int_action_choice = input("Make a selection --> ")
        
        # see if user entered shortcut key, e.g., user entered "df" for "Open downloads folder"
        try:
          int_action_choice = self.list_str_action_keys.index(int_action_choice) + 1
        except:
          None # non shortcut key entered
          
        # get action string description  
        try:
          int_action_choice = int(int_action_choice)
          str_action_choice = self.list_str_action_values[int_action_choice - 1]
        except:
          self.invalid_user_input_notice()
        else:
          valid_selection = True
      
      # perform non version specific actions
      self.clear_cmd_window()
      ask_for_version_folder = False 
      match str_action_choice: 
        case "Open Admin portal":
          computer_name = os.environ['COMPUTERNAME']
          webbrowser.open('http://%s:9443/app/admin/#/AdminLogOn'%computer_name)
          time.sleep(3)
          
        case "Open TCP root folder":
          str_action_description = "attempting to open TCP root folder: "
          path_action_version_action = '"' + self.path_root.replace("/","\\") + '"'
          os.system("start explorer.exe %s"%path_action_version_action)
          time.sleep(3)            
          
        case "Download file from QA S3":
          str_action_description = "attempting to download file: "
          self.download_file()
          
        case "Unzip file":
          str_action_description = "attempting to Unzip file: "
          self.unzip_file()
          
        case "Open downloads folder":
          str_action_description = "attempting to open downloads folder: "
          path_action_version_action = '"' + self.path_downloads.replace("/","\\") + '"'
          os.system("start explorer.exe %s"%path_action_version_action)
          time.sleep(3)

        case "Reset (enter)":
          str_action_description = "resetting application: "
          
        case "Exit":
          self.pause("Exiting")
          self.soft_exit()
          
        case default:
          ask_for_version_folder = True
      
      print("action selected : %s"%str_action_choice)
      
      
      # user selects a folder and action is attempted    
      valid_selection = False
      while valid_selection == False and ask_for_version_folder == True:
        # print list of folder names
        self.clear_cmd_window()
        self.load_folder_names()
        print("action selected : %s\n"%str_action_choice)
        self.print_divider()
        
        str_to_present = "\nEnter the full or partial version number(c = cancel)(l = list available)"
        if len(self.list_running_versions) > 0:
          str_to_present = str_to_present + "(enter = current version[%s])"%self.list_running_versions[0]
        str_to_present = str_to_present + ": --> "
        version_selection_type = input(str_to_present)
        
        if version_selection_type == "": # user pressed enter to select current running version
          if len(self.list_running_versions) >= 0:
            # get index of current running version in list_folder_names
            action_version_folder_index = self.get_folder_index_from_version_string(self.list_running_versions[0])
        elif version_selection_type == "c":
          break
        elif version_selection_type == "l":
          self.print_folder_names()
          action_version_folder_index = input("\nSelect a version folder (enter c to cancel): \n--> ")
          if action_version_folder_index == '' or action_version_folder_index == "c":
            break
          else: 
            action_version_folder_index = int(action_version_folder_index) - 1
        else: # User typed a number - find the correct version folder index
          str_version_full = self.build_version_str_from_user_input(version_selection_type)
          if str_version_full == "error":
            self.invalid_user_input_notice()
            continue
          if str_version_full == "c":
            break
          print("\nVersion input by user: %s \n Continue?"%str_version_full)
          print(self.generate_string(self.list_yes_no))
          str_action_temp = input("Make a selection --> ")
          if str_action_temp != "" and str_action_temp != "1":
            continue
          action_version_folder_index = self.get_folder_index_from_version_string(str_version_full)
        try:
          str_action_version_folder = self.list_folder_names[action_version_folder_index]
          print("version found and selected : %s"%str_action_version_folder)
        except:
          self.invalid_user_input_notice()
        else:
          valid_selection = True
          path_action_version_folder = self.path_root + str_action_version_folder + "/"
          match str_action_choice:
            case "Start":
              path_action_version_action = path_action_version_folder + self.path_bin_root + "start.bat"            
              str_action_description = "Start"
              
            case "Stop":
              path_action_version_action = path_action_version_folder + self.path_bin_root + "stop.bat"
              str_action_description = "Stop"
              
            case "Restart":
              path_action_version_action = path_action_version_folder + self.path_bin_root + "restart.bat"
              str_action_description = "Restart"
          
            case "TCP control panel":
              path_action_version_action = path_action_version_folder + self.path_control_panel
              str_action_description = "open TCP control panel"
              path_action_version_action = '"' + path_action_version_action + '"'
              
            case "Copy config files":
              path_action_version_action = path_action_version_folder + self.path_cfg_root
              str_action_description = "Copy config files"
              
            case "read/write cfg settings":
              str_action_description = "read/write cfg settings"
              self.cfg_file_interface(path_action_version_folder)
              break
              
            case "Open version folder":
              str_action_description = "open version folder: "
              path_action_version_action = '"' + path_action_version_folder.replace("/","\\") + '"'
              #os.system("start explorer.exe %s"%path_action_version_action)
              
            case "Open log file":
              #input_log_src = input("
              str_action = self.generate_string(self.list_str_log_folders)
              print("\n")
              print(str_action)
              
              # get user action choice
              valid_selection = False
              while valid_selection == False:
                try:
                  int_action_choice = input("Make a selection --> ")
                except:
                  self.soft_exit()
                else:
                  try:
                    if int_action_choice == "":
                      int_action_choice = 0
                    else:
                      int_action_choice = int(int_action_choice)
                  except: # invalid user input
                    print(int_action_choice)
                    continue
                  if int_action_choice == 0:
                    valid_selection = True
                  elif int_action_choice >= 0 and int_action_choice <= len(self.list_str_log_folders):
                    valid_selection = True
                  else:
                    self.invalid_user_input_notice()
                    
                  # get string value of choice
                  if int_action_choice == 0:
                    str_action_choice = "Reset (enter)"
                  else:
                    str_action_choice_temp = self.list_str_log_folders[int_action_choice - 1]
                  print(str_action_choice)
                  if str_action_choice_temp == "adm":
                    path_action_version_action = path_action_version_folder + self.path_adm_log
                  elif str_action_choice_temp == "app":
                    path_action_version_action = path_action_version_folder + self.path_app_log
              str_action_description = "Open log file"
            case default:
              None
              break
          
          # confirm action
          self.clear_cmd_window()
          str_action_description = "\nAttempt to %s ?"%str_action_description + path_action_version_action
          print(str_action_description)
          str_action = self.generate_string(['Yes [Enter]','Cancel'])
          print("\n" + str_action)
          str_input = input("Make a selection --> ")
          if str_input != "1" and str_input != "": # user chose to cancel action
            break
            
          if str_action_choice == "Copy config files":
            dest = shutil.copytree(self.path_root + self.path_cfg_template, path_action_version_action, dirs_exist_ok = True)
            dest = shutil.copy(self.path_root + self.path_cfg_template + "AdmPass.txt", path_action_version_folder + self.path_adm_cfg + "AdmPass.txt")
            break
          elif str_action_choice == "TCP control panel":
            os.startfile(path_action_version_action)
            break
          elif str_action_choice == "Open log file":
            os.startfile(path_action_version_action)
          elif str_action_choice == "Open version folder":  
            os.system("start explorer.exe %s"%path_action_version_action)
            break            
            
          path_action_version_action = '"' + path_action_version_action + '"'
          self.clear_cmd_window()
          print("\nExecuting : %s"%path_action_version_action)
          os.system("start cmd /c %s"%path_action_version_action)
    
    
      # confirm action
      

  #  move window -----------------------------------------------------------------
  def start_move(self, event): # move window left click mouse down
    self.x = event.x
    self.y = event.y

  def stop_move(self, event): # move window left click mouse up
    self.x = None
    self.y = None

  def do_move(self, event): # move window left click drag
    deltax = event.x - self.x
    deltay = event.y - self.y
    x = self.window.winfo_x() + deltax
    y = self.window.winfo_y() + deltay
    self.window.geometry(f"+{x}+{y}")

  def set_mode(self,val):
    if self.app_initialized == True:
      match val:
        case 'parse_then_translate':
          self.parse_mode = val
          self.set_button_state('btn_mode_parse_then_translate',1)
          self.set_button_state('btn_mode_translate_then_parse',0)
        case 'translate_then_parse':
          self.parse_mode = val
          self.set_button_state('btn_mode_parse_then_translate',0)
          self.set_button_state('btn_mode_translate_then_parse',1)
        case 'use_binary_short_fields':
          self.binary_use_mode = val
          self.set_button_state('btn_mode_binary_full_field',0)
          self.set_button_state('btn_mode_binary_short_fields',1)
        case 'use_binary_full_field':
          self.binary_use_mode = val
          self.set_button_state('btn_mode_binary_full_field',1)
          self.set_button_state('btn_mode_binary_short_fields',0)


# instantiate class/application
if __name__ == "__main__":
  cl_spin_up = spin_up()
    


    


