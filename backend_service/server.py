import os
import requests
import subprocess
from fastapi import FastAPI, Request, UploadFile, File, Form
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
    print(f"📥 Downloading → {url}")
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(out_path, "wb") as f:
            f.write(r.content)
        print(f"✅ Saved → {out_path}")
    else:
        print(f"⚠️ Failed → {url}")

@app.post("/bootstrap")
async def bootstrap(request: Request):
    data = await request.json()

    pages = data["pages"]
    images_needed = data["images_needed"]
    voices_needed = data["voice_scripts_needed"]
    callback_url = data.get("callback_url_for_assets")

    for page in pages:
        write_page(page["filename"], page["html_file"])

    return {
        "status": "site initialized",
        "images_needed": images_needed,
        "voice_scripts_needed": voices_needed,
        "callback_url_for_assets": callback_url
    }

@app.post("/submit-assets")
async def submit_assets(request: Request):
    content_type = request.headers.get("content-type", "")

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    # ✅ CASE 1: JSON (URL based assets)
    if "application/json" in content_type:
        data = await request.json()

        # Images
        for img in data.get("images", []):
            download(img["file_url"], IMG_DIR / f"{img['id']}.png")

        # Voice (URL mp3)
        for v in data.get("voices", []):
            download(v["file_url"], AUDIO_DIR / f"{v['id']}.mp3")

    # ✅ CASE 2: Multipart form-data (binary audio upload)
    elif "multipart/form-data" in content_type:
        form = await request.form()
        for key, file in form.items():
            if hasattr(file, "filename"):
                out_file = AUDIO_DIR / file.filename
                with open(out_file, "wb") as f:
                    f.write(await file.read())
                print(f"✅ Uploaded Binary Voice File → {out_file}")
    else:
        return {"error": "Unsupported input format. Send JSON or multipart."}

    # ✅ Insert images into site pages (replace placeholders)
    for html_file in SITE_DIR.glob("*.html"):
        content = html_file.read_text()

        for img_file in IMG_DIR.glob("*.png"):
            img_id = img_file.stem
            placeholder = f"<!-- IMAGE_PLACEHOLDER:{img_id} -->"
            tag = f"<img src='assets/images/{img_id}.png' class='section-image'/>"
            content = content.replace(placeholder, tag)

        # Voice Button always plays `audio/site_intro.mp3`
        if "site_intro.mp3" in [x.name for x in AUDIO_DIR.iterdir()]:
            content = content.replace(
                "<!-- VOICE_PLACEHOLDER -->",
                "<button class='voice-btn' onclick=\"document.getElementById('audio_site_intro').play()\">🔊 Listen</button>\n<audio id='audio_site_intro' src='assets/audio/site_intro.mp3'></audio>"
            )

        html_file.write_text(content)

    # ✅ Deploy to S3
    print("🚀 Deploying website to S3...")
    subprocess.call("python3 deploy.py", cwd=BASE_DIR, shell=True)
    print("✅ Deployment complete! CloudFront updated 🎉")

    return {"status": "assets injected + deployed ✅"}

@app.get("/health")
async def health():
    return {"status": "ok"}
