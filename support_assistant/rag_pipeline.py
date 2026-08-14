import os
from typing import TypedDict
from models import QueryResponse

import chromadb
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph, END



# ==========================================================
# MOCK LLM TOGGLE
# ==========================================================

MOCK_LLM = os.getenv("MOCK_LLM", "1") == "1"


# ==========================================================
# LOAD EMBEDDING MODEL
# ==========================================================

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# ==========================================================
# CREATE CHROMADB CLIENT
# ==========================================================

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="zepto_policies"
)


# ==========================================================
# LOAD DOCUMENTS
# ==========================================================

docs_path = "docs"

documents = []
doc_ids = []

for file in sorted(os.listdir(docs_path)):
    if file.endswith(".txt"):
        with open(os.path.join(docs_path, file), "r", encoding="utf-8") as f:
            text = f.read()

        documents.append(text)
        doc_ids.append(file.replace(".txt", ""))

print(f"Loaded {len(documents)} documents")


# ==========================================================
# GENERATE EMBEDDINGS
# ==========================================================

embeddings = embedding_model.encode(
    documents,
    convert_to_numpy=True
)

print("Embeddings Generated")


# ==========================================================
# STORE DOCUMENTS IN CHROMADB
# ==========================================================

try:
    collection.add(
        ids=doc_ids,
        documents=documents,
        embeddings=embeddings.tolist()
    )
    print("Documents Stored Successfully")

except Exception:
    print("Documents already exist in ChromaDB")


# ==========================================================
# TEST RETRIEVAL
# ==========================================================

query = "What is the refund policy?"

query_embedding = embedding_model.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

print("\nRetrieved IDs:")
print(results["ids"])

print("\nRetrieved Documents:")

for doc in results["documents"][0]:
    print("-" * 60)
    print(doc[:250])


# ==========================================================
# LANGGRAPH STATE
# ==========================================================

class GraphState(TypedDict):
    query: str
    intent: str
    answer: str
    sources: list
    confidence: float


# ==========================================================
# NODE 1 : CLASSIFY INTENT
# ==========================================================

def classify_intent(state: GraphState):

    query = state["query"].lower()

    keywords = [
    "delivery",
    "return",
    "refund",
    "membership",
    "tracking",
    "cancel",
    "gift card",
    "support",
    "customer support",
    "contact",
    "email",
    "chat",
    "phone",
    "reschedule",
    "order",
    "policy"
]

    if any(keyword in query for keyword in keywords):
        state["intent"] = "policy_question"
    else:
        state["intent"] = "general_question"

    return state


def retrieve_and_answer(state: GraphState):

    query = state["query"]

    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    retrieved_docs = results["documents"][0]
    retrieved_ids = results["ids"][0]

    # ===============================
    # MOCK MODE (Graded Baseline)
    # ===============================
    if MOCK_LLM:

        top_chunk = retrieved_docs[0][:200]

        answer = (
            f"Based on the retrieved context: {top_chunk}"
        )

    # ===============================
    # REAL LLM (Optional)
    # ===============================
    else:

        answer = (
            "Real LLM response will be implemented here."
        )

    state["answer"] = answer
    state["sources"] = retrieved_ids
    state["confidence"] = 1.0

    return state

# ==========================================================
# NODE 3 : DIRECT ANSWER
# ==========================================================

def direct_answer(state: GraphState):

    if MOCK_LLM:

        answer = (
            "I can only answer questions about Zepto policies right now."
        )

    else:

        answer = (
            "Real LLM general response will be implemented here."
        )

    state["answer"] = answer
    state["sources"] = []
    state["confidence"] = 1.0

    return state

# ==========================================================
# ROUTER
# ==========================================================

def route_intent(state: GraphState):

    if state["intent"] == "policy_question":
        return "retrieve_and_answer"

    return "direct_answer"


# ==========================================================
# BUILD LANGGRAPH
# ==========================================================

graph = StateGraph(GraphState)

graph.add_node("classify_intent", classify_intent)
graph.add_node("retrieve_and_answer", retrieve_and_answer)
graph.add_node("direct_answer", direct_answer)

graph.set_entry_point("classify_intent")

graph.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer"
    }
)

graph.add_edge("retrieve_and_answer", END)
graph.add_edge("direct_answer", END)

app = graph.compile()

print("\nLangGraph Created Successfully")


# ==========================================================
# TEST 1
# ==========================================================

print("\n" + "=" * 60)
print("TEST 1 : POLICY QUESTION")
print("=" * 60)

result = app.invoke({
    "query": "What is the refund policy?"
})

response = QueryResponse(
    answer=result["answer"],
    sources=result["sources"],
    confidence=result["confidence"]
)

print(response.model_dump())


# ==========================================================
# TEST 2
# ==========================================================

print("\n" + "=" * 60)
print("TEST 2 : GENERAL QUESTION")
print("=" * 60)

result = app.invoke({
    "query": "Who is Virat Kohli?"
})

response = QueryResponse(
    answer=result["answer"],
    sources=result["sources"],
    confidence=result["confidence"]
)

print(response.model_dump())