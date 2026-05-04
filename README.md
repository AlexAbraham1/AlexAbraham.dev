# AlexAbraham.dev
Personal Website powered by AWS

## Prerequisites
- AWS CLI configured (`aws configure`)
- EB CLI installed (`pip install awsebcli`)
- EB environment initialized (`eb init` — one-time setup, see below)

## Local Development
```bash
python main.py
```
Runs at http://127.0.0.1:8080

## Deploy
```bash
eb deploy
```

## One-Time AWS Setup

### 1. Verify domains in SES
```bash
aws ses verify-domain-identity --domain alexabraham.net --region us-east-1
aws ses verify-domain-identity --domain alexabraham.dev --region us-east-1
```
Add the returned TXT records to DNS for each domain.

### 2. Request SES production access
Go to AWS console → SES → Account dashboard → "Request production access".
This removes sandbox restrictions so email can be sent to unverified addresses.

### 3. Create IAM instance profile for Elastic Beanstalk
Attach a policy allowing `ses:SendEmail` on both SES identities:
```json
{
  "Effect": "Allow",
  "Action": "ses:SendEmail",
  "Resource": [
    "arn:aws:ses:us-east-1:*:identity/alexabraham.net",
    "arn:aws:ses:us-east-1:*:identity/alexabraham.dev"
  ]
}
```

### 4. Initialize Elastic Beanstalk
```bash
eb init alexabraham-dev --platform "Python 3.13" --region us-east-1
eb create alexabraham-prod
```
