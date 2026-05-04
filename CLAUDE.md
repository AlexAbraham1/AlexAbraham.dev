# AlexAbraham.dev

Personal portfolio website. Flask app deployed on AWS Elastic Beanstalk.

## Stack
- Python 3.13 / Flask
- AWS Elastic Beanstalk (hosting)
- AWS SES (contact form email, authenticated via IAM role — no API keys)

## Project Structure
- `main.py` — Flask app (routes: `GET /`, `POST /send_email`)
- `templates/` — Jinja2 main template + HTML snippets for work experience and education
- `static/` — CSS, JS, images, PDFs, skill logos
- `Procfile` — gunicorn startup command for Elastic Beanstalk

## Local Development
```bash
python main.py
```
Runs at http://127.0.0.1:8080

## Deploy
```bash
eb deploy
```

## Tests
```bash
pytest
```
