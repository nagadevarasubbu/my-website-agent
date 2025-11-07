import os
import subprocess
from pathlib import Path

# ✅ Your S3 bucket
S3_BUCKET = "my-website-agent-output"

BASE_DIR = Path(__file__).resolve().parent
STATIC_SITE_DIR = BASE_DIR / "static_site"

def deploy():
    print("🚀 Deploying website to S3...")
    cmd = f"aws s3 sync {STATIC_SITE_DIR} s3://{S3_BUCKET} --delete"
    result = subprocess.call(cmd, shell=True)
    if result == 0:
        print("✅ Deployment complete! Website is now live on CloudFront 🎉")
    else:
        print("❌ Deployment FAILED — Check AWS credentials / IAM role.")

if __name__ == "__main__":
    deploy()
