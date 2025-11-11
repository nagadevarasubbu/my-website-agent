import subprocess
from pathlib import Path

# ✅ Your S3 bucket
S3_BUCKET = "my-website-agent-output"

# ✅ Your CloudFront Distribution ID
CLOUDFRONT_ID = "E25Q9X6SJA9ERD"

BASE_DIR = Path(__file__).resolve().parent
STATIC_SITE_DIR = BASE_DIR / "static_site"

def deploy():
    print("🚀 Deploying website to S3...")

    # ✅ Sync with trailing slashes (required for deletion correctness)
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

    print("✅ Deployment fully complete!")

if __name__ == "__main__":
    deploy()
