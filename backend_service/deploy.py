import subprocess
from pathlib import Path
import requests
import boto3
from datetime import datetime
import json

# ---------- AWS CONFIG ----------
S3_BUCKET = "my-website-agent-output"
CLOUDFRONT_ID = "E25Q9X6SJA9ERD"
DYNAMO_TABLE = "WebsiteDeployments"  # ✅ create this table in DynamoDB
AWS_REGION = "us-east-1"

# ---------- FRIEND AGENT ----------
FRIEND_CALLBACK_URL = "https://webhook.site/bfdf0876-a200-4f30-8df1-88d0ca1c40e9"  # 🔄 update

BASE_DIR = Path(__file__).resolve().parent
STATIC_SITE_DIR = BASE_DIR / "static_site"

# ---------- DYNAMODB LOGGER ----------
def log_to_dynamodb(status: str, message: str):
    """
    Records each deployment event in DynamoDB.
    Partition key: 'deployment_id' (timestamp-based unique key)
    """
    try:
        dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
        table = dynamodb.Table(DYNAMO_TABLE)

        item = {
            "deployment_id": datetime.utcnow().strftime("%Y%m%d%H%M%S"),
            "timestamp": datetime.utcnow().isoformat(),
            "status": status,
            "message": message,
            "s3_bucket": S3_BUCKET,
            "cloudfront_id": CLOUDFRONT_ID,
            "cloudfront_url": "https://d35x17h179ym5e.cloudfront.net"
        }

        table.put_item(Item=item)
        print("🗂️  Logged deployment to DynamoDB successfully.")
    except Exception as e:
        print(f"⚠️  Failed to log to DynamoDB: {e}")

# ---------- FRIEND CALLBACK ----------
def notify_friend_agent():
    """
    Sends a POST request to your friend's agent once deployment completes successfully.
    """
    payload = {
        "status": "success",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "✅ Website deployed successfully to AWS S3 + CloudFront",
        "cloudfront_url": "https://d35x17h179ym5e.cloudfront.net",
        "s3_bucket": S3_BUCKET
    }

    try:
        print("📡 Notifying Friend Agent...")
        response = requests.post(FRIEND_CALLBACK_URL, json=payload, timeout=8)
        if response.status_code == 200:
            print("📤 Successfully notified Friend Agent!")
        else:
            print(f"⚠️ Friend Agent responded with status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Failed to notify Friend Agent: {e}")

# ---------- DEPLOY ----------
def deploy():
    print("🚀 Deploying website to S3...")

    # ✅ Sync with trailing slashes (ensures deletion correctness)
    sync_cmd = f"aws s3 sync {STATIC_SITE_DIR}/ s3://{S3_BUCKET}/ --delete"
    print(f"🔧 Running: {sync_cmd}")
    subprocess.call(sync_cmd, shell=True)

    print("🔄 Invalidating CloudFront Cache...")
    invalidate_cmd = (
        f"aws cloudfront create-invalidation "
        f"--distribution-id {CLOUDFRONT_ID} "
        f"--paths '/*'"
    )
    print(f"🔧 Running: {invalidate_cmd}")
    subprocess.call(invalidate_cmd, shell=True)

    print("✅ Deployment fully complete! 🎉")

    # ✅ Log to DynamoDB
    log_to_dynamodb("success", "Website deployed successfully to AWS S3 + CloudFront.")

    # ✅ Send callback notification
    notify_friend_agent()

if __name__ == "__main__":
    deploy()
