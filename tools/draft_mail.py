from typing import Dict
from langchain_ollama.llms import OllamaLLM
import asyncio
import re

# Initialize Ollama LLM (assumes Ollama is running locally)
llm = OllamaLLM(model="llama3.2")  # You can change the model name if needed

def extract_sender_name(sender: str) -> str:
    """
    Extracts the sender's name from the email address.
    Examples:
    - "John Doe <john@example.com>" -> "John"
    - "john@example.com" -> "John"
    - "John Doe" -> "John"
    """
    if not sender:
        return "Sender"
    
    # Remove email address if present
    sender_clean = re.sub(r'<[^>]+>', '', sender).strip()
    
    # If it's just an email address, extract the name part
    if '@' in sender_clean and ' ' not in sender_clean:
        name_part = sender_clean.split('@')[0]
        # Capitalize first letter
        return name_part.capitalize()
    
    # If it's a full name, take the first name
    if ' ' in sender_clean:
        first_name = sender_clean.split(' ')[0]
        return first_name
    
    # If it's a single word, use it as is
    return sender_clean

async def draft_email_response(email: Dict, tone: str = "polite") -> str:
    """
    Drafts a response to the given email using Ollama LLM, with optional tone adjustment.
    Returns the draft email body as a string.
    """
    sender = email.get('from', 'Sender')
    subject = email.get('subject', 'your email')
    snippet = email.get('snippet', '')
    
    # Extract the sender's name
    sender_name = extract_sender_name(sender)
    
    prompt = (
        f"Draft a {tone} reply to the following email. Use the sender's actual name '{sender_name}' in the greeting instead of generic placeholders like [Your Name] or [Sender's Name].\n"
        f"From: {sender}\n"
        f"Subject: {subject}\n"
        f"Body: {snippet}\n"
        f"Important: Start the reply with 'Dear {sender_name},' and end with 'Best regards,' followed by 'Sridhar Prajwal' (not [Your Name])."
    )
    try:
        # OllamaLLM is synchronous, so run in a thread executor for async compatibility
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: llm.invoke(prompt))
        return response
    except Exception as e:
        return f"[LLM Error: {e}]"
    # TODO: Integrate LangChain/LLM for smarter, context-aware drafting 