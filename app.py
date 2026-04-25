from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

NOTION_TOKEN = "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"
DATABASE_ID = "34d2cc4fd597807995b1ebcbe76597b2"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_to_notion():
    data = request.json
    
    url = "https://api.notion.com/v1/pages"
    
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # Formatting the data exactly how Notion's API expects it
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": data['name']}}]},
            "Email": {"email": data['email']},
            "Target Track": {"rich_text": [{"text": {"content": data['track']}}]}
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # If Notion accepts it, send a success message back to the webpage
        if response.status_code == 200:
            return jsonify({"status": "success", "message": "Lead captured successfully!"}), 200
        else:
            # If Notion rejects it (e.g., bad API key), send an error
            return jsonify({"status": "error", "message": "Failed to connect to the database."}), 400
            
    except Exception as e:
        return jsonify({"status": "error", "message": "Server error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)