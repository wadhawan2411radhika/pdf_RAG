# groq_client.py
import os
from groq import Groq  
from dotenv import load_dotenv

load_dotenv()
class LlamaClient:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

    def generate_analysis(self, context: str) -> str:
        prompt = (
            "You are a financial advisor. Your task is to provide a strength analysis for the given organisation: Commonwealth Bank of Australia. "
            f"You are given the following report to perform analysis. Leverage this. "
            f"Report: {context} "
            "Your Analysis: "
        )

        response = self.client.chat.completions.create(
            model="llama3-8b-8192",  # Use the appropriate Llama 3 model name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.1
        )

        # Return the generated response
        return response.choices[0].message.content
