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
import boto3
import traceback
from validate_email import validate_email

app = Flask(__name__)

@app.route('/')
def root():
    data = load_home_page_data()
    return render_template('index.html', data=data)

def load_skill_logos(directory):
    """Load skill logos from a directory and extract skill names from filenames.
    
    Args:
        directory: Path to directory containing logo files
        
    Returns:
        List of dicts with 'filename' and 'name' keys, sorted by filename
    """
    logos = []
    if os.path.exists(directory):
        for filename in natsorted(os.listdir(directory)):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                # Split on "_" to separate number prefix from skill name
                parts = filename.rsplit('.', 1)[0].split('_', 1)  # Remove extension first, then split
                if len(parts) > 1:
                    skill_name = parts[1]  # Take everything after the first underscore
                else:
                    skill_name = parts[0]  # Fallback if no underscore
                logos.append({
                    'filename': filename,
                    'name': skill_name
                })
    return logos

def load_home_page_data():
    data = {
        'contact': {
            'email': 'alexgabraham1@gmail.com',
            'phone': '1-201-403-7591',
            'phone2': '(201) 403-7591',
            'address': '64 Meadow Drive',
            'city': 'Woodsburgh',
            'state_code': 'NY',
            'zip': '11598'
        },
        'interests': [
            'skiing', 'snowboarding', 'running', 'tennis',
            'guitar', 'piano', 'music', 'movies',
            'chilling', 'web_surfing', 'watching_tv', 'games'
        ],
        'education': [],
        'tech_skills_logos': load_skill_logos('static/_content/tech_skills'),
        'leadership_skills_logos': load_skill_logos('static/_content/leadership_skills'),
        'work_experience': [],
        'copyright_year': '2026'
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
        client = boto3.client('ses', region_name='us-east-1')
        client.send_email(
            Source='form@alexabraham.net',
            Destination={'ToAddresses': ['alexgabraham1@gmail.com']},
            Message={
                'Subject': {'Data': 'Personal Website Form Submission'},
                'Body': {'Text': {'Data': 'Name: {}\nEmail: {}\nSubject: {}\nMessage: {}'.format(name, email, subject, text)}}
            }
        )
        return "OK"
    except:
        traceback.print_exc()
        return "There was an error sending your message. Please try reaching out via email. Thanks!"


from apig_wsgi import make_lambda_handler
handler = make_lambda_handler(app, binary_support=True)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
