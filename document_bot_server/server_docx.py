import io
import json ,os                   
import base64                  
import logging  
from pyngrok import ngrok, conf           
import numpy as np
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
from upload_docx_source_code import main
from flask import Flask, request, jsonify, abort

app = Flask(__name__)          
app.logger.setLevel(logging.DEBUG)
  
port = 5000
public_url = ngrok.connect(port).public_url
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

print("public_url ================ > " , public_url)


# Update any base URLs to use the public ngrok URL
app.config["BASE_URL"] = public_url


@app.route("/document_api", methods=['POST'])
def test_method():   
    global model  
        
    
    if not request.json or 'documents' not in request.json: 
        abort(400)
             
    # get the base64 encoded string
    document_list = request.json["documents"]
    query = request.json["question"]
    
    response = main(prompt=query,docx_list=document_list)
    
    print(query)
    print(response)
    
    return response
  
  

  
if __name__ == "__main__":     
    app.run()