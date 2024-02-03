import requests
import base64
import json
def send_request(pdf_base64, user_question):
    api_url = "http://127.0.0.1:5000/"  # Update with your API URL

    data = {
        "pdf_base64": pdf_base64,
        "user_question": user_question
    }

    # data =  json.dumps(data)
    
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, json=data,headers=headers)

    print(response)
    
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Example usage:
with open(r"D:\Downloads\events.pdf", "rb") as pdf_file:
    pdf_base64 = base64.b64encode(pdf_file.read()).decode("utf-8")


user_question = "hi hello"
result = send_request(pdf_base64, user_question)

print(result)
