from ossaudiodev import OSSAudioError
import sys
import os
import json
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
  
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
  
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)
  
# now we can import the module in the parent
# directory.
import subprocess
def run_command(command_string):
  try:
    process = subprocess.Popen(command_string, stdout=subprocess.PIPE, shell = True)
  except OSError:
    return False
  process.wait()
  if process.returncode != 0:
    return False
  return process.communicate()[0]

def check_if_vncs_exist(name):
  return os.path.isfile('vncs_directory/' + name + ".vncs")

def run_vnc_server(geometry):
  output = run_command("vncserver -geometry " + geometry + " > /tmp/vncoutput 2>&1 ")
  output_file = open("/tmp/vncoutput")
  log_file= ""
  desktop_file = ""
  hostname = os.uname().nodename
  for line in output_file:
    if line.startswith("Log file is"):
      log_file = line.split(' ')[-1]
    if line.startswith("New 'X' desktop is "):
      desktop_file = line.split(' ')[-1].strip()
  display_port = desktop_file.split(':')[-1]
  vnc_file = open(log_file.strip())
  vnc_port = ""
  for line in vnc_file:
    if "Listening for VNC connections on TCP port" in line:
      vnc_port = line.split(' ')[-1].strip()
  if vnc_port != "":
    return {'status': 'ok', 'message': {'vnc_port': vnc_port, 'display': display_port, 'log_file': log_file, 'geometry': geometry, 'hostname': hostname}}
  else:
    return {'status': 'error' ,'message': {'vnc_port': '', 'display': '', 'log_file': '', 'geometry': '', 'hostname': hostname }}
  
def start_vnc_server(name, geometry):
  if not check_if_vncs_exist(name):
    vnc_info = run_vnc_server(geometry)
    if vnc_info['status'] == 'ok':
      file_name = "vncs_directory/" + name + ".vncs"
      with open(file_name, 'w') as outfile:
        json.dump(vnc_info, outfile)
      return {'status': 'ok', 'message': { 'vnc_info': vnc_info }}
    else:
      return {'status': 'error', 'message': 'Not able to create VNCs'}
  else:
    return {'status': 'error', 'message': 'VNC already exists'}
print(start_vnc_server("myvnc", "1920x1080"))