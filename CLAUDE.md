# AlexAbraham.dev

Personal portfolio website. Flask app deployed on AWS App Runner.

## Stack
- Python 3.11 / Flask
- AWS App Runner (source-based deploy from GitHub, auto-deploys on push to `master`)
- AWS SES (contact form email, authenticated via IAM instance role — no API keys)

## Project Structure
- `main.py` — Flask app (routes: `GET /`, `POST /send_email`)
- `templates/` — Jinja2 main template + HTML snippets for work experience and education
- `static/` — CSS, JS, images, PDFs, skill logos
- `apprunner.yaml` — App Runner build + run config

## Local Development
```bash
python main.py
```
Runs at http://127.0.0.1:8080

## Deploy
Push to `master`. App Runner auto-deploys.

## Tests
```bash
pytest
```
