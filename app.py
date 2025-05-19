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
    print("[Claude Bridge] Received data:", data)
    user = data.get("user")
    text = data.get("text")
    channel = data.get("channel")
    if not text or not channel:
        print("[Claude Bridge] Missing text or channel! Data:", data)
        return jsonify({"error": "Missing text or channel"}), 400

    print(f"[Claude Bridge] Sending to Claude: prompt='{text}'")
    claude_response = requests.post(
        CLAUDE_API_URL,
        headers={"Authorization": f"Bearer {CLAUDE_API_KEY}"},
        json={"prompt": text}
    )
    print(f"[Claude Bridge] Claude API status: {claude_response.status_code}, response: {claude_response.text}")
    if claude_response.status_code != 200:
        print("[Claude Bridge] Claude API error:", claude_response.text)
        return jsonify({"error": "Claude API error", "details": claude_response.text}), 500
    claude_reply = claude_response.json().get("completion", "(no response)")

    slack_payload = {
        "channel": channel,
        "text": claude_reply
    }
    print(f"[Claude Bridge] Sending reply to Slack MCP: {slack_payload}")
    mcp_response = requests.post(
        f"{SLACK_MCP_URL}/send-message",
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
        json=slack_payload
    )
    print(f"[Claude Bridge] Slack MCP status: {mcp_response.status_code}, response: {mcp_response.text}")
    if mcp_response.status_code != 200:
        print("[Claude Bridge] Slack MCP error:", mcp_response.text)
        return jsonify({"error": "Slack MCP error", "details": mcp_response.text}), 500

    print("[Claude Bridge] Success! Claude reply sent to Slack.")
    return jsonify({"ok": True, "claude_reply": claude_reply})

@app.route("/")
def index():
    return "Slack-to-Claude MCP Bridge is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
