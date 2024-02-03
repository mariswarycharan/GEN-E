import base64
import json                    
import requests

api = 'https://8ab7-103-196-28-194.ngrok-free.app/test'
image_file = r'C:\Users\Charan A A\Pictures\IMG_20230928_080525.jpg'

with open(image_file, "rb") as f:
    im_bytes = f.read()        
im_b64 = base64.b64encode(im_bytes).decode("utf8")

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
  
payload = json.dumps({ 'question' : 'describe it' , "image": im_b64, "other_key": "value"})
response = requests.post(api, data=payload, headers=headers)
try:
    data = response.json()     
    print(data)                
except requests.exceptions.RequestException:
    print(response.text)
    