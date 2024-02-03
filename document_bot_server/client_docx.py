import base64
import json
import requests

api = 'https://b80d-103-196-28-194.ngrok-free.app/document_api'
pdf_path = r"D:\Downloads\React Native SDK - Quick Start _ HyperVerge.pdf"

# Read the PDF file as bytes
with open(pdf_path, "rb") as pdf_file:
    pdf_binary = pdf_file.read()

# Encode the PDF binary data as base64
pdf_base64 = base64.b64encode(pdf_binary).decode("utf-8")

# Prepare the payload as JSON
payload = {
    'question': 'React Native',
    'documents': [pdf_base64],
    'other_key': 'value'
}

# Set the headers to indicate JSON content
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

# Make a POST request with JSON payload
response = requests.post(api, data=json.dumps(payload), headers=headers)

try:
    data = response.text
    print(data)
except requests.exceptions.RequestException as e:
    print(str(e))
