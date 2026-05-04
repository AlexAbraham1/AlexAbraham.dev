# AlexAbraham.dev
Personal Website powered by AWS App Runner

## Local Development
```bash
python main.py
```
Runs at http://127.0.0.1:8080

## Deploy
Push to `master`. App Runner is wired to this repo and auto-deploys on push.

## One-Time AWS Setup

### 1. Verify domains in SES
```bash
aws ses verify-domain-identity --domain alexabraham.net --region us-east-1
aws ses verify-domain-identity --domain alexabraham.dev --region us-east-1
```
Add the returned TXT records to DNS for each domain.

### 2. Request SES production access
AWS console → SES → Account dashboard → "Request production access".
Removes sandbox restrictions so email can be sent to unverified recipients.

### 3. Create App Runner instance role
This role is assumed by the running container — App Runner's equivalent of an EC2 instance profile.

Trust policy:
```json
{
  "Effect": "Allow",
  "Principal": { "Service": "tasks.apprunner.amazonaws.com" },
  "Action": "sts:AssumeRole"
}
```

Inline permissions policy (`ses:SendEmail` on both domains):
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

### 4. Create GitHub connection
AWS console → App Runner → Connections → Create → GitHub → authorize the `AlexAbraham1` account.

### 5. Create the App Runner service
```bash
aws apprunner create-service \
  --service-name alexabraham-prod \
  --source-configuration '{
    "AuthenticationConfiguration": { "ConnectionArn": "<connection-arn>" },
    "AutoDeploymentsEnabled": true,
    "CodeRepository": {
      "RepositoryUrl": "https://github.com/AlexAbraham1/AlexAbraham.dev",
      "SourceCodeVersion": { "Type": "BRANCH", "Value": "master" },
      "CodeConfiguration": { "ConfigurationSource": "REPOSITORY" }
    }
  }' \
  --instance-configuration '{
    "Cpu": "256", "Memory": "512",
    "InstanceRoleArn": "arn:aws:iam::<acct>:role/AppRunnerInstanceRole-alexabraham"
  }' \
  --region us-east-1
```

### 6. Pin auto-scaling to a single warm instance (avoids cold starts)
```bash
aws apprunner create-auto-scaling-configuration \
  --auto-scaling-configuration-name alexabraham-min \
  --min-size 1 --max-size 1 --max-concurrency 100 --region us-east-1
aws apprunner update-service --service-arn <svc-arn> \
  --auto-scaling-configuration-arn <asc-arn> --region us-east-1
```

### 7. Associate custom domains
```bash
aws apprunner associate-custom-domain --service-arn <svc-arn> \
  --domain-name alexabraham.net --enable-www-subdomain --region us-east-1
aws apprunner associate-custom-domain --service-arn <svc-arn> \
  --domain-name alexabraham.dev --enable-www-subdomain --region us-east-1
```
Add the returned cert-validation CNAMEs and target CNAMEs at your DNS provider. Apex records require ALIAS / ANAME / CNAME-flattening (Route 53 ALIAS, Cloudflare CNAME-flattening, etc.).
