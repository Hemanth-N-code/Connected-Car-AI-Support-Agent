import chromadb

client = chromadb.PersistentClient(
    path="vector_store"
)

collection = client.get_collection(
    name="automotive_kb"
)

def retrieve_documents(query):

    results = collection.query(
        query_texts=[query],
        n_results=2
    )

    return results["documents"][0]