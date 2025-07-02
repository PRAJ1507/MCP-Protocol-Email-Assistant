import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_IMAP_SERVER = os.getenv('EMAIL_IMAP_SERVER')
EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
OAUTH_CLIENT_ID = os.getenv('OAUTH_CLIENT_ID')
OAUTH_CLIENT_SECRET = os.getenv('OAUTH_CLIENT_SECRET')
OAUTH_REDIRECT_URI = os.getenv('OAUTH_REDIRECT_URI')

# MCP Server Configuration
MCP_SERVER_HOST = os.getenv('MCP_SERVER_HOST', '127.0.0.1')  # Changed to localhost
MCP_SERVER_PORT = int(os.getenv('MCP_SERVER_PORT', 8000))

# Development mode - set to True to skip API key authentication
DEV_MODE = os.getenv('DEV_MODE', 'True').lower() == 'true' 