🚀 AI-Driven Automated Website Generator
Fully automated website creation using Gemini + FastAPI + AWS S3 + CloudFront + DynamoDB

📌 Overview

This project automatically generates a complete, professional, fully deployed website using only basic business inputs.

Once a user provides:

Business Name
Website Type
Required Sections

The system automatically:

1.Refines Inputs using AI
2.Generates detailed content using Google Gemini
3.Creates image & audio requirements
4.Builds all HTML pages dynamically
5.Deploys website to AWS S3 + CloudFront
6.Logs deployment to DynamoDB
7.Sends status callback to the requesting agent

📁 Project Structure
my-website-agent/
│
├── agent_api/
│   ├── main.py               # FastAPI service (AI content generator)
│   ├── agent_logic.py        # Website builder logic (Gemini-based)
│   ├── agent_layer.py        # Input refinement AI layer
│   ├── requirements.txt
│   ├── venv/
│
├── backend_service/
│   ├── server.py             # Receives assets + builds static site
│   ├── deploy.py             # S3 + CloudFront deploy + Dynamo logging
│   ├── db.py                 # DynamoDB writer
│   ├── static_site/          # Auto-generated website
│   ├── requirements.txt
│   ├── venv/
│
├── README.md
└── dynamo_policy.json

⚙️ Prerequisites

Python 3.9+

AWS CLI configured

IAM Role with S3, CloudFront, DynamoDB access

EC2 Instance (Amazon Linux 2023)


🔧 1. Setup — Agent API Service (Port 8000)
Navigate to project:
cd ~/my-website-agent
cd my-website-agent/agent_api

Create virtual environment:
python3 -m venv venv
source venv/bin/activate

Install requirements:
pip install -r requirements.txt

Start FastAPI server:
pkill -f uvicorn     # stop old instance (optional)
uvicorn main:app --host 0.0.0.0 --port 8000

🔧 2. Setup — Backend Service (Port 9000)
Navigate:
cd ~/my-website-agent/backend_service

Create virtual environment:
python3 -m venv venv
source venv/bin/activate

Install requirements:
pip install -r requirements.txt

Start backend server:
uvicorn server:app --host 0.0.0.0 --port 9000

🖥️ 3. Running Both Services Using tmux (Recommended)
Install tmux:
sudo yum install -y tmux

Start Agent API tmux session
tmux new -s ris
cd ~/my-website-agent/agent_api
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000


Detach:

CTRL + B, then D

Start Backend Service tmux session
tmux new -s oj
cd ~/my-website-agent/backend_service
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 9000


Re-attach anytime:

tmux attach -t oj
tmux attach -t ris

🧠 4. How the System Works

n8n sends a payload → /generate-website

agent_api:

Refines inputs (agent_layer)

Generates website text (Gemini)

Outputs HTML pages, image prompts, voice scripts

backend_service:

Receives images/audio

Inserts them into HTML

Deploys to S3 bucket

Invalidates CloudFront

Logs to DynamoDB

Sends callback to friend's agent

Everything happens automatically.

🌐 5. Deployment Process

Inside backend_service:

python3 deploy.py


This script:

✔ Uploads static_site → S3
✔ Clears CloudFront cache
✔ Writes DynamoDB log
✔ Notifies requesting agent

🔑 6. Environment Variables
Agent API
export GOOGLE_API_KEY="your_key"

Backend Service
export DEPLOY_S3_BUCKET="my-website-agent-output"
export DEPLOY_CF_ID="E25Q9X6SJA9ERD"
export DYNAMO_TABLE="WebsiteDeploymentLogs"

🧪 7. Testing
Test DynamoDB Write:
python3 test_dynamo_put.py

Test Agent API:
curl -X POST http://<EC2-IP>:8000/generate-website \
     -H "Content-Type: application/json" \
     -d '{"business_name":"Test","website_type":"Hospital","sections_required":["Home","Doctors"]}'

🪲 8. Troubleshooting
Port already in use:
pkill -f uvicorn

tmux session forgot:
tmux ls
tmux attach -t <name>

S3 deploy not updating:

Ensure CloudFront invalidation works

Ensure bucket has permissions

🎯 Conclusion

This project delivers a complete automated website generation system powered by AI and AWS. With just a few API inputs, the entire website — content, images, audio, deployment, and logs — is created end-to-end.
