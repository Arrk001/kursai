import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

from rich import print

load_dotenv()
token = os.getenv("GH_API_TOKEN")
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

# Complaint letter recogniser
# is_complaint: boolean which would tell if a letter was complainatory 
# is_refund_request: boolean which would tell if a letter was an inquiry for refund
# positive_score: a float from 0 to 1 telling how positive the letter was.
# complaint_tags: string, one or few of the following: "not satisfied", "very disappointed", "complain", "unacceptable","issue", "problem", "angry", "bad experience", "frustrated", "refund", "faulty", "poor service", "doesn't work", "worst"

complaint_keywords = [
        "not satisfied", "very disappointed", "complain", "unacceptable",
        "issue", "problem", "angry", "bad experience", "frustrated", "refund",
        "faulty", "poor service", "doesn't work", "worst"]
complaint_keywords_with_quotes = [f"\"{keyword}\"" for keyword in complaint_keywords]
complaint_keywords_list_str = ", ".join(complaint_keywords_with_quotes)

complaint_letter = """Dear Customer Service,
I am writing to express my dissatisfaction with the recent purchase I made from your store.
The product arrived damaged and did not match the description provided on your website. 
I expected a much higher quality based on the price I paid. I would like a full refund and an apology for the inconvenience caused.
Thank you for your attention to this matter.
Sincerely, Jonas"""

loving_product_letter = """Dear Customer Service,
The product was shipped fast (in four days). Product was easy to use, it's quality was the best!
Thank you for your service!

Sincerely, Jonė
"""


class LetterInformation(BaseModel): 
    """This is a class for analyzing letter content.
    
    This class represents information about a letter, specifically focusing on wheter it is a complant,
    and what type of complaint letter it is. 
    It ingerits from BaseModel to handle data validation and serialization.

    Attributes:
        is_complaint (bool): Indicates whether the letter is classified as a complaint letter.
        is_refund_request (bool): Indicates whether the letter is classified as a refund inquiry.
        positive_score (float): float from 0 to 1 telling how positive the letter was.
        complaint_tags (list[str]): list of strings, which are one or more of the following: "not satisfied", "very disappointed", "complain", "unacceptable","issue", "problem", "angry", "bad experience", "frustrated", "refund", "faulty", "poor service", "doesn't work", "worst" 
    """
    is_complaint: bool
    is_refund_request: bool
    positive_score: float
    complaint_tags: list[str]


system_prompt = f"""You are a helpful assistant that classifies customer letters.
            Analyze the following message and respond in **valid JSON**
            Complaint tags should be a list of strings, where strings can be the following: {complaint_keywords_list_str}
            """

print("[green]This is a system prompt:[/green]")
print(f"[yellow]{system_prompt}[/yellow]")

response = client.beta.chat.completions.parse(
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": f"""Letter:
            \"{loving_product_letter}\""""
        }
    ],
    model=model,
    response_format=LetterInformation
)

parsed_result = response.choices[0].message.parsed

print(parsed_result)