from flask import Flask, request, render_template, send_from_directory, abort
from flask_httpauth import HTTPBasicAuth
from database import check_user_existence
import os
import time
import json
import socket
from datetime import datetime

MyApp = Flask('GRAIC Submission Website')
auth = HTTPBasicAuth()

@MyApp.route('/_submit', methods=['POST'])
def _submit():
    # if 'enableConsent' not in request.form.keys():
    #     return render_template("error.html")

    # file_line = request.files['fileToUpload_line']
    # file_vision = request.files['fileToUpload_vision']

    file_control = request.files['fileToUpload_control']
    # dependencies = request.files['reqFile']
    # email = request.form['email']
    # teamName = request.form['teamName']
    netid_1 = request.form['netid_1']
    netid_2 = request.form['netid_2']
    netid_3 = request.form['netid_3']

 
    # if not file or not email or not teamName or file.filename !='agent.py' or len(teamName.split(" ")) > 1:
    #     return render_template('error.html')
    if not file_control or not netid_1 or not netid_2:
        return render_template('error.html')

    # if dependencies:
    #     dependencies.save("dependency_2023/{}_requirements.txt".format(email))

    # save
    # fname = f"{email}-{model}.zip"
    # now = datetime.now()
    # dt_string = now.strftime("%m:%d:%Y-%H:%M:%S")
    # fname = email + '__' + teamName + '__' + dt_string + '.py'

    # fname_1 = file_line.filename
    # fname_2 = file_vision.filename
    fname = file_control.filename
    if fname != "controller.py":
        return render_template('error.html')

    arr = [netid_1, netid_2, netid_3] if netid_3 else [netid_1, netid_2]
    folder_name = '_'.join(sorted(arr))
    os.makedirs(f"submissions/{folder_name}", exist_ok=True)
    file_control.save(f'submissions/{folder_name}/' + fname)
    # file_line.save(f'ECE484_FA23_MP1/{folder_name}/' + fname_1)
    # file_vision.save(f'ECE484_FA23_MP1/{folder_name}/' + fname_2)
    return render_template('confirmation.html', 
                           netid_1 = netid_1, netid_2 = netid_2, netid_3 = netid_3
                           ) 
                        #teamName = fname


@MyApp.route('/')
# @auth.login_required
def index():
    return render_template('index.html')


@MyApp.route('/rules')
# @auth.login_required
def rules():
    return render_template('rules.html')


if __name__ == '__main__':
    MyApp.run(host='0.0.0.0', port=8000)
