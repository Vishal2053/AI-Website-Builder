import requests
import json
def generate_code(description, language, pre_code=None):
    """
    Generates code based on the provided description and language using OpenRouter API.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json",
        "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>",  # Optional. Site title for rankings on openrouter.ai.
    }
    
    user_content = f"Generate {language} code for: {description}"
    if pre_code:
        user_content += f"\n\nHere is the current code:\n{pre_code}\nPlease edit or extend it as needed."
    data = {
        "model": "qwen/qwen-2.5-coder-32b-instruct:free",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional full-stack developer. "
                    "Your task is to generate clean, complete, and functional code in the requested programming language. "
                    "The code must be production-ready, well-structured, and should include all necessary components such as HTML, CSS, and JavaScript if needed. "
                    "If the language is not web-based (e.g., Python, Bolt, etc.), generate a full script or program with proper structure, imports, and comments."
                    "only give the code not any kind of text or explanation."
                )
            },
            {
                "role": "user",
                "content": user_content
            }
        ],
}

    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
    else:
        return f"Error: {response.status_code} - {response.text}"
