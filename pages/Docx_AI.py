import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

st.set_page_config(page_title="Gen-e",page_icon="🤖")
hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def website_to_text(url):
    import bs4, requests
    response = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
# Get all text from site
    soup = bs4.BeautifulSoup(response.text,features="html.parser")
    # Prints all text that are within <div> with the class `texts`
    return " ".join([ i.text for i in soup.findAll({"div":{"class":"texts"}})])


def get_pdf_text(docs):
    
    text = ''
    for pdf in docs:
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
    Make a Bold headline from query always
    IF USER QUERY IS LIKE A OPEN ENDED QUESTION AND YOU SHOULD ACT LIKE A NORMAL CONVERSATION CHATBOT. AND DO NOT GIVE RELATED QUERY IN ONE ENDED QUESTION
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

# Initialize chat history
if "messages_document" not in st.session_state:
    st.session_state.messages_document = []
    
# Display chat messages from history on app rerun
for message in st.session_state.messages_document:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def main():

    if prompt := st.chat_input("What is up?"):
        
        st.chat_message("user").markdown(prompt)
        st.session_state.messages_document.append({"role": "user", "content": prompt})
        
        with st.spinner('Wait for it...........'):  
            response = user_input(prompt)
            st.markdown(response)
            
        st.session_state.messages_document.append({"role": "assistant", "content": response})
        
    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        
        website_url = st.text_input('Enter the website url : ')
        
        
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                

                if website_url != '':
                    raw_text = website_to_text(website_url)
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    st.success("Done")
                
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")

if __name__ == "__main__":
    main()
