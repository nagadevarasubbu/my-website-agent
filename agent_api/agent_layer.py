import google.generativeai as genai
import json
from textwrap import dedent

# ---------- CONFIGURE GEMINI ----------
# (Optional Bedrock reference)
# from langchain_aws import ChatBedrock
# bedrock_model = ChatBedrock(model_id="anthropic.claude-3-sonnet-20240229-v1:0", region_name="us-east-1")

# 🔑 Set your Gemini API key directly here
genai.configure(api_key="AIzaSyDagMyFx-dxUIs4xtdqU4newjP39HsN6nQ") 

gemini_model = genai.GenerativeModel("gemini-2.5-flash") 

# ---------- AGENT: INPUT REFINEMENT ----------
def refine_website_inputs(business_name: str, website_type: str, sections: list):
    """
    Refines and enhances incoming website inputs for cleaner, structured generation.
    - Polishes business_name and website_type
    - Normalizes section titles
    - Ensures max 4 clean section names
    """

    prompt = dedent(f"""
        You are an AI website planning assistant.

        Inputs:
        - business_name: {business_name}
        - website_type: {website_type}
        - sections: {sections}

        Improve clarity and presentation.
        * Make business_name professional (e.g., 'Apollo Hospital', 'TechVerse Solutions').
        * Expand website_type for clarity (e.g., 'Healthcare & Patient Services', 'IT Software Solutions').
        * Capitalize and refine sections, ensuring 4 clean and relevant titles.

        Return JSON only:
        {{
          "business_name": "Refined name",
          "website_type": "Refined descriptive type",
          "sections": ["Section 1", "Section 2", "Section 3", "Section 4"]
        }}
    """)

    try:
        response = gemini_model.generate_content(prompt)
        text = response.text.strip().replace("```json", "").replace("```", "")
        data = json.loads(text)
        if not all(k in data for k in ["business_name", "website_type", "sections"]):
            raise ValueError("Invalid structure")
        print("🤖 Gemini refinement successful.")
        return data
    except Exception as e:
        print("⚠️ Input refinement failed, using original values:", e)
        return {
            "business_name": business_name,
            "website_type": website_type,
            "sections": sections[:4]
        }

# ---------- TEST ----------
if __name__ == "__main__":
    test = refine_website_inputs("applo hospitl", "hospital", ["home", "services", "doctors", "patients"])
    print(json.dumps(test, indent=2))
