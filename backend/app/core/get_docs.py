from llama_index import VectorStoreIndex, SimpleDirectoryReader

def get_docs():
    documents = SimpleDirectoryReader("./docs").load_data()
    # index = VectorStoreIndex.from_documents(documents)
    # query_engine = index.as_query_engine()
    # response = query_engine.query("Some question about the data should go here")
    # print(response)
    return documents
