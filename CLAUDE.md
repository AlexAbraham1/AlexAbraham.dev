# AlexAbraham.dev

Personal portfolio website. Flask app deployed on AWS Lambda via AWS SAM.

## Stack
- Python 3.13 / Flask
- AWS Lambda + API Gateway HTTP API (hosting, deployed via SAM)
- AWS SES (contact form email, authenticated via Lambda execution role — no API keys)

## Project Structure
- `main.py` — Flask app (routes: `GET /`, `POST /send_email`) + Lambda handler
- `templates/` — Jinja2 main template + HTML snippets for work experience and education
- `static/` — CSS, JS, images, PDFs, skill logos
- `template.yaml` — SAM template (Lambda, API Gateway, IAM, CloudWatch)

## Local Development
```bash
python main.py
```
Runs at http://127.0.0.1:8080

## Deploy
```bash
sam build --use-container
sam deploy
```

First deploy: `sam deploy --guided` (saves config to `samconfig.toml`).

## Tests
```bash
pytest
```
