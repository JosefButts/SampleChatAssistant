# Python standard library imports
import logging
import os
import traceback
from typing import Dict

# Third-party imports
from langgraph.prebuilt import create_react_agent
from llama_index import SimpleDirectoryReader

# Langchain imports
from langchain.chains import RetrievalQA
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import BaseTool, tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

logger = logging.getLogger(__name__)




class SearchWebTool(BaseTool):
    name: str = "search_web"
    description: SyntaxWarning = "Search the web for current events or general knowledge"
    search: SerpAPIWrapper

    def _run(self, query: str) -> str:
        return self.search.run(query)

class SearchDocsTool(BaseTool):
    name: str = "search_docs"
    description: str = "Search the documentation"
    # retriever: Any

    def _run(self, query: str) -> str:
        return self.retriever.invoke(query)
    

class AIAssistant:
    def __init__(self, api_key: str):
        try:
            self.llm = ChatOpenAI(
                temperature=0,
                model="gpt-4-turbo-preview",
                openai_api_key=api_key
            )
            self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
            self.qa_chain = None
            self.agent = None
            self.tools = []
            self.vector_store = None
            self.search = SerpAPIWrapper()
            self.initialize_knowledge_base()
        except Exception as e:
            logger.error(f"Error initializing AIAssistant: {str(e)}\nStack trace: {traceback.format_exc()}")
            raise e

    def get_docs(self):
        try:
            llama_docs = SimpleDirectoryReader(os.path.join("./app/docs/application-focussed-interface/")).load_data()
            langchain_docs = []
            for doc in llama_docs:
                try:
                    langchain_docs.append(Document(
                        page_content=doc.text,
                        metadata={"source": doc.metadata.get("file_name", "")}
                    ))
                except Exception as e:
                    logger.error(f"Error converting document: {str(e)}\nStack trace: {traceback.format_exc()}")
            return langchain_docs
        except Exception as e:
            logger.error(f"Error loading documents: {str(e)}\nStack trace: {traceback.format_exc()}")
            return []

    def initialize_knowledge_base(self):
        try:
            documents = self.get_docs()
            if not documents:
                logger.error("No documents loaded for knowledge base initialization")
                raise ValueError("No documents available")

            try:
                self.vector_store = Chroma.from_documents(documents, self.embeddings)
            except Exception as e:
                logger.error(f"Error creating vector store: {str(e)}\nStack trace: {traceback.format_exc()}")
                raise

            try:
                self.qa_chain = RetrievalQA.from_chain_type(
                    llm=self.llm,
                    chain_type="stuff",
                    retriever=self.vector_store.as_retriever(return_source_documents=True)
                )
            except Exception as e:
                logger.error(f"Error creating QA chain: {str(e)}\nStack trace: {traceback.format_exc()}")
                raise

            @tool
            def search_docs(query: str) -> str:
                """Search the vector store for relevant documents"""
                return self.vector_store.as_retriever(
                    return_source_documents=True
                ).invoke(query)
            

            # Define tools
            @tool
            def search_web(query: str) -> str:
                """Search the web for current events or general knowledge."""
                return self.search.run(query)

            tools = [search_web, search_docs]
            self.tools = tools

            prompt = PromptTemplate.from_template(
                """
                You are a helpful assistant that can answer questions
                You have access to the following tools: {tools}. 
             
                For information on Duplocloud search the documentation first before using the web search to answer any questions.
                Use websearch if the documentation does not have the answer to the user's question,
                or the answer requires a current event or general knowledge.
                If the answers come from the web search, cite the link if possible.
                Cite the source (document name, web search etc ) of your answer as a markdown list.
                
                """
            )
            
            ## Modify the agent creation
            self.agent = create_react_agent(
                model=self.llm,
                tools=self.tools,
                state_modifier=prompt.format(tools=self.tools)  # Pass tools explicitly
)
        except Exception as e:
            logger.error(f"Error initializing knowledge base: {str(e)}\nStack trace: {traceback.format_exc()}")
            raise e

    async def get_response(self, query: str) -> Dict:
        """
        Get response from the assistant
        Returns both the answer and the source documents
        """
        try:
            if not self.agent:
                logger.error("Agent not initialized")
                raise ValueError("Agent not properly initialized")

            try:
                inputs = {
                    "messages": [HumanMessage(content=query)],
                    "chat_history": []
                }
                result = await self.agent.ainvoke(inputs)
            except Exception as e:
                logger.error(f"Error invoking agent: {str(e)}\nStack trace: {traceback.format_exc()}")
                raise

            if isinstance(result, dict) and 'messages' in result:
                return {"answer": result['messages'][-1].content}
            else:
                logger.error(f"Unexpected response format: {result}")
                raise ValueError("Unexpected response format from agent")

        except Exception as e:
            logger.error(f"Error getting response: {str(e)}\nStack trace: {traceback.format_exc()}")
            return {
                "answer": f"I encountered an error: {str(e)}",
            } 