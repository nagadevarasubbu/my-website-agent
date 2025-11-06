import os
import base64
import zipfile
import requests
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
    """Writes HTML content to a file inside static site directory."""
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    (SITE_DIR / filename).write_text(html_content, encoding="utf-8")


def download(url: str, out_path: Path):
    """Download a file from the internet."""
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(out_path, "wb") as f:
            f.write(r.content)
    else:
        print(f"[WARN] Failed to download: {url}")


@app.post("/bootstrap")
async def bootstrap(request: Request):
    data = await request.json()

    pages = data["pages"]
    images_needed = data["images_needed"]
    voices_needed = data["voice_scripts_needed"]

    for page in pages:
        filename = page["filename"]
        html = page["html_file"]
        write_page(filename, html)

    return {
        "status": "site initialized",
        "images_needed": images_needed,
        "voice_scripts_needed": voices_needed
    }


@app.post("/submit-assets")
async def submit_assets(request: Request):
    """
    Friend's agent or image/voice team calls this.
    They send: { images: [{id, file_url}], voices: [{id, file_url}] }
    """
    data = await request.json()

    # Ensure folders exist
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    # Save Images
    for img in data.get("images", []):
        out = IMG_DIR / f"{img['id']}.png"
        download(img["file_url"], out)

    # Save Audio
    for v in data.get("voices", []):
        out = AUDIO_DIR / f"audio_{v['id']}.mp3"
        download(v["file_url"], out)

    # Now inject into ALL HTML pages
    for html_file in SITE_DIR.glob("*.html"):
        content = html_file.read_text()

        # HERO special case (background banner)
        content = content.replace("<!-- IMAGE_PLACEHOLDER:hero -->",
                                  "<div class='hero-bg' style=\"background-image:url('assets/images/hero.png');\"></div>")

        # Other sections (normal inserted images)
        for section in ["departments", "doctors", "contact"]:
            content = content.replace(f"<!-- IMAGE_PLACEHOLDER:{section} -->",
                                      f"<img class='section-img' src='assets/images/{section}.png' />")

        html_file.write_text(content)

    return {"status": "assets injected successfully"}


@app.post("/deploy")
async def deploy():
    """
    Packages static site and uploads to S3 (you already configured bucket).
    """
    zip_path = BASE_DIR / "site_package.zip"
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w") as z:
        for root, dirs, files in os.walk(SITE_DIR):
            for file in files:
                full_path = os.path.join(root, file)
                rel = os.path.relpath(full_path, SITE_DIR)
                z.write(full_path, rel)

    return {"status": "ready-to-upload", "zip_path": str(zip_path)}
