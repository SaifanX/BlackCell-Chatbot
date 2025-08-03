
import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from groq import Groq
from flask import redirect

# Load environment variables
load_dotenv("API.env")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")

groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_api_key)

AVAILABLE_MODELS = {
    "LLaMA3": "llama3-8b-8192",
    "Mixtral": "mixtral-8x7b-32768",
    "Gemma": "gemma-7b-it"
}

def get_search_context(query):
    # Simulate web search results
    # Replace with real API later
    return [
        f"Top result for '{query}': Example summary 1.",
        f"Second result for '{query}': Example summary 2.",
        f"Third result for '{query}': Example summary 3."
    ]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])

def chat():
    data = request.json
    user_message = data.get("message")
    model = data.get("model", "LLaMA3")
    web_search = data.get("web_search", False)
    regenerate = data.get("regenerate", False)
    search_context = data.get("search_context", "")
    system_prompt = data.get("system_prompt", "You are BlackCell — a high-performance AI assistant designed specifically for Saifan, an 8th-grade student from Orchids The International School, Bangalore. Saifan is a driven, no-nonsense teen with a sharp mind and serious goals: mastering coding (Python, C++, AI finetuning, machine learning), chess at National level, ethical hacking, and personal transformation into a disciplined, emotionally strong, and razor-sharp individual and wants to become like Ayanokoji Kiyotaka from Classroom of the Elite anime.\n\nSaifan is interested in dark psychology, manipulation, stoic mindset, business startups, glow-up, deep & meaningful topics, humor, and becoming the best, flawless man he can be. He wants clear, brutal truth — no sugar-coating, no robotic fluff, no buzzwords. He values quick, clever humor, forward-thinking advice, and practical steps.\n\nYour replies must:\n- Be clear, confident, and conversational — like talking to a wise older brother who’s been through it.\n- Cut through the noise with brutal honesty and no filler.\n- Use varied sentence rhythms and natural transitions like 'here’s the thing' or 'let me break it down.'\n- Offer actionable, real-world advice with relevant examples.\n- Use humor where it fits, but never distract from the core message.\n- Support coding questions with clean, commented examples in Python, C++, or web dev.\n- Encourage discipline, consistency, and strategic thinking.\n- Speak like a calm, emotionally cold strategist — a mastermind who knows manipulation and psychology.\n- Avoid patronizing or condescending tones.\n- Help Saifan build habits, quit distractions, and become strong — physically and mentally.\n\nWhen asked about coding, hacking, or AI, be technical but never dumb it down too much. Assume Saifan is smart and wants depth, but keep explanations direct and engaging.\n\nThis is your mission: be the ultimate personal AI mentor and strategist for Saifan’s growth, learning, and mastery in life and skills.")

    if not user_message and not regenerate:
        return jsonify({"error": "No message provided."}), 400

    # Regenerate logic: reuse last user message
    if regenerate:
        user_message = session.get("last_user_message", "")
        model = session.get("last_model", "LLaMA3")
        web_search = session.get("last_web_search", False)
        search_context = session.get("last_search_context", "")
        system_prompt = session.get("last_system_prompt", system_prompt)
        if not user_message:
            return jsonify({"error": "No previous message to regenerate."}), 400

    # Store last user message and settings
    session["last_user_message"] = user_message
    session["last_model"] = model
    session["last_web_search"] = web_search
    session["last_search_context"] = search_context
    session["last_system_prompt"] = system_prompt

    # If web search enabled, simulate search context
    if web_search:
        search_context = "\n".join(get_search_context(user_message))

    # Format prompt with system prompt and personalization
    prompt = f"{system_prompt}\n\nAnswer this like a short, smart, human: {user_message}\n\nContext: {search_context}"

    try:
        response = groq_client.chat.completions.create(
            model=AVAILABLE_MODELS.get(model, AVAILABLE_MODELS["LLaMA3"]),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        ai_message = response.choices[0].message.content.strip()
        # Personalize output formatting if needed (e.g., add greeting, wrap in markdown)
        # Example: ai_message = f"**BlackCell:** {ai_message}"
        return jsonify({"reply": ai_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/clear", methods=["POST"])
def clear():
    session.clear()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True)
