from typing import Dict, Any, List
import re
import os
import json
from textwrap import dedent
import google.generativeai as genai

# ---------- Configure Gemini ----------
genai.configure(api_key=os.getenv("AIzaSyAaYENJEtAHp2qvF-uCESKRWy6QeRB0RQc")) 
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------- helpers ----------
def slug_hyphen(s: str) -> str:
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

# ---------- theme color selection ----------
def pick_theme_color(website_type: str) -> str:
    wt = website_type.lower()
    if any(k in wt for k in ["hospital", "health", "clinic", "care"]):
        return "#4A63FF"
    if any(k in wt for k in ["gym", "fitness", "sports"]):
        return "#FF6B3D"
    if any(k in wt for k in ["spa", "yoga", "wellness"]):
        return "#6A8CAF"
    if any(k in wt for k in ["school", "education", "training"]):
        return "#8A5AFF"
    if any(k in wt for k in ["tech", "software", "it", "digital"]):
        return "#0057FF"
    return "#4A63FF"  # default

# ---------- fallback text ----------
def fallback_section_text(section: str, site_name: str, website_type: str) -> str:
    return dedent(f"""
        {section} at {site_name}

        {section} plays an important role in what we do at {site_name}.
        As a {website_type} organization, we focus on clarity, trust, and support.

        On this page, you will find helpful information and guidance.
        We are here to assist and provide a meaningful experience.
    """).strip()

# ---------- GPT Section Writer ----------
def generate_sections_with_gemini(business_name: str, website_type: str, sections: List[str]) -> Dict[str, str]:
    prompt = dedent(f"""
        You are a professional website content writer.

        business_name: {business_name}
        website_type: {website_type}
        sections: {sections}

        For each section, write **2–3 paragraphs** (6–12 sentences total).
        Warm, human tone. Clear and useful.
        No repeating the section title in first sentence.
        No filler like "This section provides".
        
        Return JSON:
        {{
          "sections": [
            {{ "title": "...", "content": "..." }}
          ]
        }}
    """)

    try:
        response = model.generate_content(prompt)
        data = json.loads(response.text)

        final = {}
        for sec in data.get("sections", []):
            if sec.get("title") and sec.get("content"):
                final[sec["title"]] = sec["content"]
        return final
    except:
        return {}

# ---------- Styles (uses theme color) ----------
def build_styles(primary: str) -> str:
    return dedent(f"""
        :root {{
          --primary: {primary};
          --primary-hover: {primary};
          --text: #1C1F33;
          --subtext: #4A4F63;
          --border: #E6E8F0;
          --bg-light: #F7F9FF;
        }}

        body {{ margin:0; font-family:'Inter',system-ui,Arial; line-height:1.7; color:var(--text); }}

        .navbar {{ display:flex; justify-content:space-between; align-items:center; padding:24px 60px; border-bottom:1px solid var(--border); background:white; }}
        .navbar .brand {{ font-size:1.35rem; font-weight:600; }}
        .navbar .links a {{ margin-left:24px; text-decoration:none; color:var(--text); opacity:.85; font-weight:500; }}
        .navbar .links a:hover {{ opacity:1; color:var(--primary); }}

        .hero {{ padding:80px 60px; background:linear-gradient(135deg, var(--bg-light), #ffffff); }}
        .hero h1 {{ font-size:3rem; font-weight:700; margin-bottom:18px; }}
        .hero p {{ font-size:1.2rem; color:var(--subtext); max-width:620px; }}

        .grid {{ display:grid; gap:32px; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); padding-top:20px; }}
        .card {{ background:white; border:1px solid var(--border); border-radius:18px; padding:28px; transition:0.3s; }}
        .card:hover {{ transform:translateY(-6px); border-color:var(--primary); background:var(--bg-light); }}

        .btn {{ background:var(--primary); color:white; padding:12px 20px; border-radius:8px; text-decoration:none; font-weight:500; }}
        .btn:hover {{ background:var(--primary-hover); }}

        section {{ padding:60px 60px; }}
        .section-body {{ max-width:900px; margin:auto; }}
        .section-body h2 {{ font-size:2rem; margin-bottom:24px; }}
        .section-body p {{ font-size:1.12rem; color:var(--subtext); margin-bottom:26px; }}
        .section-body img {{ width:100%; border-radius:14px; margin:28px 0; object-fit:cover; }}

        footer {{ padding:30px; text-align:center; border-top:1px solid var(--border); color:var(--subtext); }}
    """).strip()

# ---------- HOME ----------
def build_home_html(site_name: str, sections: List[str], theme: str) -> str:
    nav_links = " ".join(f"<a href='{slug_hyphen(s)}.html'>{html_escape(s)}</a>" for s in sections)
    cards = "\n".join(f"""
        <div class="card">
            <h3>{html_escape(s)}</h3>
            <p>Learn more about {html_escape(s)}.</p>
            <a class="btn" href="{slug_hyphen(s)}.html">View</a>
        </div>
    """.strip() for s in sections)

    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<title>{html_escape(site_name)}</title>
<style>{build_styles(theme)}</style>
</head>
<body>

<nav class="navbar">
  <div class="brand">{html_escape(site_name)}</div>
  <div class="links">{nav_links}</div>
</nav>

<section class="hero">
  <!-- IMAGE_PLACEHOLDER:home_hero -->
  <h1>Welcome to {html_escape(site_name)}</h1>
  <p>Your trusted destination.</p>
  <button class="btn" onclick="document.getElementById('audio_site_intro').play()">🔊 Listen</button>
  <audio id="audio_site_intro" src="assets/audio/site_intro.mp3"></audio>
</section>

<section>
  <h2>Explore Sections</h2>
  <div class="grid">{cards}</div>
</section>

<footer>© {html_escape(site_name)}</footer>
</body>
</html>"""

# ---------- SECTIONS ----------
def build_section_html(site_name: str, section_name: str, summary_text: str, theme: str) -> str:
    sid = slug_hyphen(section_name)
    parts = [p.strip() for p in summary_text.split("\n\n") if p.strip()]
    while len(parts) < 3: parts.append(parts[-1])
    p1, p2, p3 = parts[0], parts[1], parts[2]

    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<title>{html_escape(section_name)} — {html_escape(site_name)}</title>
<style>{build_styles(theme)}</style>
</head>
<body>

<nav class="navbar">
  <a class="btn" href="index.html">← Back</a>
  <div class="brand">{html_escape(section_name)}</div>
</nav>

<section class="section-body">
  <h2>{html_escape(section_name)}</h2>

  <p>{html_escape(p1)}</p>
  <!-- IMAGE_PLACEHOLDER:{sid}_img1 -->

  <p>{html_escape(p2)}</p>
  <!-- IMAGE_PLACEHOLDER:{sid}_img2 -->

  <p>{html_escape(p3)}</p>
</section>

<footer>© {html_escape(site_name)}</footer>
</body>
</html>"""

# ---------- IMAGES + NARRATION ----------
def make_image_prompts(website_type: str, site_name: str, sections_4: List[str]):
    prompts = [{"id": "home_hero", "description": f"Hero banner for a {website_type} website '{site_name}'. Clean and warm."}]
    for sec in sections_4:
        sid = slug_hyphen(sec)
        prompts.append({"id": f"{sid}_img1", "description": f"Primary image for '{sec}'."})
        prompts.append({"id": f"{sid}_img2", "description": f"Supporting contextual image for '{sec}'."})
    return prompts

def make_site_narration(site_name: str, website_type: str, sections_4: List[str]):
    listed = ", ".join(sections_4[:-1]) + (", and " + sections_4[-1])
    return f"Welcome to {site_name}, your trusted {website_type} destination. Explore {listed}."

# ---------- MAIN ----------
def generate_website_package(payload: Dict[str, Any]):
    website_type = (payload.get("website_type") or "business").strip()
    business_name = payload.get("business_name") or "My Website"
    sections_all = payload.get("sections_required") or []
    sections_4 = [s.strip() for s in sections_all][:4] or ["About", "Services", "Team", "Contact"]

    theme = pick_theme_color(website_type)

    sections_content = generate_sections_with_gemini(business_name, website_type, sections_4)

    pages = [{"filename": "index.html", "html_file": build_home_html(business_name, sections_4, theme)}]

    for sec in sections_4:
        text = sections_content.get(sec) or fallback_section_text(sec, business_name, website_type)
        pages.append({"filename": f"{slug_hyphen(sec)}.html", "html_file": build_section_html(business_name, sec, text, theme)})

    return {
        "pages": pages,
        "images_needed": make_image_prompts(website_type, business_name, sections_4),
        "voice_scripts_needed": [{"id": "site_intro", "script": make_site_narration(business_name, website_type, sections_4)}],
        "callback_url_for_assets": payload.get("callback_url_for_assets") or "http://54.167.58.174:9000/submit-assets"
    }
