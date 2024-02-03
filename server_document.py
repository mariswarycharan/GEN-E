import io
import json ,os                   
import base64   
from pyngrok import ngrok, conf                  
import logging             
import numpy as np
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, request, jsonify, abort

app = Flask(__name__)          
app.logger.setLevel(logging.DEBUG)
  
port = 5000
public_url = ngrok.connect(port).public_url
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

print("public_url ================ > " , public_url)

app.config["BASE_URL"] = public_url


# Load environment variables from the .env file
load_dotenv()
# Access the environment variable
api_key = os.getenv("OPENAI_API_KEY")  

model = genai.GenerativeModel('gemini-pro-vision')
  
@app.route("/test", methods=['POST'])
def test_method():   
    global model  
        
    genai.configure(api_key=api_key)
         
    if not request.json or 'image' not in request.json: 
        abort(400)
             
    # get the base64 encoded string
    im_b64 = request.json['image']
    query = request.json['question']
    
    # convert it into bytes  
    img_bytes = base64.b64decode(im_b64.encode('utf-8'))

    # convert bytes data to PIL Image object
    img = Image.open(io.BytesIO(img_bytes))

    response = model.generate_content([query, img])
    response = response.text
    print(response)
    result_dict = {'output': response}
    return result_dict['output']
  

  
if __name__ == "__main__":     
    app.run()