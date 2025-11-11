import os
import requests
import subprocess
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SITE_DIR = BASE_DIR / "static_site"
IMG_DIR = SITE_DIR / "assets" / "images"
AUDIO_DIR = SITE_DIR / "assets" / "audio"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def write_page(filename: str, html_content: str):
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    (SITE_DIR / filename).write_text(html_content, encoding="utf-8")

def download(url: str, out_path: Path):
    try:
        r = requests.get(url, stream=True, timeout=10)
        if r.status_code == 200:
            with open(out_path, "wb") as f:
                f.write(r.content)
            print(f"✅ Downloaded: {url}")
        else:
            print(f"[WARN] Failed to download {url}: HTTP {r.status_code}")
    except Exception as e:
        print(f"[ERROR] Download failed {url}: {e}")

@app.post("/bootstrap")
async def bootstrap(request: Request):
    data = await request.json()

    pages = data["pages"]
    images_needed = data["images_needed"]
    voices_needed = data["voice_scripts_needed"]
    callback = data.get("callback_url_for_assets")  # ✅ FIXED

    # ✅ Save HTML pages
    for page in pages:
        write_page(page["filename"], page["html_file"])

    return {
        "status": "site initialized ✅",
        "images_needed": images_needed,
        "voice_scripts_needed": voices_needed,
        "callback_url_for_assets": callback   # ✅ RETURN IT
    }

@app.post("/submit-assets")
async def submit_assets(request: Request):
    data = await request.json()

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    # ✅ Save images
    for img in data.get("images", []):
        download(img["file_url"], IMG_DIR / f"{img['id']}.png")

    # ✅ Save audio
    for v in data.get("voices", []):
        download(v["file_url"], AUDIO_DIR / f"audio_{v['id']}.mp3")

    # ✅ Update HTML placeholders
    for html_file in SITE_DIR.glob("*.html"):
        content = html_file.read_text()

        # Replace image placeholders dynamically
        for section in ["hero", "about", "services", "contact", "departments", "doctors", "menu", "chefs"]:
            content = content.replace(
                f"<!-- IMAGE_PLACEHOLDER:{section} -->",
                f"<img class='section-img' src='assets/images/{section}.png' />"
            )

        html_file.write_text(content)

    # ✅ Auto deploy to S3
    print("🚀 Deploying website to S3...")
    subprocess.call("python3 deploy.py", cwd=BASE_DIR, shell=True)

    return {"status": "✅ Assets injected + Website deployed to CloudFront!"}

@app.get("/health")
async def health():
    return {"status": "ok"}
