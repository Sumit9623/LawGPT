import os
import streamlit as st
import qdrant_client
from dotenv import load_dotenv
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate,MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain.schema.runnable import RunnableLambda
from htmlTemplates import css, bot_template, user_template
# from langchain.memory import ConversationBufferMemory,VectorStoreRetrieverMemory
# from langchain.chains import ConversationalRetrievalChain
# from langchain_core.runnables import RunnablePassthrough,RunnableParallel
# from langchain.chains import LLMChain


def get_conversation_chain():
    # llm = ChatOpenAI(model_name='gpt-3.5-turbo-0125')
    llm = ChatOpenAI(model_name='gpt-4')
    output_parser = StrOutputParser()
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    client = qdrant_client.QdrantClient(os.getenv("QDRANT_HOST"),api_key=os.getenv("QDRANT_API_KEY"))
    vectorstore = Qdrant(client=client,collection_name=os.getenv("QDRANT_COLLECTION_NAME"),embeddings=embeddings)
    retriver = vectorstore.as_retriever()

    instruction_to_system = """Given a chat history and the latest user question, which may reference context from the chat history, formulate a standalone question that can be understood without the chat history.\
    if quetion is asked about perticular court case then refer the chat history for case name\
    Do not answer the question; simply reformulate it if necessary, otherwise return question as is."""
    question_maker_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", instruction_to_system),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )

    question_chain = question_maker_prompt | llm | output_parser

    def contextualized_question(input: dict):
        if input.get("chat_history"):
            input['question'] = question_chain.invoke(input)
        context = retriver.invoke(input["question"])[0].page_content
        return {"question":input["question"],"context":context}

    dict_chain = RunnableLambda(contextualized_question)

    qa_system_prompt = """You are a chatbot named LawGPT designed for question-answering task\
    below is some context given generate answer based on that \
    if context not given generate answer based on your knowledge and provide disclaimer that information is not from trusted sources.\
    context = {context}"""
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            ("human", "{question}"),
        ]
    )

    rag_chain = (dict_chain | qa_prompt | llm)
    return rag_chain

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def handle_userinput(user_question):
    # last_que = []
    # if(len(st.session_state.chat_history)>0):
    #     last_que = [st.session_state.chat_history[len(st.session_state.chat_history)-1]]
    response = st.session_state.conversation.invoke({'question': user_question,"chat_history":st.session_state.chat_history})
    st.session_state.chat_history.extend([HumanMessage(content=user_question), AIMessage(content=response.content)])
    print(st.session_state.chat_history)
    for i in range(len(st.session_state.chat_history)-1,-1,-2):
        st.write(user_template.replace(
            "{{MSG}}", st.session_state.chat_history[i-1].content), unsafe_allow_html=True)
        st.write(bot_template.replace(
            "{{MSG}}", st.session_state.chat_history[i].content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Law-GPT",layout="centered")
    st.write(css, unsafe_allow_html=True)
    st.markdown('<p style="color:red;"> Disclaimer : The responces generated is through AI models and can have some errors, verify before use.</p>', unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
        st.session_state.conversation = get_conversation_chain()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.title("LawGPT :books:")
    user_question = st.text_area("Ask me about indian court cases:")
    if user_question:
        handle_userinput(user_question)

if __name__ == '__main__':
    main()