from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os
from tqdm import tqdm


print('carregando')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(BASE_DIR, "./pdf/teste.pdf")

loader = PyPDFLoader(pdf_path)

doc = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(doc)

print(f"Documento dividido em {len(chunks)} blocos de texto.")


print("Gerando embeddings e criando a base vetorial...")

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)
batch_size = 100

for i in tqdm(range(0,len(chunks), batch_size), desc='lotes'):
    batch = chunks[i : i  + batch_size]
    vectorstore.add_documents(documents=batch)

print("Base vetorial criada com sucesso!")

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

llm = ChatOllama(model="llama3", temperature=2)

prompt_template = """
Você é um assistente especializado. Responda à pergunta do usuário utilizando APENAS o contexto fornecido abaixo.
Se você não souber a resposta com base no contexto, responda apenas "Não encontrei essa informação no documento."

Contexto:
{context}

Pergunta:
{question}

Resposta:
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


if __name__ == "__main__":
    pergunta = input('Pergunta: ')
    print(f"\nPergunta: {pergunta}\n")
    
    resposta = rag_chain.invoke(pergunta)
    print(f"Resposta:\n{resposta}")