# AlexAbraham.dev

Personal portfolio website. Flask app deployed on AWS Lambda via AWS SAM.

## Stack
- Python 3.13 / Flask
- AWS Lambda + API Gateway HTTP API (hosting, deployed via SAM)
- S3 bucket for static assets (served directly to browsers — Lambda only handles `/` and `/send_email`)
- AWS SES (contact form email, authenticated via Lambda execution role — no API keys)

## Project Structure
- `main.py` — Flask app (routes: `GET /`, `POST /send_email`) + Lambda handler. Reads `STATIC_URL` env var (S3 bucket URL in prod, `/static` locally) and rewrites `/static` → `STATIC_URL` in `work_experience` / `education` snippet HTML at load time
- `templates/` — Jinja2 main template (uses `{{ STATIC_URL }}`) + raw HTML snippets for work experience and education (use literal `/static`, rewritten at runtime)
- `static/` — CSS, JS, images, PDFs, skill logos. Served from S3 in prod; from Flask in local dev
- `template.yaml` — SAM template (Lambda, API Gateway, S3 bucket + public-read policy, IAM, CloudWatch)

## Local Development
```bash
python main.py
```
Runs at http://127.0.0.1:8080

## Deploy
```bash
sam build --use-container
sam deploy
BUCKET=$(aws cloudformation describe-stacks --stack-name alexabraham-site \
  --query 'Stacks[0].Outputs[?OutputKey==`StaticBucketName`].OutputValue' --output text)
aws s3 sync ./static/ s3://$BUCKET/
```
The S3 sync is required whenever files in `./static/` change.

First deploy: `sam deploy --guided` (saves config to `samconfig.toml`).

## Tests
```bash
pytest
```
