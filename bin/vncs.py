from email import message
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

vncs_directory = '/home/harshv/python/desktopManager/bin/vncs_directory/'
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
  return os.path.isfile(vncs_directory + name)

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
    return {'status': 'ok', 'message': {'vnc_port': vnc_port, 'display': display_port, 'log_file': log_file.strip(), 'geometry': geometry, 'hostname': hostname}}
  else:
    return {'status': 'error' ,'message': {'vnc_port': '', 'display': '', 'log_file': '', 'geometry': '', 'hostname': hostname }}
  
def start_vnc_server(name, geometry):
  if not check_if_vncs_exist(name + ".vncs"):
    vnc_info = run_vnc_server(geometry)
    if vnc_info['status'] == 'ok':
      file_name = vncs_directory + name + ".vncs"
      with open(file_name, 'w') as outfile:
        json.dump(vnc_info['message'], outfile)
      return {'status': 'ok', 'message': { 'vnc_info': vnc_info }}
    else:
      return {'status': 'error', 'message': 'Not able to create VNCs'}
  else:
    return {'status': 'error', 'message': 'VNC already exists'}

def kill_vnc_server(name):
  if check_if_vncs_exist(name):
    file_name = vncs_directory + name
    with open(file_name, 'r') as outfile:
      vnc_data = json.load(outfile)
    display_id = vnc_data['display']
    output = run_command("vncserver -kill :" + display_id.strip() + " > /tmp/vncoutput 2>&1")
    file = open('/tmp/vncoutput')
    output = run_command('rm -f ' + file_name)
    for line in file:
      if line.startswith('Killing'):
        return {'status': 'ok', 'message': name + " vnc server removed"}
    return {'status': 'ok', 'message': name + " vnc server config file removed"}
  else:
    return {'status': 'error', 'message': name + " vnc server not found"}

def list_all_vnc_server():
  vnc_servers = []
  for vncs in os.listdir(vncs_directory):
    with open(vncs_directory + "/" + vncs, 'r') as vnc_file:
      vnc_servers.append({ 'name': vncs.split('/')[-1],'data': json.load(vnc_file)})
  if vnc_servers:
    return {'status': 'ok', 'message': vnc_servers}
  else:
    return {'status': 'error', 'message': 'No VNC servers found'}

def get_vnc_info(name):
  if check_if_vncs_exist(name):
    file_name = vncs_directory + name
    with open(file_name, 'r') as vncs:
      data = json.load(vncs)
    return {'status': 'ok', 'message': data}
  else:
    return {'status': 'error', 'message': name + ' VNC does not exist'}

def kill_all_vnc():
  list_of_files = os.listdir(vncs_directory)
  messages = []
  for file in list_of_files:
    if file.endswith('.vncs'):
      vnc_status = kill_vnc_server(file)
      if vnc_status['status'] == 'ok':
        messages.append({'status': 'ok', 'message': vnc_status['message']})
      else:
        messages.append({'status': 'error', 'message': vnc_status['message']})
  if list_of_files:
    return {'status': 'ok', 'message': messages}
  else:
    return {'status': 'error', 'message': 'No VNCs found'}

def kill_multiple_vncs(list_of_vnc):
  if list_of_vnc:
    messages = []
    for vnc in list_of_vnc:
      if vnc.endswith('.vncs'):
        vnc_status = kill_vnc_server(vnc)
        if vnc_status['status'] == 'ok':
          messages.append({'status': 'ok', 'message': vnc_status['message']})
        else:
          messages.append({'status': 'error', 'message': vnc_status['message']})
      else:
        messages.append({'status': 'error', 'message': 'wrong vnc name given: '+vnc})
    return {'status': 'ok', 'message': messages}
  else:
    return {'status': 'error', 'message': 'No VNCs found'}