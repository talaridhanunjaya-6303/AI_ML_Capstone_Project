from fastapi import FastAPI
from models import QueryRequest, QueryResponse
from rag_pipeline import app as graph_app

app = FastAPI(
    title="Zepto Support Assistant",
    description="RAG + LangGraph + ChromaDB",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "Zepto Support Assistant API is Running!"
    }


@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):

    result = graph_app.invoke(
        {
            "query": request.query
        }
    )

    return QueryResponse(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"]
    )