# import os
# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# # Initialize OpenAI Client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def analyze_assignment(text: str):
#     prompt = f"""
#     You are an academic assistant. Analyze the following student assignment.
#     Provide the response in the following format:
    
#     SUMMARY: (A brief summary)
#     PLAGIARISM_CHECK: (Analysis of style and potential AI/copy-paste patterns)
#     IMPROVEMENTS: (Constructive feedback)

#     Assignment Text:
#     {text}
#     """
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "You are a helpful academic assistant."},
#                 {"role": "user", "content": prompt}
#             ]
#         )
        
#         # Extract the text content from the response
#         analysis_text = response.choices[0].message.content
#         return {"success": True, "analysis": analysis_text}
        
#     except Exception as e:
#         print(f"OPENAI DEBUG ERROR: {e}")
#         return {"success": False, "error": str(e)}

import time
import random

def analyze_assignment(text: str):
    time.sleep(1.5) 
    
    # Generate a random but realistic plagiarism score
    mock_score = round(random.uniform(0.5, 15.0), 2)
    
    mock_response = (
        "SUMMARY: Analyzed the provided text regarding urban industrialization. "
        "PLAGIARISM_CHECK: Writing style appears authentic with minor common phrasing. "
        "IMPROVEMENTS: Try to expand on the environmental impacts of the 19th-century expansion."
    )
    
    return {
        "success": True, 
        "analysis": mock_response,
        "score": mock_score # New field!
    }