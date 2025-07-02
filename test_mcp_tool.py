import requests

# Set the URL of your FastAPI MCP server
URL = "http://127.0.0.1:8000/call_tool"

# Prepare the payload for the tool call
payload = {
    "name": "run_email_automation_workflow",
    "arguments": {
        "max_emails": 2,      # Change as needed
        "tone": "polite"      # Change as needed ("polite", "formal", etc.)
        # You can also add "schedule_time": "2024-07-01T12:00:00Z" if you want a custom time
    }
}

# Make the POST request
response = requests.post(URL, json=payload)

# Print the result
if response.ok:
    print("Tool call successful!\n")
    print(response.json())
else:
    print("Error calling tool:")
    print(response.status_code, response.text) 