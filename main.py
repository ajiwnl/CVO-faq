from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Set OpenAI API Key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get the message from the request body
        data = request.get_json()
        message = data.get("message", "")

        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Call OpenAI API
        completion = openai.ChatCompletion.create(
            model="ft:gpt-4o-mini-2024-07-18:personal:furbot:B0QMU8PC",
            messages=[{"role": "user", "content": message}]
        )

        # Extract the response text
        response_message = completion["choices"][0]["message"]["content"]

        # Replace "ChatGPT" and "OpenAI" with "Furbot"
        response_message = response_message.replace("ChatGPT", "Furbot").replace("OpenAI", "Furbot")

        return jsonify({"response": response_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
