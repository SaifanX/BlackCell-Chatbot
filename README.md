# BlackCell-ChatBot

A high-performance AI chatbot designed for Saifan, an ambitious student from Orchids The International School, Bangalore. Built with Flask, Groq API, and a modern interactive frontend.

## Features
- ChatGPT-style UI with TailwindCSS
- Model switcher, dark mode, web search simulation
- Brutally honest, strategic, and technical responses
- Personalized for Saifan's goals and interests

## Setup
1. Clone the repo:
   ```
   git clone https://github.com/SaifanX/BlackCell-ChatBot.git
   cd blackcell-chatbot-saifan
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create an `API.env` file (not included in repo):
   ```
   YOUR_API_KEY=your_api_key_here
   ```
4. Run the app:
   ```
   python app.py
   ```
5. Open `http://127.0.0.1:5000` in your browser.

## Security
- **Never share your API.env file or API key.**
- API.env is excluded from git via `.gitignore`.
- Set your API key securely in your deployment platform.

## Personalization
- Edit the system prompt in `app.py` for custom behavior.
- Change UI colors, logo, and text in `templates/index.html`.
- Add more features or settings as you wish!

---
Made for Saifan by BlackCell AI.
