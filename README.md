# Slack-to-Claude MCP Bridge

This project bridges Slack messages to Claude using a Slack MCP server and deploys easily on Railway.

## Features
- Listens for Slack messages via MCP
- Forwards messages to Claude (API/endpoint)
- Sends Claude's responses back to Slack

## Quick Start (Railway)

1. **Clone this repo & push to GitHub**
2. **Create a Railway project** and connect your GitHub repo
3. **Set these environment variables in Railway:**
   - `SLACK_MCP_URL`: URL of your Slack MCP server
   - `SLACK_BOT_TOKEN`: Your Slack bot token
   - `CLAUDE_API_KEY`: Your Claude API key
   - `CLAUDE_API_URL`: (Optional) Claude API endpoint
4. **Deploy!**

## Local Development
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Files
- `app.py`: Main bridge logic
- `requirements.txt`: Dependencies
- `.env.example`: Example config for secrets

---

**Note:** You need access to a Slack MCP server and Claude API.
