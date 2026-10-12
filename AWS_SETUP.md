# AWS_SETUP.md

## Overview
MonsoonReady AI can store incident photos either locally (demo mode) or in a private Amazon S3 bucket. The S3 integration is optional and only activated when the required environment variables are present.

## Required environment variables
Create a `.env` file (or set variables in your deployment environment) with the following keys:
```dotenv
# General configuration
LOCAL_DEMO=true                 # Set to "false" to enable real AWS mode

# AWS credentials – required only when LOCAL_DEMO=false
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION=us-east-1    # Adjust to your preferred region
S3_BUCKET_NAME=your-bucket-name
```
- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` must belong to an IAM user or role that has **PutObject**, **GetObject**, and **ListBucket** permissions on the bucket.
- The bucket **must not be public**; we only generate presigned URLs for temporary access.

## IAM policy example (minimum permissions)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::your-bucket-name",
        "arn:aws:s3:::your-bucket-name/*"
      ]
    }
  ]
}
```
Attach this policy to the IAM user/role.

## Local demo mode
When `LOCAL_DEMO=true` (default), photos are stored under `backend/app/uploads/` and the backend returns a `file://` URL via the `/presigned/{report_id}` endpoint. No AWS traffic occurs, and the health endpoint reports status **LOCAL_DEMO**.

## Verifying the configuration
1. Start the FastAPI server (`uvicorn backend/app/main:app --reload`).
2. Call **GET** `/health`:
   - Returns `{ "status": "LOCAL_DEMO" }` if demo mode.
   - Returns `{ "status": "CONNECTED" }` if all AWS variables are present and a test upload succeeded.
   - Returns `{ "status": "NOT_CONFIGURED" }` if variables are missing or the upload check fails.

## Troubleshooting
- **401/403 errors** – check IAM policy and that the credentials match the bucket.
- **Missing bucket** – create the bucket first, then set `S3_BUCKET_NAME`.
- **Network issues** – ensure the machine can reach the S3 endpoint (no firewall blocks).

**Never** commit real credentials to the repository. Use the `.env.example` file as a template.
