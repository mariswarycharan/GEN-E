
itemurl = "https://betterprogramming.pub/speed-up-llm-inference-83653aa24c47"

def website_to_text(url):
    import bs4, requests
    response = requests.get(itemurl,headers={'User-Agent': 'Mozilla/5.0'})
    print(response.text) # Get all text from site
    soup = bs4.BeautifulSoup(response.text,features="html.parser")
    # Prints all text that are within <div> with the class `texts`
    return " ".join([ i.text for i in soup.findAll({"div":{"class":"texts"}})])

# r = website_to_text(itemurl)
# print(r)

   
import shutil 
import os 
   

# path 
path = 'hello.mp3'
   
# removing directory 
os.remove(path) 