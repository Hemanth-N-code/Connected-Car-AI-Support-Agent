from rag.retriever import (
    retrieve_documents
)

def knowledge_agent(state):

    query = state["customer_query"]

    docs = retrieve_documents(query)

    kb_context = "\n\n".join(docs)

    state["kb_context"] = kb_context
    state["investigation_steps"].append(
    "RAG Agent retrieved knowledge base documents"
)
    print("\nRAG RETRIEVAL")

    print(kb_context[:500])

    return state