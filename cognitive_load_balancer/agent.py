# agent.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

def initialize_agent():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file!")
    
    genai.configure(api_key=api_key)
    # Using gemini-1.5-flash as it is free, fast, and excellent for coding
    return genai.GenerativeModel('gemini-1.5-flash')

def delegate_task(model, task_description):
    print("\n🤖 [AGENT INITIATED] Connecting to Google Gemini API...")
    
    prompt = f"""
    You are an elite, autonomous AI software engineer. 
    Your human developer is currently experiencing High Cognitive Load and is overwhelmed.
    
    Take over and complete the following pending task perfectly:
    {task_description}
    
    Provide ONLY the completed code. Include comments explaining the logic, but no markdown greetings.
    """
    
    response = model.generate_content(prompt)
    return response.text