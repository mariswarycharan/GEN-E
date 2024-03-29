from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os,base64
from io import BytesIO
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import textract

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_pdf_text(docs):
    
    text = ''
    for pdf in docs:
        pdf = base64.b64decode(pdf)
        pdf =  BytesIO(pdf)
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
            
    # file_path = 'documents/' + docs[0].name
    # with open(file_path, "wb") as f:
    #     f.write(docs[0].read())
    # text = textract.process(file_path).decode('latin-1')
    
    return  text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():

    prompt_template = """ you should also act like a natural bot to answer open ended questions and during open ended question don't include uploaded context information  
    response should be professinally and be gentle don't use offensive language 
    use points structure in response
    You should only generate response from uploaded files  
    IF USER QUERY IS LIKE A OPEN ENDED QUESTION AND YOU SHOULD ACT LIKE A NORMAL CONVERSATION CHATBOT.
    Make a Bold headline from query always
    you should also give relevant source links always 
    lastly add relevent queries to the input query and uploaded document as "Relevant Queries"
    you should remember all context what users given and Answer the question as in natural language \n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    
    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()
    
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    return response["output_text"]



def main(prompt,docx_list):
    
    pdf_docs =  docx_list
    raw_text = get_pdf_text(pdf_docs)
    text_chunks = get_text_chunks(raw_text)
    get_vector_store(text_chunks)
      
    response = user_input(prompt)
    
    return response
    

# # Assuming pdf_base64 contains the file path to the PDF
# pdf_path = r"D:\Downloads\React Native SDK - Quick Start _ HyperVerge.pdf"


# # Read the PDF file as bytes
# with open(pdf_path, "rb") as pdf_file:
#     pdf_binary = pdf_file.read()
    
    
# l = [pdf_binary] 
# pdf_base64 = base64.b64decode(l[0])  
# print(BytesIO(pdf_base64))


# r = main(prompt='React Native',docx_list=l)
# print(r)