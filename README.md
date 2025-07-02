# Email MCP Assistant

A **LangGraph + MCP hybrid** email automation assistant that combines the power of LangGraph workflow orchestration with the Model Context Protocol (MCP) for seamless AI integration.

## 🏗️ Architecture

This project implements a **hybrid architecture**:

- **LangGraph**: Orchestrates the email workflow as a graph (read → categorize → draft → schedule)
- **MCP**: Exposes the complete LangGraph workflow as a single tool that can be called by MCP clients
- **Hybrid**: Combines both for powerful, protocol-based email automation

## 🔧 Features

- **LangGraph Workflow**: Automated email processing pipeline
  - Read inbox emails from Gmail
  - Categorize emails by priority using AI (Ollama LLM)
  - Draft personalized responses using AI
  - Schedule emails for later sending
- **MCP Integration**: Single tool exposure for AI assistants
  - Complete workflow as one MCP tool
  - Configurable parameters (max emails, tone, schedule time)
  - Protocol-based integration
- **Local AI**: Uses Ollama for privacy and performance
- **Smart Name Extraction**: Automatically extracts sender names for personalized responses

## 🚀 Quick Start

1. **Install [uv](https://github.com/astral-sh/uv) (ultra-fast Python package manager):**
   ```bash
   pip install uv
   ```

2. **Install dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Configure environment** (create `.env` file):
   ```env
   EMAIL_IMAP_SERVER=imap.gmail.com
   EMAIL_SMTP_SERVER=smtp.gmail.com
   EMAIL_ADDRESS=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   ```

4. **Start Ollama** (for local LLM):
   ```bash
   ollama serve
   ollama pull llama3.2
   ```

5. **Test the workflow:**
   ```bash
   uv run main.py
   ```

6. **Start FastAPI MCP server:**
   ```bash
   uv run uvicorn mcp_server:app --reload
   ```

## 🧪 Testing

Test the LangGraph + MCP hybrid:
```bash
uv run test_mcp_tool.py
```

## 📋 MCP Tool

The MCP server exposes one comprehensive tool:

**`run_email_automation_workflow`**
- **Description**: Run the complete email automation workflow using LangGraph
- **Parameters**:
  - `max_emails`: Number of emails to process (default: 10)
  - `tone`: Response tone (polite, formal, casual, urgent)
  - `schedule_time`: When to schedule emails (ISO format)

## 🔄 Workflow Steps

1. **Read Emails**: Connect to Gmail and fetch latest emails
2. **Categorize**: AI-powered email classification (urgent, spam, normal, etc.)
3. **Draft Responses**: Generate personalized replies using sender names
4. **Schedule**: Queue emails for later sending

## 🛡️ Security

- Environment-based configuration
- App password authentication
- Local LLM processing (no data sent to external APIs)
- Secure credential management

## 📚 Example Workflows

See `example_workflows.md` for sample email automation flows.

## 🔗 Integration

This MCP server can be integrated with any MCP-compatible AI assistant, providing powerful email automation capabilities through a single tool call. 