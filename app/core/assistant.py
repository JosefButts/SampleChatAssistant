from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from typing import Dict, List

class AIAssistant:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-4-turbo-preview",
            api_key=api_key
        )
        self.embeddings = OpenAIEmbeddings(api_key=api_key)
        self.vector_store = None
        self.qa_chain = None
        self.agent = None

    def initialize_knowledge_base(self, documents: List[Document]):
        """Initialize the vector store with documentation"""
        self.vector_store = Chroma.from_documents(
            documents,
            self.embeddings
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever()
        )

    def initialize_agent(self, tools: List[Tool]):
        """Initialize the agent with tools"""
        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    async def get_response(self, query: str) -> Dict:
        """
        Get response from the assistant
        Returns both the answer and the source documents
        """
        # First try to answer from documentation
        if self.qa_chain:
            try:
                result = self.qa_chain({"query": query})
                if result["result"]:
                    return {
                        "answer": result["result"],
                        "source": "DuploCloud Documentation",
                        "confidence": "high"
                    }
            except Exception as e:
                print(f"Error in QA chain: {e}")

        # If no good answer from docs, use agent with tools
        if self.agent:
            try:
                result = await self.agent.arun(query)
                return {
                    "answer": result,
                    "source": "Web Search",
                    "confidence": "medium"
                }
            except Exception as e:
                print(f"Error in agent: {e}")

        return {
            "answer": "I'm sorry, I couldn't find a good answer to your question.",
            "source": None,
            "confidence": "low"
        } 