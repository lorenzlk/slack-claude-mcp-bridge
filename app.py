import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

SLACK_MCP_URL = os.getenv("SLACK_MCP_URL")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = os.getenv("CLAUDE_API_URL", "https://api.claude.ai/v1/message")

app = Flask(__name__)

@app.route("/mcp/slack", methods=["POST"])
def slack_mcp_webhook():
    data = request.json
    # Example: Expecting {"user": "U123", "text": "Hello", "channel": "C123"}
    user = data.get("user")
    text = data.get("text")
    channel = data.get("channel")
    if not text or not channel:
        return jsonify({"error": "Missing text or channel"}), 400

    # Send message to Claude
    claude_response = requests.post(
        CLAUDE_API_URL,
        headers={"Authorization": f"Bearer {CLAUDE_API_KEY}"},
        json={"prompt": text}
    )
    if claude_response.status_code != 200:
        return jsonify({"error": "Claude API error", "details": claude_response.text}), 500
    claude_reply = claude_response.json().get("completion", "(no response)")

    # Send response back to Slack via MCP server
    slack_payload = {
        "channel": channel,
        "text": claude_reply
    }
    mcp_response = requests.post(
        f"{SLACK_MCP_URL}/send-message",
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
        json=slack_payload
    )
    if mcp_response.status_code != 200:
        return jsonify({"error": "Slack MCP error", "details": mcp_response.text}), 500

    return jsonify({"ok": True, "claude_reply": claude_reply})

@app.route("/")
def index():
    return "Slack-to-Claude MCP Bridge is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
