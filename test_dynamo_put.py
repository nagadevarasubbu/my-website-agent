# test_dynamo_put.py
import boto3
from datetime import datetime
import json

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("WebsiteDeployments")

item = {
    "deployment_id": datetime.utcnow().strftime("%Y%m%d%H%M%S"),
    "timestamp": datetime.utcnow().isoformat(),
    "status": "test",
    "message": "test deployment from EC2",
    "s3_bucket": "my-website-agent-output",
    "cloudfront_id": "E25Q9X6SJA9ERD",
    "cloudfront_url": "https://d35x17h179ym5e.cloudfront.net"
}

resp = table.put_item(Item=item)
print("PutItem response:", resp)
