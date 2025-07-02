from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from mcp.types import Tool, ListToolsResult, CallToolResult, TextContent
from langgraph_flow import run_workflow
from config import EMAIL_IMAP_SERVER, EMAIL_SMTP_SERVER, EMAIL_ADDRESS, EMAIL_PASSWORD
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from tools.schedule_mail import process_due_emails

# --- APScheduler integration for local scheduling ---
def start_mail_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        lambda: process_due_emails(EMAIL_SMTP_SERVER, EMAIL_ADDRESS, EMAIL_PASSWORD),
        'interval',
        minutes=1,
        id='mail_scheduler'
    )
    scheduler.start()
    print("[SCHEDULER] Mail scheduler started (runs every minute)")
# ---------------------------------------------------

app = FastAPI()

EMAIL_WORKFLOW_TOOL = Tool(
    name="run_email_automation_workflow",
    description="Run the complete email automation workflow using LangGraph: Read emails → Categorize → Draft responses → Schedule",
    inputSchema={
        "type": "object",
        "properties": {
            "max_emails": {
                "type": "integer",
                "description": "Maximum number of emails to process (default: 10)",
                "default": 10
            },
            "tone": {
                "type": "string",
                "description": "Tone for email responses (polite, formal, casual, urgent)",
                "default": "polite"
            },
            "schedule_time": {
                "type": "string",
                "description": "When to schedule emails (ISO format, default: 5 minutes from now)",
                "format": "date-time",
                "default": (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)).replace(microsecond=0).isoformat()
            }
        },
        "required": []
    }
)

@app.on_event("startup")
def on_startup():
    start_mail_scheduler()

@app.get("/list_tools")
def list_tools():
    return ListToolsResult(tools=[EMAIL_WORKFLOW_TOOL]).dict()

class CallToolRequest(BaseModel):
    name: str
    arguments: Dict[str, Any]

@app.post("/call_tool")
async def call_tool(req: CallToolRequest):
    if req.name == "run_email_automation_workflow":
        try:
            max_emails = req.arguments.get("max_emails", 10)
            tone = req.arguments.get("tone", "polite")
            schedule_time = req.arguments.get("schedule_time")
            # Debug prints for config values
            print("IMAP:", EMAIL_IMAP_SERVER)
            print("SMTP:", EMAIL_SMTP_SERVER)
            print("EMAIL:", EMAIL_ADDRESS)
            print("PASSWORD:", EMAIL_PASSWORD)
            result = await run_workflow(
                imap_server=EMAIL_IMAP_SERVER,
                smtp_server=EMAIL_SMTP_SERVER,
                email=EMAIL_ADDRESS,
                password=EMAIL_PASSWORD,
                send_time=schedule_time,
                tone=tone,
                max_emails=max_emails
            )
            result_text = "📧 Email Automation Workflow Results\n"
            result_text += "=" * 50 + "\n\n"
            for email in result:
                result_text += f"📨 From: {email.get('from', 'Unknown')}\n"
                result_text += f"📝 Subject: {email.get('subject', 'No subject')}\n"
                result_text += f"🏷️  Category: {email.get('category', 'unknown')}\n"
                result_text += f"📅 Scheduled: {email.get('scheduled', False)}\n"
                result_text += f"✍️  Draft: {email.get('draft', 'No draft')[:200]}...\n"
                result_text += "-" * 50 + "\n\n"
            return CallToolResult(
                content=[TextContent(type="text", text=result_text)]
            ).dict()
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"❌ Workflow Error: {str(e)}")]
            ).dict()
    else:
        return CallToolResult(
            content=[TextContent(type="text", text=f"❌ Unknown tool: {req.name}")]
        ).dict() 