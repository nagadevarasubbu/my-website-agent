# 🚀 AI-Driven Automated Website Generator

Fully automated website creation using **Google Gemini + FastAPI + AWS S3 + CloudFront + DynamoDB**

---

## 📌 Overview

This project automatically generates a complete, professional, fully deployed website using only basic business inputs.

Once a user provides:

* **Business Name**
* **Website Type**
* **Required Sections**

The system automatically:

* Refines Inputs using AI
* Generates detailed content using Google Gemini
* Creates image & audio requirements
* Builds all HTML pages dynamically
* Deploys website to AWS S3 + CloudFront
* Logs deployment to DynamoDB
* Sends status callback to the requesting agent

> ✅ No manual coding… no design work… everything is automated.

---

## 📁 Project Structure

```
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
```

---

## ⚙️ Prerequisites

* Python **3.9+**
* AWS CLI configured
* EC2 Instance (Amazon Linux 2023)
* IAM Role with:

  * S3 Access
  * CloudFront Access
  * DynamoDB Access
* Google Gemini API Key

---

## 🔧 1. Setup — Agent API Service (Port 8000)

### Navigate to project:

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

### Start FastAPI server:

```bash
pkill -f uvicorn     # stop old instance (optional)
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

## 🖥️ 3. Running Both Services Using `tmux` (Recommended)

### Install tmux:

```bash
sudo yum install -y tmux
```

### ▶ Start Agent API tmux session:

```bash
tmux new -s ris
cd ~/my-website-agent/agent_api
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

Detach:
**CTRL + B**, then **D**

### ▶ Start Backend Service tmux session:

```bash
tmux new -s oj
cd ~/my-website-agent/backend_service
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 9000
```

Re-attach anytime:

```bash
tmux attach -t oj
tmux attach -t ris
```

---

## 🧠 4. How the System Works

### **Workflow**

1. n8n sends payload → `/generate-website`
2. **agent_api** (Port 8000):

   * Refines inputs
   * Generates content using Gemini
   * Produces HTML + image prompts + voice scripts
3. **backend_service** (Port 9000):

   * Receives assets
   * Builds final website
   * Deploys to S3
   * Invalidates CloudFront
   * Logs to DynamoDB
   * Sends callback

> 🔄 Everything is fully automated.

---

## 🌐 5. Deployment Process

Inside **backend_service**:

```bash
python3 deploy.py
```

This script:

* Uploads `static_site/` → S3
* Clears CloudFront cache
* Logs deployment to DynamoDB
* Sends callback

---

## 🔑 6. Environment Variables

### **Agent API**

```bash
export GOOGLE_API_KEY="your_key"
```

### **Backend Service**

```bash
export DEPLOY_S3_BUCKET="my-website-agent-output"
export DEPLOY_CF_ID="E25Q9X6SJA9ERD"
export DYNAMO_TABLE="WebsiteDeploymentLogs"
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

### Port already in use:

```bash
pkill -f uvicorn
```

### Forgot tmux session:

```bash
tmux ls
tmux attach -t <name>
```

### S3 deploy not updating:

* Ensure CloudFront invalidation works
* Ensure S3 bucket permissions
* Ensure EC2 IAM role access

---

## 🎯 Conclusion

This project automates the entire lifecycle of website creation — from AI-generated content to hosting and deployment logs. With only minimal inputs, the system delivers a fully deployed, professional-grade website.

> 🚀 **True end-to-end AI automation.**
