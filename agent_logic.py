from typing import Dict, Any, List
import re
from textwrap import dedent

# ---------- helpers ----------

def slug_hyphen(s: str) -> str:
    """Lowercase + hyphen slug: 'Patient Information' -> 'patient-information'."""
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s.strip().lower())
    return re.sub(r'-+', '-', s).strip('-')

def html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
         .replace("'", "&#39;")
    )

# ---------- page builders ----------

def build_styles() -> str:
    # keep simple, clean defaults
    return dedent("""
        body { font-family: system-ui, Arial, sans-serif; margin: 0; color: #111; }
        .navbar { display:flex; align-items:center; gap:16px; padding:14px 20px; background:#111; color:#fff; }
        .navbar .brand { font-weight: 700; letter-spacing: .3px; }
        .navbar .links a { color:#fff; text-decoration:none; margin-right:14px; opacity:.9 }
        .navbar .links a:hover { opacity:1; text-decoration:underline; }
        .hero { display:grid; gap:16px; padding:40px 20px; background:#f7f7f9; }
        .grid { display:grid; gap:16px; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }
        .card { border:1px solid #e9e9ee; border-radius:12px; padding:18px; background:#fff; }
        .btn { display:inline-block; padding:10px 14px; border-radius:10px; border:1px solid #ddd; background:#fff; cursor:pointer; }
        .btn:hover { background:#f3f3f7; }
        section { padding:28px 20px; }
        footer { padding:24px 20px; text-align:center; background:#fafafa; border-top:1px solid #eee; color:#444; }
        .img { width:100%; height:auto; display:block; border-radius:12px; border:1px solid #eee; }
        .voice { margin-top:8px; }
    """).strip()

def build_home_html(site_name: str, sections: List[str]) -> str:
    nav_links = " ".join(
        [f"<a href='{slug_hyphen(s)}.html'>{html_escape(s)}</a>" for s in sections]
    )
    cards = "\n".join(
        [
            f"""
            <div class="card">
              <h3>{html_escape(s)}</h3>
              <p>Learn more about {html_escape(s)} at {html_escape(site_name)}.</p>
              <a class="btn" href="{slug_hyphen(s)}.html">Open {html_escape(s)}</a>
            </div>
            """.strip()
            for s in sections
        ]
    )

    # hero uses image id: home_hero
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>{html_escape(site_name)}</title>
  <link rel="stylesheet" href="assets/styles.css" />
  <style>{build_styles()}</style>
</head>
<body>

<nav class="navbar">
  <div class="brand">{html_escape(site_name)}</div>
  <div class="links">{nav_links}</div>
</nav>

<section class="hero">
  <!-- IMAGE_PLACEHOLDER:home_hero -->
  <div>
    <h1>Welcome to {html_escape(site_name)}</h1>
    <p>Explore our key sections below.</p>
    <div class="voice">
      <button class="btn" onclick="document.getElementById('audio_site_intro').play()">🔊 Listen</button>
      <audio id="audio_site_intro" src="assets/audio/site_intro.mp3"></audio>
    </div>
  </div>
</section>

<section>
  <h2>Explore Sections</h2>
  <div class="grid">
    {cards}
  </div>
</section>

<footer>
  <p>© {html_escape(site_name)} — Powered by AI Website Agent</p>
</footer>

</body>
</html>"""

def build_section_html(site_name: str, section_name: str, summary_text: str) -> str:
    sid = slug_hyphen(section_name)
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>{html_escape(section_name)} — {html_escape(site_name)}</title>
  <link rel="stylesheet" href="assets/styles.css" />
  <style>{build_styles()}</style>
</head>
<body>

<nav class="navbar">
  <a class="btn" href="index.html">← Home</a>
  <div class="brand">{html_escape(section_name)}</div>
</nav>

<section>
  <h2>{html_escape(section_name)}</h2>
  <p>{html_escape(summary_text)}</p>

  <!-- IMAGE_PLACEHOLDER:{sid}_img1 -->
  <!-- IMAGE_PLACEHOLDER:{sid}_img2 -->
</section>

<footer>
  <p>© {html_escape(site_name)}</p>
</footer>

</body>
</html>"""

# ---------- prompt builders ----------

def make_image_prompts(website_type: str, site_name: str, sections_4: List[str]) -> List[Dict[str, str]]:
    prompts: List[Dict[str, str]] = []

    # hero
    prompts.append({
        "id": "home_hero",
        "description": f"Wide hero banner for a {website_type} website named '{site_name}'. Clean, modern, welcoming."
    })

    # 2 images per section
    for idx, sec in enumerate(sections_4, start=1):
        sid = slug_hyphen(sec)
        # primary image prompt
        prompts.append({
            "id": f"{sid}_img1",
            "description": f"Primary image for the '{sec}' section of a {website_type} site. Professional, high-quality, relevant to {sec}."
        })
        # supporting image prompt
        prompts.append({
            "id": f"{sid}_img2",
            "description": f"Supporting image for the '{sec}' section. Complementary visual that reinforces {sec} context."
        })

    return prompts

def make_site_narration(site_name: str, website_type: str, sections_4: List[str]) -> str:
    listed = ", ".join(sections_4[:-1]) + (", and " + sections_4[-1] if len(sections_4) > 1 else (sections_4[0] if sections_4 else ""))
    return dedent(f"""
        Welcome to {site_name}, your trusted {website_type} destination online.
        On this website you can explore {listed}. Each page is designed to be clear, fast, and useful.
        Use the navigation to jump into any section, or return to the home page at any time.
        Thank you for visiting {site_name}.
    """).strip()

# ---------- main generator ----------

def generate_website_package(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Input (from friend's agent via N8N):
      {
        "website_type": "hospital",
        "business_name": "Sunshine General Hospital",
        "sections_required": ["Home","Services","Doctors","Patient Information","Community","Contact"],
        "callback_url_for_assets": "http://<ip>:9000/submit-assets"   # optional
      }
    Output (used by N8N):
      - pages (for your /bootstrap)
      - images_needed (9)
      - voice_scripts_needed (1)
      - callback_url_for_assets
    """
    website_type = (payload.get("website_type") or "business").strip()
    business_name = payload.get("business_name") or payload.get("website_type") or "My Website"
    sections_all: List[str] = payload.get("sections_required") or []
    # Always take FIRST 4 sections as per your rule
    sections_4: List[str] = [s for s in sections_all if s.strip()][:4] or ["About", "Services", "Team", "Contact"]

    # Build pages
    pages = []
    pages.append({
        "filename": "index.html",
        "html_file": build_home_html(business_name, sections_4)
    })
    for sec in sections_4:
        summary = f"Information and highlights about {sec} at {business_name}."
        pages.append({
            "filename": f"{slug_hyphen(sec)}.html",
            "html_file": build_section_html(business_name, sec, summary)
        })

    # Prompts: 1 hero + 2 per section = 9 for 4 sections
    images_needed = make_image_prompts(website_type, business_name, sections_4)

    # Voice: single narration for home page
    voice_scripts_needed = [{
        "id": "site_intro",
        "script": make_site_narration(business_name, website_type, sections_4)
    }]

    # Callback: prefer request value; else default to your EC2
    callback_url = payload.get("callback_url_for_assets") or "http://54.167.58.174:9000/submit-assets"

    return {
        "pages": pages,
        "images_needed": images_needed,
        "voice_scripts_needed": voice_scripts_needed,
        "callback_url_for_assets": callback_url
    }
