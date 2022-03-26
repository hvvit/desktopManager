from flask import Blueprint, render_template

contents = Blueprint('contents', __name__)

@contents.route('/dashboard')
@contents.route('/')
def dashboard():
  return render_template('dashboard.html')

@contents.route('/agents')
def agents():
  return render_template('agents.html')

@contents.route('/vnc')
def vnc():
  return render_template('vncs.html')