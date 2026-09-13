# Generate app.py file
app_code = '''import streamlit as st
import json
import re
from groq import Groq

# ---------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Scam & Fraud Message Detector",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI Scam & Fraud Message Detector")
st.markdown("Analyze SMS, WhatsApp, Emails, and Messages in real-time to detect scams, phishing attempts, and fraudulent intent.")

# ---------------------------------------------------------
# SIDEBAR: API KEY MANAGEMENT
# ---------------------------------------------------------
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

st.sidebar.markdown("""
### 🔑 How to get a free API Key?
1. Go to [console.groq.com](https://console.groq.com)
2. Create a free account.
3. Generate an API Key under **API Keys**.
4. Paste it above!
""")

# ---------------------------------------------------------
# CORE ANALYSIS FUNCTION
# ---------------------------------------------------------
def analyze_message(message_text, message_type, api_key):
    """
    Sends the message to the Groq API and requests a structured JSON analysis.
    """
    client = Groq(api_key=api_key)
    
    prompt = f"""
    You are an expert AI Cybersecurity Analyst specializing in detecting scams, phishing, and fraudulent messages.
    Analyze the following {message_type} message carefully:

    ---
    MESSAGE CONTENT:
    "{message_text}"
    ---

    Respond ONLY with a valid JSON object in the exact format below (no markdown wrappers, no introductory or concluding text):

    {{
      "is_scam": true or false,
      "risk_level": "Low", "Medium", "High", or "Critical",
      "scam_type": "Type of Scam (e.g., Phishing, Impersonation, Lottery Scam, Urgency/OTP Scam, Legitimate, etc.)",
      "risk_score": 85 (a number from 0 to 100),
      "caption": "A 1-line catchy warning or status headline summary",
      "red_flags": [
        "First specific suspicious indicator found in text",
        "Second suspicious indicator found in text"
      ],
      "safety_advice": [
        "Specific actionable advice 1",
        "Specific actionable advice 2"
      ],
      "detailed_explanation": "A concise paragraph explaining why this message was categorized as such."
    }}
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    raw_content = response.choices[0].message.content.strip()
    
    # Strip markdown code fence blocks if returned by the LLM
    cleaned_content = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_content, flags=re.MULTILINE).strip()
    
    return json.loads(cleaned_content)

# ---------------------------------------------------------
# MAIN INTERFACE
# ---------------------------------------------------------
st.subheader("📥 Input Message Details")

col1, col2 = st.columns([1, 3])

with col1:
    msg_type = st.selectbox(
        "Select Platform / Format:",
        ["SMS", "WhatsApp", "Email", "Social Media / Other"]
    )

with col2:
    msg_input = st.text_area(
        "Paste the message content below:",
        height=150,
        placeholder="e.g., Dear user, your account has been suspended. Click here immediately to verify: http://bit.ly/fake-link"
    )

analyze_btn = st.button("🚨 Analyze Message for Scam", use_container_width=True)

# ---------------------------------------------------------
# RESPONSE DISPLAY LOGIC
# ---------------------------------------------------------
if analyze_btn:
    if not api_key:
        st.error("⚠️ Please enter your Groq API Key in the sidebar to proceed.")
    elif not msg_input.strip():
        st.warning("⚠️ Please paste a message to analyze.")
    else:
        with st.spinner("🔍 Analyzing message patterns, urgency, and URLs..."):
            try:
                result = analyze_message(msg_input, msg_type, api_key)
                
                st.markdown("---")
                st.subheader("📊 Complete Detection Report")
                
                # Top Headline / Caption
                caption = result.get("caption", "Analysis Complete")
                is_scam = result.get("is_scam", False)
                
                if is_scam:
                    st.error(f"🚨 **CAPTION:** {caption}")
                else:
                    st.success(f"✅ **CAPTION:** {caption}")
                
                # Metrics Row
                m1, m2, m3 = st.columns(3)
                
                m1.metric("Status", "SCAM DETECTED" if is_scam else "LEGITIMATE / SAFE")
                
                risk_lvl = result.get("risk_level", "Unknown")
                m2.metric("Risk Level", risk_lvl)
                
                risk_score = result.get("risk_score", 0)
                m3.metric("Scam Probability", f"{risk_score}%")
                
                # Scam Type
                st.info(f"🏷️ **Detected Scam Category:** {result.get('scam_type', 'N/A')}")
                
                # Detailed Explanation
                st.markdown("### 📝 Detailed Analysis")
                st.write(result.get("detailed_explanation", ""))
                
                # Red Flags & Safety Advice
                c_red, c_green = st.columns(2)
                
                with c_red:
                    st.markdown("### 🚩 Red Flags Detected")
                    flags = result.get("red_flags", [])
                    if flags:
                        for flag in flags:
                            st.markdown(f"- ⚠️ {flag}")
                    else:
                        st.write("No obvious suspicious red flags detected.")
                        
                with c_green:
                    st.markdown("### 🛡️ Relevant Safety Advice")
                    advice_list = result.get("safety_advice", [])
                    if advice_list:
                        for item in advice_list:
                            st.markdown(f"- 💡 {item}")
                    else:
                        st.write("Standard security practices apply.")
                        
            except json.JSONDecodeError:
                st.error("Failed to parse AI model response into structured JSON. Please try again.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
'''

with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

# Generate requirements.txt file
req_code = """streamlit>=1.30.0
groq>=0.4.0
"""

with open("requirements.txt", "w", encoding="utf-8") as f:
    f.write(req_code)

print("Files generated successfully!")