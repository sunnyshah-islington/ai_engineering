from pydantic import BaseModel


class ReviewRequest(BaseModel):
	prompt: str


class GeneratedResponse(BaseModel):
	prompt_text: str
	generated_text: str


class SentimentResponse(BaseModel):
	prompt_text: str
	sentiment: str
	confidence: float


class ModelStatus(BaseModel):
	status: str
	model_loaded: bool
