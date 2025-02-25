from flask import Flask, request, jsonify
import requests
from webhook_handler import handle_webhook

app = Flask(__name__)

SERVICENOW_INSTANCE_URL = "https://your_instance.service-now.com/api/now/table/your_table"
SERVICENOW_USER = "your_username"
SERVICENOW_PASSWORD = "your_password"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400
    
    handle_webhook(data)
    send_to_servicenow(data)
    return jsonify({"status": "success"}), 200

def send_to_servicenow(data):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.post(
        SERVICENOW_INSTANCE_URL,
        auth=(SERVICENOW_USER, SERVICENOW_PASSWORD),
        headers=headers,
        json=data
    )
    if response.status_code != 201:
        print(f"Failed to send data to ServiceNow: {response.status_code}, {response.text}")

@app.route("/")
def index():
    return "<p>Webhook listener is running!</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
