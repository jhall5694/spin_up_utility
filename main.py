import psutil
import os
import webbrowser
import datetime
import sys
import time
import shutil

'''  Changes
* Actions stored in list
* Add main program loop
'''

class spin_up():
  def __init__(self):
    self.path_root = 'C:/Program Files (x86)/TimeClock Plus 7.0/'
    self.path_cfg_root = 'cfg/'
    self.path_adm_cfg = 'adm/lib/tcpws-1.0.0/cfg/'
    self.path_bin_root = 'bin/'
    self.path_cfg_template = 'cfg_template/'
    self.path_adm_log = 'adm/lib/tcpws-1.0.0/log/'
    self.path_app_log = 'app/lib/tcpws-1.0.0/log/'
    self.path_control_panel = 'adm/etc/controlpanel/Tcp.ControlPanel.exe' 
    self.path_default_config_files = 'cfg_template' 
    self.list_running_versions = []
    self.list_installed_versions = []
    self.list_folder_names = []
    self.list_str_actions = ["Start","Stop","Restart","Open Admin portal","Open root folder","copy config files","TCP control panel","Reset","Exit"]
      
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
    #self.window.destroy()
    #self.window.quit()
  
  
  
  
  # data workers -----------------------------------------------------------------
  # determine what version if any is already running
  def get_list_running_versions(self):
    local_list_running_versions = []
    for service in psutil.win_service_iter():
      curr_service_name = service.name()
      #print(curr_service_name)
      if curr_service_name.find("TimeClockPlus") > -1:
        curr_version = self.get_version_from_service_string(curr_service_name)
        if curr_version != "":
          # add running version string to list of running versions (if not already present)
          if not curr_version in local_list_running_versions:
            local_list_running_versions.append(curr_version)
            #print(curr_version)
            
    return local_list_running_versions

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
  
  # get list of TCP version folder names
  def get_list_installed_versions(self):
    local_list_folder_names = []
    local_list_installed_versions = []
    for item in os.scandir(self.path_root):
      if item.is_dir() == True:
        curr_folder_name = item.name
        curr_folder_version = self.get_version_from_folder_string(curr_folder_name)
        if curr_folder_version != "":
          if not curr_folder_version in local_list_installed_versions:
            local_list_installed_versions.append(curr_folder_version)
            local_list_folder_names.append(curr_folder_name)
    return [local_list_installed_versions, local_list_folder_names]
    
  # get TCP version from folder name string
  def get_version_from_folder_string(self,str_name):
    #print(str_name)
    #print(len(str_name))
    str_version = ""
    end_index = len(str_name)
    num_decimals = 0
    for str_char_index in range(len(str_name)):
      #print(str_char_index)
      curr_char = str_name[str_char_index]
      #print(curr_char)
      if curr_char == ".":
        #print("here")
        num_decimals = num_decimals + 1
        if num_decimals == 4:
          end_index = str_char_index
          break
    if num_decimals > 2:
      str_version = str_name[0:end_index]
      
    return str_version
                    
  # generate string for user input
  def generate_string(self, list_data):
    index = 1
    str_new = ""
    for str_curr in list_data:
      str_new = str_new + "%s) %s\n"%(index,str_curr)
      index += 1
    return str_new
      
  # open log files
  def open_log_file(type):
    None
        
  # GUI -----------------------------------------------------------------
  def create_window(self):
    None
    
  def clear_cmd_window(self):
    os.system('cls')
    
    
  def thisfunc(self):
    None
    
  # command line utilization until GUI is ready 
  def main(self):
    continue_application = True    
    while continue_application == True:
      # clear terminal window
      self.clear_cmd_window()
      
      # print list of running versions
      self.list_running_versions = self.get_list_running_versions()
      print("\nrunning versions")
      print(self.list_running_versions)
      
      # print list of installed versions
      #self.list_installed_versions = self.get_list_installed_versions()[0]
      #print("\ninstalled versions")
      #print(self.list_installed_versions)
      
      # print list of folder names
      self.list_folder_names = self.get_list_installed_versions()[1]
      print("\nfolder names")
      #print(self.list_folder_names)
      str_print = ""
      str_print = self.generate_string(self.list_folder_names)
      #for i in range(len(self.list_folder_names)):
      #  curr_folder_name = self.list_folder_names[i]
      #  str_print = str_print + "\n" + str(i) + ") " + curr_folder_name
      print(str_print)
      
      # user selects an action
      print("\n\n")
      str_action = self.generate_string(self.list_str_actions)
      print(str_action)

      # get user action choice
      valid_selection = False
      while valid_selection == False:
        #self.print_running_versions()
        #self.print_version_folder()
        int_action_choice = int(input("Make a selection --> "))
        if int_action_choice >= 0 and int_action_choice <= len(self.list_str_actions):
          valid_selection = True
        else:
          print("\ninvalid selection - try again\n")
          
        # get string value of choice
        str_action_choice = self.list_str_actions[int_action_choice - 1]
        print(str_action_choice)
    
      # perform non version specific actions
      ask_for_version_folder = False 
      match str_action_choice: 
        case "Open Admin portal":
          computer_name = os.environ['COMPUTERNAME']
          webbrowser.open('http://%s:9443/app/admin/#/AdminLogOn'%computer_name)
          time.sleep(3)
          
        case "Open root folder":
          str_action_description = "attempting to open root folder: "
          #path_action_version_action = '"' + self.path_root + '"'
          path_action_version_action = '"' + self.path_root.replace("/","\\") + '"'
          #print(path_action_version_action)
          #os.system("start cmd /c %s"%path_action_version_action)      
          os.system("start explorer.exe %s"%path_action_version_action)
          time.sleep(3)
          
        case "Reset":
          print("here") 
          str_action_description = "resetting application: "
          
        case "Exit":
          str_action_description = "attempting to exit application: "
          self.soft_exit()
          
        case default:
          ask_for_version_folder = True
      
      # user selects a folder and action is attempted    
      valid_selection = False
      while valid_selection == False and ask_for_version_folder == True:
        if len(self.list_running_versions) > 0:
          action_version_folder_index = input("\nSelect a version folder (press enter for current [%s])(enter c to cancel): \n--> "%self.list_running_versions[0])
          if action_version_folder_index == "": # user pressed enter to select current running version
            # get index of current running version in list_folder_names
            try:
              action_version_folder_index = self.list_folder_names.index(self.list_running_versions[0])
            except:
              # return an invalid index so user can try again
              action_version_folder_index = len(self.list_folder_names) + 999
          elif action_version_folder_index == "c":
            break
          else:
            action_version_folder_index = int(action_version_folder_index)
        else:
          action_version_folder_index = int(input("\nSelect a version folder : \n--> ")) 
        try:
          str_action_version_folder = self.list_folder_names[action_version_folder_index - 1]
        except:
          print("\ninvalid folder selection - try again\n")
        else:
          valid_selection = True
          path_action_version_folder = self.path_root + str_action_version_folder + "/"
          match str_action_choice:
            case "Start":
              path_action_version_action = path_action_version_folder + self.path_bin_root + "start.bat"            
              str_action_description = "start"
              
            case "Stop":
              path_action_version_action = path_action_version_folder + self.path_bin_root + "stop.bat"
              str_action_description = "stop"
              
            case "Restart":
              path_action_version_action = path_action_version_folder + self.path_bin_root + "restart.bat"
              str_action_description = "restart"
              
            case "TCP control panel":
              path_action_version_action = path_action_version_folder + self.path_control_panel
              str_action_description = "open TCP control panel"
              path_action_version_action = '"' + path_action_version_action + '"'
              
            case "copy config files":
              path_action_version_action = path_action_version_folder + self.path_cfg_root
              str_action_description = "copy config files"
              
            case default:
              None
              break
          
          # confirm action
          str_action_description = "\nAttempt to %s?"%str_action_description + path_action_version_action
          print(str_action_description)
          str_action = self.generate_string(['Yes','Cancel'])
          print(str_action)
          str_input = input("Make a selection --> ")
          if str_input != "1" and str_input != "": # user chose to cancel action
            break
            
          if str_action_choice == "copy config files":
            #print(self.path_root + self.path_cfg_template)
            #print(path_action_version_action)
            dest = shutil.copytree(self.path_root + self.path_cfg_template, path_action_version_action, dirs_exist_ok = True)
            dest = shutil.copy(self.path_root + self.path_cfg_template + "AdmPass.txt", path_action_version_folder + self.path_adm_cfg + "AdmPass.txt")
            #print(self.path_root + self.path_cfg_template + "AdmPass.txt")
            #print(path_action_version_folder + self.path_adm_cfg + "AdmPass.txt")
            #inp = input("press enter to continue")
            break
          elif str_action_choice == "TCP control panel":
            os.startfile(path_action_version_action)
            break
            
          path_action_version_action = '"' + path_action_version_action + '"'
          print(path_action_version_action)
          #path_action_version_action = path_action_version_action.replace("/","\\")
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
    


    


