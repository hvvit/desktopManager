from flask import Blueprint, render_template

contents = Blueprint('contents', __name__)


from bin import vncs

@contents.route('/dashboard')
@contents.route('/')
def dashboard():
  vncs_dict_info = vncs.list_all_vnc_server()
  return render_template('dashboard.html', vncs_dict=vncs_dict_info['message'], status=vncs_dict_info['status'])

@contents.route('/agents')
def agents():
  return render_template('agents.html')

@contents.route('/vnc')
def vnc():
  return render_template('vncs.html')