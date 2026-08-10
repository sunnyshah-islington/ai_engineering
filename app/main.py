import os

from dotenv import load_dotenv
from fastapi import FastAPI
from transformers import pipeline

from app.models_validation import (
    ModelStatus,
    ReviewRequest,
    GeneratedResponse,
    SentimentResponse,
)

from app.postgres_database import CreatePostgresDatabase

load_dotenv()

DB_HOST = os.environ["DB_HOST"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "postgres")


def load_model():
    return pipeline(
        task="text-generation",
        model="Qwen/Qwen2.5-1.5B",
    )


def load_ai_sentiment_model():
    return pipeline(
        task="sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
    )


ml = {}


async def lifespan(app: FastAPI):
    # ml["text_generator"] = load_model()
    ml["sentiment_analyzer"] = load_ai_sentiment_model()
    yield
    ml.clear()


app = FastAPI(
    title="AI Engineering with FastAPI and Transformers(HF models)",
    description="A simple FastAPI application that uses Hugging Face Transformers for text generation and sentiment analysis.",
    lifespan=lifespan,
)


@app.get("/", tags=["health"])
def health_checks():
    return ModelStatus(
        model_loaded="text_generator" in ml or "sentiment_analyzer" in ml,
        status=("Server Healthy and Running" if "text_generator" in ml or "sentiment_analyzer" in ml else "Server Unhealthy: Models not loaded"),
    )


@app.post("/generate_text", response_model=GeneratedResponse, tags=["text-generation"])
async def generate(request: ReviewRequest):
    result = ml['text_generator'](request.prompt)[0]
    db = CreatePostgresDatabase(host=DB_HOST, password=DB_PASSWORD, port=DB_PORT, dbname=DB_NAME, user=DB_USER)
    db.save_response_text_gen(request.prompt, result["generated_text"])
    return GeneratedResponse(
        prompt_text=request.prompt,
        generated_text=result["generated_text"]
    )


@app.post("/analyze_sentiment", response_model=SentimentResponse, tags=["sentiment-analysis"])
async def analyze_sentiment(request: ReviewRequest):
    result = ml["sentiment_analyzer"](request.prompt)[0]
    db = CreatePostgresDatabase(host=DB_HOST, password=DB_PASSWORD, port=DB_PORT, dbname=DB_NAME, user=DB_USER)
    db.save_response_sentiment(request.prompt, result["label"], float(result["score"]))
    return SentimentResponse(
        prompt_text=request.prompt,
        sentiment=result["label"],
        confidence=round(float(result["score"]), 4),
    )
