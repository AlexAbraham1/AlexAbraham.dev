# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_render_template]
import datetime
import os

from flask import Flask, render_template, request
import sendgrid
import traceback
import secrets
from validate_email import validate_email

app = Flask(__name__)

@app.route('/')
def root():
    data = load_home_page_data()
    return render_template('index.html', data=data)

def load_home_page_data():
    data = {
        'contact': {
            'email': 'alex@abraham.net',
            'phone': '1-201-403-7591',
            'phone2': '(201) 403-7591',
            'address': '200 Bennett Ave #2D',
            'city': 'New York',
            'state_code': 'NY',
            'zip': '10040'
        },
        'interests': [
            'skiing', 'snowboarding', 'running', 'tennis',
            'guitar', 'piano', 'music', 'movies',
            'chilling', 'web_surfing', 'watching_tv', 'games'
        ],
        'education': [],
        'tech_skills_1': {
            'Python': 95,
            'MongoDB': 90,
            'SQL': 90,
            'Angular': 90
        },
        'tech_skills_2': {
            'Cloud Infrastructure (Azure)': 85,
            'Java': 85,
            'Apache Airflow': 80,
            'HTML & CSS': 80
        },
        'work_experience': [],
        'copyright_year': '2019'
    }

    for path in os.listdir('templates/work_experience'):
        with open('templates/work_experience/' + path, 'r', encoding='utf-8') as f:
            data['work_experience'].append(f.read())

    for path in os.listdir('templates/education'):
        with open('templates/education/' + path, 'r', encoding='utf-8') as f:
            data['education'].append(f.read())

    return data

@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    text = request.form['message']

    if not name:
        return "Please enter a valid name"
    if not validate_email(email):
        return "Please enter a valid email address"
    if not subject:
        return "Please enter a valid subject"
    if not text:
        return "Please enter a valid message"

    try:
        sg = sendgrid.SendGridClient(secrets.SENDGRID_API_KEY)
        message = sendgrid.Mail()

        message.add_to("alex@abraham.net")
        message.set_from("{} <{}>".format(name, email))
        message.set_subject(subject)
        message.set_html(text)
        sg.send(message)
    except:
        traceback.print_exc()
        return "There was an error sending your message. Please try reaching out via email. Thanks!"

    return "OK"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
