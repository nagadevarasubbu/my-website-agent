from typing import Dict, Any, List
import re
from textwrap import dedent
import google.generativeai as genai

genai.configure(api_key="AIzaSyAaYENJEtAHp2qvF-uCESKRWy6QeRB0RQc")


# ------------------- Helpers -------------------

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


# ------------------- Gemini Content Generator -------------------

def generate_section_content(business_name: str, website_type: str, section_name: str) -> str:
    prompt = f"""
Your task is to create high-quality website section content.

Write content for a section of a business website.

BUSINESS NAME: {business_name}
WEBSITE TYPE: {website_type}
SECTION NAME: {section_name}

CONTENT STYLE REQUIREMENTS:
- Tone: Professional, friendly, trustworthy.
- Write in natural human style (no robotic wording).
- Break content into clear meaningful paragraphs.
- Include a subheading that expands the section’s purpose.
- Include a short bullet list of benefits, features, or key points.
- Do NOT talk about images, web layout, placeholders, or voice scripts.
- Do NOT mention AI, generation, or prompts.

FORMAT EXACTLY LIKE THIS:

<h3>[Section Purpose Title]</h3>

<p>[Paragraph 1 introducing what this section means for the business and why it matters to visitors.]</p>

<p>[Paragraph 2 providing reassurance, trust-building details, and clarity.]</p>

<ul>
  <li>[Key point / benefit]</li>
  <li>[Key point / benefit]</li>
  <li>[Key point / benefit]</li>
</ul>
"""

    model = genai.GenerativeModel("gemini-2.5-flash") 
    response = model.generate_content(prompt)

    return response.text.strip()


# ------------------- CSS & Page Templates -------------------

def build_styles() -> str:
    return dedent("""
        body {
          margin: 0;
          font-family: 'Inter', system-ui, Arial, sans-serif;
          background: #FFFFFF;
          color: #1C1F33;
          line-height: 1.6;
        }

        .navbar {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 18px 32px;
          background: #ffffff;
          border-bottom: 1px solid #E6E8F0;
        }
        .navbar .brand {
          font-size: 1.25rem;
          font-weight: 600;
        }
        .navbar .links a {
          margin-left: 18px;
          text-decoration: none;
          color: #1C1F33;
          font-weight: 500;
        }
        .navbar .links a:hover {
          color: #4A63FF;
        }

        .hero img {
          width: 100%;
          height: 420px;
          object-fit: cover;
          border-radius: 16px;
        }

        .content-img {
          width: 100%;
          height: 340px;
          object-fit: cover;
          border-radius: 14px;
          margin-top: 16px;
          border: 1px solid #E6E8F0;
        }

        .grid {
          display: grid;
          gap: 18px;
          grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        }
        .card {
          background: #FFFFFF;
          border: 1px solid #E6E8F0;
          border-radius: 16px;
          padding: 20px;
          transition: 0.25s;
        }
        .card:hover {
          transform: translateY(-4px);
          background: #F7F9FF;
          border-color: #D7DBF5;
        }

        .btn {
          display: inline-block;
          background: #4A63FF;
          color: #FFFFFF;
          padding: 10px 18px;
          border-radius: 8px;
          text-decoration: none;
          font-weight: 500;
        }

        section { padding: 44px 32px; }

        footer {
          padding: 24px;
          text-align: center;
          border-top: 1px solid #E6E8F0;
          color: #555A6E;
        }
    """).strip()


def build_home_html(site_name: str, sections: List[str]) -> str:
    nav_links = " ".join([f"<a href='{slug_hyphen(s)}.html'>{html_escape(s)}</a>" for s in sections])
    cards = "\n".join([
        f"""
        <div class="card">
          <h3>{html_escape(s)}</h3>
          <p>Discover details, benefits, and helpful information in this section.</p>
          <a class="btn" href="{slug_hyphen(s)}.html">Open {html_escape(s)}</a>
        </div>
        """.strip()
        for s in sections
    ])

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
  <p>© {html_escape(site_name)}</p>
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
  <div class="section-body">{summary_text}</div>

  <!-- IMAGE_PLACEHOLDER:{sid}_img1 -->
  <!-- IMAGE_PLACEHOLDER:{sid}_img2 -->
</section>

<footer>
  <p>© {html_escape(site_name)}</p>
</footer>

</body>
</html>"""


# ------------------- MAIN GENERATOR -------------------

def generate_website_package(payload: Dict[str, Any]) -> Dict[str, Any]:
    website_type = (payload.get("website_type") or "business").strip()
    business_name = payload.get("business_name") or "My Website"
    sections_all: List[str] = payload.get("sections_required") or []
    sections_4: List[str] = [s for s in sections_all if s.strip()][:4]

    pages = []
    pages.append({
        "filename": "index.html",
        "html_file": build_home_html(business_name, sections_4)
    })

    for sec in sections_4:
        summary = generate_section_content(business_name, website_type, sec)
        pages.append({
            "filename": f"{slug_hyphen(sec)}.html",
            "html_file": build_section_html(business_name, sec, summary)
        })

    images_needed = []
    images_needed.append({"id": "home_hero", "description": f"Wide hero banner for {business_name} {website_type} website."})
    for sec in sections_4:
        sid = slug_hyphen(sec)
        images_needed.append({"id": f"{sid}_img1", "description": f"Primary image for {sec}."})
        images_needed.append({"id": f"{sid}_img2", "description": f"Supporting image for {sec}."})

    voice_scripts_needed = [{
        "id": "site_intro",
        "script": generate_section_content(business_name, website_type, "Overview")
    }]

    callback_url = payload.get("callback_url_for_assets") or "http://54.167.58.174:9000/submit-assets"

    return {
        "pages": pages,
        "images_needed": images_needed,
        "voice_scripts_needed": voice_scripts_needed,
        "callback_url_for_assets": callback_url
    }
