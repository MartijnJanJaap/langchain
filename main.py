from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain

from load_api_key_from_file import load_api_key_from_file

def main():
    api_key = load_api_key_from_file()
    print(api_key)
    llm = ChatOpenAI(api_key=api_key)

    loader = WebBaseLoader("https://docs.smith.langchain.com/user_guide")
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    vector = FAISS.from_documents(documents, embeddings)

    context_prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
    <context>{context}</context>
    Question: {input}""")

    document_chain = create_stuff_documents_chain(llm, context_prompt)

    question = "how can langsmith help with testing?"
    relevant_docs = vector.similarity_search(question, k=4)

    response = document_chain.invoke({
        "input": question,
        "context": relevant_docs
    })

    print(response)

if __name__ == "__main__":
    main()
