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
from natsort import natsorted

from flask import Flask, render_template, request
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import traceback
from validate_email import validate_email
from firestore import FireStore

app = Flask(__name__)

@app.route('/')
def root():
    data = load_home_page_data()
    return render_template('index.html', data=data)

def load_home_page_data():
    data = {
        'contact': {
            'email': 'alexgabraham1@gmail.com',
            'phone': '1-201-403-7591',
            'phone2': '(201) 403-7591',
            'address': '146 McGlynn Place',
            'city': 'Cedarhurst',
            'state_code': 'NY',
            'zip': '11516'
        },
        'interests': [
            'skiing', 'snowboarding', 'running', 'tennis',
            'guitar', 'piano', 'music', 'movies',
            'chilling', 'web_surfing', 'watching_tv', 'games'
        ],
        'education': [],
        'tech_skills_1': {
            'Python': 95,
            'SQL': 95,
            'Kafka': 90,
            'Java': 90
        },
        'tech_skills_2': {
            'Google Cloud Platform': 85,
            'Kubernetes': 85,
            'Apache Airflow': 80,
            'Javascript': 80
        },
        'work_experience': [],
        'copyright_year': '2023'
    }

    for path in natsorted(os.listdir('templates/work_experience')):
        with open('templates/work_experience/' + path, 'r', encoding='utf-8') as f:
            data['work_experience'].append(f.read())

    for path in natsorted(os.listdir('templates/education')):
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

    if len(text.strip()) < 15:
        return "OK"

    try:
        sg = sendgrid.SendGridAPIClient(api_key=FireStore().get_value("SENDGRID_API_KEY"))

        from_email = Email("form@alexabraham.net")
        to_email = To("alexgabraham1@gmail.com")
        subject_email = "Personal Website Form Submission"
        content = Content("text/plain", """
Name: {}
Email: {}
Subject: {}
Message: {}
        """.format(name, email, subject, text))


        mail = Mail(from_email, to_email, subject_email, content)
        mail_json = mail.get()
        response = sg.client.mail.send.post(request_body=mail_json)
        assert response.status_code == 202

        return "OK"
    except:
        traceback.print_exc()
        return "There was an error sending your message. Please try reaching out via email. Thanks!"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
