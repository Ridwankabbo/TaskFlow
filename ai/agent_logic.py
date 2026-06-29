from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from datetime import datetime
import json

llm = Ollama(model="llama3.1:8b", temperature=0.1)

parser = JsonOutputParser()

prompt_template = ChatPromptTemplate.from_template("""
You are an expert academic assistant. Extract assignment details from the email.

Today is {current_date}.

Email Content:
{email_content}

Return ONLY valid JSON with this exact structure:
{{
  "course": "string",
  "title": "string",
  "deadline": "YYYY-MM-DD HH:MM",   // Use 24-hour format. If relative, calculate actual date.
  "weight_marks": number or null,
  "estimated_hours": number or null,
  "requirements": ["list", "of", "strings"],
  "subtasks": [
    {{"title": "string", "due_offset_days": number}}
  ]
}}

If any field is missing, use null or empty list.
""")

def parse_assignment(email_content: str) -> dict:
    try:
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        chain = prompt_template | llm | parser
        
        result = chain.invoke({
            "email_content": email_content,
            "current_date": current_date
        })
        
        # Basic validation
        if not result.get("deadline"):
            result["deadline"] = None
            
        return result
    except Exception as e:
        print(f"LLM Parsing Error: {e}")
        return None