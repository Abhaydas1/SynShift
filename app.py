from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__, static_folder="static", template_folder="templates")

API_KEY = "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"  # 🔐 Replace with your actual key
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "anthropic/claude-sonnet-4"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "Code Translator"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    print("Received request:", data)  # Debug line

    input_lang = data["input_lang"]
    output_lang = data["output_lang"]
    code = data["code"]

    system_prompt = (
        f"You are a programming expert. Translate this code from {input_lang} to {output_lang}. "
        f"Return only the code without explanation, and without mentioning the programming language in the output."
    )
    user_prompt = f"```{input_lang.lower()}\n{code}\n```"

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 1024
    }

    try:
        print("Sending request to OpenRouter...")
        res = requests.post(API_URL, headers=HEADERS, json=payload)
        print("Response status:", res.status_code)
        print("Response body:", res.text)

        res.raise_for_status()
        result = res.json()["choices"][0]["message"]["content"]
        return jsonify({"result": result})
    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)
