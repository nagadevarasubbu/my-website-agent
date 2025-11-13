# 🚀 AI-Driven Automated Website Generator

Fully automated website creation using **Amazon Bedrock + FastAPI + AWS S3 + CloudFront + DynamoDB**

---

## 📌 Overview

This project automatically generates a complete, professional, fully deployed website using only basic business inputs.

When the user provides:

* **Business Name**
* **Website Type**
* **Required Sections**

The system automatically:

* Refines Inputs using **AI (Bedrock Agent Layer)**
* Generates detailed content using **Amazon Bedrock Claude Sonnet**
* Creates **image & audio requirements** for the media agent
* Builds all HTML pages dynamically
* Deploys website to **AWS S3 + CloudFront**
* Logs deployment to **DynamoDB**
* Sends a callback to the requesting agent

✔ **No manual coding… no design work… everything is automated.**

---

## 📁 Project Structure

```
my-website-agent/
│
├── agent_api/                         # AI Logic + Input Refinement
│   ├── main.py                        # FastAPI service (AI content generator)
│   ├── agent_logic.py                 # Website builder logic (Bedrock-based)
│   ├── agent_layer.py                 # Input refinement AI layer
│   ├── requirements.txt
│   ├── venv/
│
├── backend_service/                   # Website Assembly + Deployment
│   ├── server.py                      # Receives assets + builds static site
│   ├── deploy.py                      # S3 + CloudFront deploy + Dynamo logging
│   ├── db.py                          # DynamoDB writer
│   ├── static_site/                   # Auto-generated website
│   ├── requirements.txt
│   ├── venv/
│
├── README.md
└── dynamo_policy.json                 # IAM policy for Dynamo logging
```

---

## ⚙️ Prerequisites

* Python **3.9+**
* AWS CLI configured
* IAM Role with access to:

  * S3
  * CloudFront
  * DynamoDB
  * Amazon Bedrock InvokeModel
* EC2 Instance (Amazon Linux 2023)

➡️ **No Gemini API — Project uses Bedrock only.**

---

## 🔧 1. Setup — Agent API Service (Port 8000)

### Navigate:

```bash
cd ~/my-website-agent
cd my-website-agent/agent_api
```

### Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install requirements:

```bash
pip install -r requirements.txt
```

### Start FastAPI service:

```bash
pkill -f uvicorn   # optional
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 🔧 2. Setup — Backend Service (Port 9000)

### Navigate:

```bash
cd ~/my-website-agent/backend_service
```

### Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install requirements:

```bash
pip install -r requirements.txt
```

### Start backend server:

```bash
uvicorn server:app --host 0.0.0.0 --port 9000
```

---

## 🖥️ 3. Run Both Services Using tmux

### Install tmux:

```bash
sudo yum install -y tmux
```

### Run Agent API in tmux:

```bash
tmux new -s ris
cd ~/my-website-agent/agent_api
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

Detach: `CTRL + B`, then `D`

### Run Backend Service in tmux:

```bash
tmux new -s oj
cd ~/my-website-agent/backend_service
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 9000
```

Reattach anytime:

```bash
tmux attach -t oj
tmux attach -t ris
```

---

## 🧠 4. How the System Works

### agent_api (Port 8000)

* Refines inputs using **agent_layer**
* Generates website content using **Bedrock**
* Produces HTML structures, image prompts, audio scripts

### backend_service (Port 9000)

* Receives image & audio assets
* Builds final HTML pages
* Deploys to S3
* Invalidates CloudFront
* Logs deployment into DynamoDB
* Sends callback to requesting agent

✔ Everything happens automatically.

---

## 🌐 5. Deployment Process

Inside backend_service:

```bash
python3 deploy.py
```

This script:

* Uploads `static_site/` to S3
* Clears CloudFront cache
* Writes a DynamoDB log
* Notifies the agent

---

## 🔑 6. Environment Variables

### Backend

```
export DEPLOY_S3_BUCKET="my-website-agent-output"
export DEPLOY_CF_ID="E25Q9X6SJA9ERD"
export DYNAMO_TABLE="WebsiteDeploymentLogs"
```

### Bedrock

```
AWS credentials must allow InvokeModel
```

---

## 🧪 7. Testing

### Test DynamoDB Write:

```bash
python3 test_dynamo_put.py
```

### Test Agent API:

```bash
curl -X POST http://<EC2-IP>:8000/generate-website \
     -H "Content-Type: application/json" \
     -d '{"business_name":"Test","website_type":"Hospital","sections_required":["Home","Doctors"]}'
```

---

## 🪲 8. Troubleshooting

### Fix port in use:

```bash
pkill -f uvicorn
```

### List tmux sessions:

```bash
tmux ls
```

### Reattach:

```bash
tmux attach -t <name>
```

### S3 updates not showing:

* Confirm CloudFront invalidation
* Confirm bucket permissions

---

## 🎯 Conclusion

This system delivers **a fully automated AI-based website generator** powered by Amazon Bedrock and AWS infrastructure. With minimal input, the system handles:

* Text generation
* Image & audio requirement creation
* HTML assembly
* Deployment
* Logging

All completely automated end-to-end.
