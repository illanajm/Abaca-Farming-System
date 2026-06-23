import ollama


def generate_ai_recommendation(data):

    prompt = f"""
You are an agricultural expert.

Analyze this abaca farming data:

{data}


Provide:

1. Interpretation
2. Possible causes
3. Recommendations

Use professional agricultural language.
"""


    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )


    return response["message"]["content"]