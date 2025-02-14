from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Set OpenAI API Key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define a fallback response
FALLBACK_RESPONSE = "I'm not sure, but I can assist you with Microchipping, Rabies, and Responsible Pet Ownership questions"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get the message from the request body
        data = request.get_json()
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Call OpenAI API
        completion = openai.ChatCompletion.create(
            model="ft:gpt-4o-mini-2024-07-18:personal:furbot:B0QMU8PC",
            messages=[{"role": "user", "content": message}]
        )

        # Extract the response text
        response_message = completion["choices"][0]["message"]["content"].strip()

        # Replace "ChatGPT" and "OpenAI" with "Furbot"
        response_message = response_message.replace("ChatGPT", "Furbot").replace("OpenAI", "Furbot")

        # Check if the response is vague or unrelated
        if len(response_message.split()) < 3 or "I don't know" in response_message:
            response_message = FALLBACK_RESPONSE

        return jsonify({"response": response_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
