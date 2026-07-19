from pydantic import BaseModel

from fastapi import FastAPI
from transformers import pipeline

from sqlite_database import CreateDatabase


def load_model():
    return pipeline(
        task="text-generation",
		model="Qwen/Qwen2.5-1.5B"
    )


ml = {}
async def lifespan(app: FastAPI):
	ml['text_generator'] = load_model()
	yield
	ml.clear()


app = FastAPI(
	title="AI Engineering with FastAPI and Transformers(HF models)",
	description="A simple FastAPI application that uses Hugging Face Transformers for text generation.",
	lifespan=lifespan
)


class ReviewRequest(BaseModel):
	prompt: str


class GeneratedResponse(BaseModel):
	prompt_text: str
	generated_text: str


@app.get("/", tags=["health"])
def health_checks():
	return {"status": "Server Healthy and Running", "model_loaded": "text_generator" in ml}


@app.post("/generate", response_model=GeneratedResponse, tags=["text-generation"])
async def generate(request: ReviewRequest):
	result = ml['text_generator'](request.prompt)[0]
	db_path = "database/ai_engineering.db"
	db = CreateDatabase(db_path=db_path)
	db.save_response(request.prompt, result['generated_text'])
	return GeneratedResponse(
		prompt_text=request.prompt,
		generated_text=result['generated_text']
	)
