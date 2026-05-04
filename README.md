# AlexAbraham.dev
Personal Website — AWS Lambda + API Gateway

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
The S3 sync is required whenever files in `./static/` change — Lambda only serves dynamic routes; assets are served from S3.

First deploy use `sam deploy --guided` — saves config to `samconfig.toml`.

## Tests
```bash
pytest
```

---

## One-Time AWS Setup

### 1. Verify domains in SES (already done)
```bash
aws ses get-identity-verification-attributes \
  --identities alexabraham.net alexabraham.dev --region us-east-1
```
Both should show `Success`. Production access should also be granted already.

### 2. Install SAM CLI
```bash
pip install aws-sam-cli
```

### 3. First deploy
```bash
sam build --use-container
sam deploy --guided
```
Prompts:
- Stack name: `alexabraham-site`
- Region: `us-east-1`
- Allow SAM to create IAM roles: **Yes**
- `SiteFunction has no authentication. Is this okay?`: **Yes** (answer for each prompt — site is intentionally public)
- Save to `samconfig.toml`: **Yes**

Then upload static assets to the S3 bucket created by the stack:
```bash
BUCKET=$(aws cloudformation describe-stacks --stack-name alexabraham-site \
  --query 'Stacks[0].Outputs[?OutputKey==`StaticBucketName`].OutputValue' --output text)
aws s3 sync ./static/ s3://$BUCKET/
```

Note the `ApiUrl` output — use this to verify the site before DNS cutover.

### 4. Custom domains (after verifying the default ApiUrl works)

**Request ACM certs (must be in us-east-1):**
```bash
aws acm request-certificate --domain-name alexabraham.net \
  --subject-alternative-names www.alexabraham.net \
  --validation-method DNS --region us-east-1

aws acm request-certificate --domain-name alexabraham.dev \
  --subject-alternative-names www.alexabraham.dev \
  --validation-method DNS --region us-east-1
```
Add the returned CNAME validation records to DNS. Wait for `Status: ISSUED`.

**Add custom domain resources to `template.yaml`** (one pair per domain):
```yaml
NetDomain:
  Type: AWS::ApiGatewayV2::DomainName
  Properties:
    DomainName: alexabraham.net
    DomainNameConfigurations:
      - CertificateArn: <net-cert-arn>
        EndpointType: REGIONAL
        SecurityPolicy: TLS_1_2
NetMapping:
  Type: AWS::ApiGatewayV2::ApiMapping
  Properties:
    ApiId: !Ref SiteHttpApi
    DomainName: !Ref NetDomain
    Stage: $default
```
Repeat for `alexabraham.dev`. Then `sam deploy`.

**DNS** (apex requires ALIAS/ANAME — not plain CNAME):
- Apex (`alexabraham.net`, `alexabraham.dev`): Route 53 ALIAS A/AAAA → API GW regional domain, or ANAME if using Cloudflare/DNSimple
- `www`: plain CNAME → API GW regional domain

### 5. GCP cutover
1. Lower TTL on GCP DNS records to 60s (24–48 hours in advance)
2. Verify Lambda site end-to-end on custom domain (form submission delivers email)
3. Swap DNS from GCP App Engine targets to API GW targets
4. Soak 24–48 hours, then decommission GCP App Engine
