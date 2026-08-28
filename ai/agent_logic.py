from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from datetime import datetime
import json
import re

llm = OllamaLLM(model="deepseek-r1:1.5b", temperature=0.1)

parser = JsonOutputParser()

prompt_template = ChatPromptTemplate.from_template("""
You are an expert academic assistant. Extract assignment details from the email.

Today is {current_date}.

Email Content:
{email_content}

STRICT RULES:
- Return ONLY pure JSON. No thinking, no explanation, no <think> tags, no markdown.
- If any information is missing, use null or empty list [].
- Deadline must be in format: YYYY-MM-DD HH:MM

Return exactly this JSON structure:
{{
  "course": "string or null",
  "title": "string or null",
  "deadline": "YYYY-MM-DD HH:MM or null",
  "weight_marks": number or null,
  "estimated_hours": number or null,
  "requirements": ["list of strings"],
  "subtasks": [
    {{"title": "string", "due_offset_days": number}}
  ]
}}
""")

def extract_json_from_text(text: str) -> dict | None:
    # Remove <think> tags and their content
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    
    # Find JSON-like content between curly braces
    match = re.search(r'\{[\s\S]*\}', text)
    
    if match:
        try:
            return json.loads(match.group())  # Fixed: json.loads() not json.load()
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return None
    return None

def parse_assignment(email_content: str) -> dict:
    try:
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Create the chain without parser
        chain = prompt_template | llm
        
        # Get raw response
        raw_response = chain.invoke({
            "email_content": email_content,
            "current_date": current_date
        })
        
        print(f"Raw response length: {len(raw_response)}")  # Debug
        
        # Extract JSON manually
        result = extract_json_from_text(raw_response)
        
        if result:
            print("Successfully parsed JSON")
            return result
        else:
            print("Failed to extract valid JSON")
            print("Raw response preview:", raw_response[:500])  # Show first 500 chars
            return None
        
    except Exception as e:
        print(f"LLM Parsing Error: {e}")
        return None